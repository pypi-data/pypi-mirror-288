from PIL import Image as PILImage
import cv2
from pathlib import Path
import time
from typing import List, Literal, Optional, Union
from mcap.writer import Writer
import numpy as np
from io import BytesIO
import re
import dataclasses

# protobuf serialization utils
from mcap_protobuf.writer import Writer as ProtobufWriter
from foxglove_schemas_protobuf.CompressedImage_pb2 import CompressedImage as CompressedImage_Protobuf

# ros2 serialization utils
from rosbags.typesys import Stores, get_typestore
from rosbags.typesys.stores.latest import builtin_interfaces__msg__Time, std_msgs__msg__Header, sensor_msgs__msg__CompressedImage

# CV2 image serialization
import cv2

from mcap_ros2.writer import Writer as mcap_ros2_Writer
from mcap.writer import Writer as MCAPWriter
from mcap.well_known import SchemaEncoding, MessageEncoding

from roboto.domain import topics
from roboto_ingestion_utils import ingestion_utils

ALLOWED_IMG_FORMATS = ["png", "jpg", "jpeg"]
MAX_UINT32 = 2 ** 32 - 1
COMPRESSED = True

typestore = get_typestore(Stores.LATEST)

def create_image_message_path_request(message_path_name: str):
    message_path = topics.AddMessagePathRequest(
            message_path=message_path_name,
            data_type="image",
            canonical_data_type=topics.CanonicalDataType.Image,
            )
    return [message_path]

def image_to_message(fname: Union[str, Path], 
                     timestamp: int, 
                     timestamp_format: str,
                     encoding: Literal['protobuf', 'cdr'],
                     frame_id: Optional[int]=None):
    if isinstance(fname, str):
        fname = Path(fname)

    ext = fname.suffix.lower()[1:] # remove period from extension
    assert ext in ALLOWED_IMG_FORMATS, f"Error: expected an image format from {ALLOWED_IMG_FORMATS}, received {ext}"


    if encoding == 'protobuf':
        raw_img = PILImage.open(fname)
        msg = CompressedImage_Protobuf()
        if timestamp_format == "seconds":
            msg.timestamp.FromSeconds(timestamp)
        elif timestamp_format == "milliseconds":
            msg.timestamp.FromMilliseconds(timestamp)
        elif timestamp_format == "microseconds":
            msg.timestamp.FromMicroseconds(timestamp)
        elif timestamp_format == "nanoseconds":
            msg.timestamp.FromNanoseconds(timestamp)
        else:
            raise ValueError(f"Error: timestamp must be in format seconds, milliseconds, microseconds, or nanoseconds, received {timestamp_format}")
        buffer = BytesIO()
        # convert jpg to jpeg
        raw_img.save(buffer, format='jpeg')
        msg.data = buffer.getvalue()
        msg.format = 'JPEG' 
    elif encoding ==  'cdr':
        # ROS2 messages require passing a frame_id
        assert frame_id is not None, "Error: ROS2 messages require a frame id"
        nanoseconds = 0
        seconds = 0
        if timestamp_format == "seconds":
            nanoseconds = int(timestamp * 1e9)
        elif timestamp_format == "milliseconds":
            nanoseconds = int(timestamp * 1e6)
        elif timestamp_format == "microseconds":
            nanoseconds = int(timestamp * 1e3)
        elif timestamp_format == "nanoseconds":
            nanoseconds = timestamp # timestamp automatically in NS

        if nanoseconds > MAX_UINT32: # roll over overflow
            seconds = nanoseconds // MAX_UINT32
            nanoseconds -= seconds * MAX_UINT32

        cv_img = cv2.imread(str(fname))
        _, im_buff_arr = cv2.imencode(".jpg", cv_img)

        ros_timestamp = builtin_interfaces__msg__Time(sec=int(seconds), nanosec=int(nanoseconds))
        ros_header = std_msgs__msg__Header(stamp=ros_timestamp, frame_id="imgs")
        msg = sensor_msgs__msg__CompressedImage(
                header=ros_header,
                data=im_buff_arr,
                format="jpeg"# try jgp
                ) 
    return msg

def image_dir_to_mcap(input_dir: Path,
                      output_dir: Optional[Union[str, Path]]=None,
                      timestamp_format: str="nanoseconds",
                      img_format: Optional[str]=None,
                      start_timestamp: Optional[int]=None,
                      frame_rate: Optional[int]=None,
                      timestamps: Optional[List]=None,
                      encoding: Literal['protobuf', 'cdr']='protobuf'):
    """
    Ingest a directory of images to an mcap file
    using encoding:
        1. foxglove's CompressedImage protobuf format
        2. CDR ROS2 format
    """
    assert encoding in ["protobuf", "cdr"]
    if img_format:
        assert img_format.lower() in ALLOWED_IMG_FORMATS, f"Error: expected one of {ALLOWED_IMG_FORMATS}, received {img_format}"
    
    assert (frame_rate is not None and start_timestamp is not None) or timestamps is not None, "Error: must provide one of a timestamp list or a framerate at which to create timestamps"
    assert timestamp_format, "timestamp must be passed with a timestamp format string."

    # create a list of all image files of specified format in the input dir
    if img_format:
        image_files = [x for x in input_dir.glob(f"*{img_format}")]
    else:
        image_files = []
        for fmt in ALLOWED_IMG_FORMATS + [x.upper() for x in ALLOWED_IMG_FORMATS]:

            image_files.extend([x for x in input_dir.glob(f"*.{fmt}")])
    
    assert image_files, f"Error: no image files in {input_dir}"

    # Sort image files using custom logic
    sorted_img_files = sorted(image_files, key=custom_sort_key)


    rel_file_path = image_files[0] 
    
    if output_dir is None:
    # setup temp output directory
        output_dir, _ = ingestion_utils.setup_output_folder_structure(
                input_dir=str(input_dir),
                file_path=str(input_dir / rel_file_path)
                )
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    if frame_rate is not None and start_timestamp is not None:
        timestamps = [start_timestamp + int(x/frame_rate * 1e9) for x in range(len(sorted_img_files))]

    assert len(timestamps) == len(image_files), "Error: each image must have one timestamp,\
                            received {len(image_files) images and len(timestamps) timestamps}"

    # Write out to MCAP
    topic_name = input_dir.name
    fname = str(output_dir / f"{topic_name}.mcap")

    if encoding == "protobuf":
        with open(fname, "wb") as f:
            writer = ProtobufWriter(f)
            for i, (timestamp, image) in enumerate(zip(timestamps, sorted_img_files)):
                image_msg = image_to_message(image,
                                             timestamp=timestamp,
                                             timestamp_format=timestamp_format,
                                             encoding="protobuf",
                                             frame_id=i)
                writer.write_message(
                    topic=topic_name,
                    message=image_msg,
                        )
            writer.finish()
    elif encoding == "cdr":
        # 7/27 852: this now works, but i can't read it out properly
        ### This successfully writes out an MCAP file but it cannot be read:
        ### mcap.exceptions.InvalidMagic: not a valid MCAP file, 
        # invalid magic: (6, 242, 85, 7, 0, 0, 0, 0)
 
        msgtype = sensor_msgs__msg__CompressedImage.__msgtype__
        msgdef, _ = typestore.generate_msgdef(msgtype) # returns tuple def, checksum
        with open(fname, "wb") as stream:
            writer = MCAPWriter(stream)
            writer.start()
            schema_id = writer.register_schema(name=msgtype,
                                               encoding=SchemaEncoding.ROS2,
                                               data=msgdef.encode()) 
            channel_id = writer.register_channel(topic=topic_name,
                                                 message_encoding=MessageEncoding.CDR,
                                                 schema_id=schema_id
                                                 )

            for i, (timestamp, image) in enumerate(zip(timestamps, sorted_img_files)):
                image_msg = image_to_message(image,
                                             timestamp=timestamp,
                                             timestamp_format=timestamp_format,
                                             encoding="cdr",
                                             frame_id=i)
                #import pdb; pdb.set_trace()
                serialized_msg = typestore.serialize_cdr(image_msg,msgtype)
                writer.add_message(
                        channel_id=channel_id,
                        log_time=timestamp,
                        data=serialized_msg,
                        publish_time=timestamp,
                        sequence=i
                        )
            writer.finish()

    topic_entry = {}

    topic_entry["first_timestamp"] = timestamps[0] 
    topic_entry["last_timestamp"] = timestamps[-1]
    topic_entry["nr_msgs"] = len(sorted_img_files)
    topic_entry["mcap_path"] = fname
    topic_info_dict = {topic_name: topic_entry}

    return topic_info_dict, None, {}, {}

# custom sorting logic: extract number from file_name
# and use as sorting key, irrespective of zero-padding
def extract_number(file_path):
    file_name = file_path.name
    match = re.search(r'(\d+)', file_name)
    return int(match.group(0)) if match else None

def custom_sort_key(file_name):
    number_part = extract_number(file_name)
    if number_part is not None:
        return (0, number_part)
    else:
        return (1, file_name)
        
