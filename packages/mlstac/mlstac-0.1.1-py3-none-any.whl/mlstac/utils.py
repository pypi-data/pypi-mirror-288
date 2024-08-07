import json
import pathlib
import struct
from io import BytesIO
from typing import Optional, Tuple, Union
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import rasterio as rio
import requests


def read_mlstac_metadata_local(file: Union[str, pathlib.Path]) -> dict:
    """Read the metadata of a mlstac file

    Args:
        file (Union[str, pathlib.Path]): A MLSTAC file.

    Returns:
        dict: The metadata of the mlstac file.
    """

    with open(file, "rb") as f:
        # Read the FIRST 2 bytes of the file
        nmagic = f.read(2)

        if nmagic != (31011).to_bytes(2, "little"):
            raise ValueError("The file is not a '.mlstac' file")

        # Read the NEXT 8 bytes of the file
        header_len = f.read(8)

        # Convert bytes to uint64
        length = int.from_bytes(header_len, "little")

        # Read the HEADER considering the length (JSON)
        header = f.read(length)

        # Read the bytes 100-200
        header = json.loads(header.decode())

    return header


def read_mlstac_data_local(
    file: Union[str, pathlib.Path],
    datapoint: pd.Series,
    metadata_length: Optional[dict] = None,
) -> Tuple[np.ndarray, dict]:
    """Read the data of a mlstac file

    Args:
        file (Union[str, pathlib.Path]): The file to read.
        datapoint (pd.Series): The datapoint to read.
        metadata_length (Optional[dict], optional): The length of the
            metadata. If None, the code seeks the metadata of the file.
            Defaults to None.

    Returns:
        Tuple[np.ndarray, dict]: The data and metadata of the
            datapoint.
    """

    # Read the metadata
    if metadata_length is None:
        metadata = read_mlstac_metadata_local(file)
        metadata_length = len(json.dumps(metadata))

    # Define fseek
    fseek: int = datapoint["begin"] + metadata_length + 2 + 8

    with open(file, "rb") as f:
        # Move the pointer to the right position
        f.seek(fseek)

        # Read the specific bytes
        data: bytes = f.read(datapoint["length"])

        # Convert the bytes to a rasterio object
        data_memory = BytesIO(data)
        with rio.open(data_memory) as src:
            data: np.ndarray = src.read()
            metadata: dict = src.meta

    return data, metadata


def read_mlstac_metadata_url(url: str) -> dict:
    """Read the metadata of a mlstac file given a URL. The
    server must support the HTTPS Range Request.

    Args:
        url (str): The URL of the file.

    Returns:
        Tuple[dict, int]: The metadata of the mlstac file
        and the length of the header.
    """

    # Fetch the first 8 bytes of the file
    headers = {"Range": "bytes=2-9"}
    response: requests.Response = requests.get(url, headers=headers)

    # Interpret the bytes as a little-endian unsigned 64-bit integer
    length_of_header: int = struct.unpack("<Q", response.content)[0] + 9

    # Fetch length_of_header bytes starting from the 9th byte
    headers = {"Range": f"bytes=10-{length_of_header}"}
    response: requests.Response = requests.get(url, headers=headers)

    # Interpret the response as a JSON object
    header = response.json()

    return header


def read_mlstac_data_url(
    url: str, datapoint: pd.Series, metadata_length: Optional[int] = None
) -> Tuple[np.ndarray, dict]:
    """Read the data of a mlstac file given a URL.
    The server must support HTTPS Range Request.

    Args:
        URL (Union[str, pathlib.Path]): The file to be read.
        datapoint_id (str): The ID of the datapoint to read.
        length_metadata (Optional[int], optional): The length of the
            metadata. If None, the code seeks the metadata of the file.
            Defaults to None.

    Returns:
        Tuple[np.ndarray, dict]: The data and metadata of the
            datapoint.
    """

    # Read the metadata
    if metadata_length is None:
        metadata = read_mlstac_metadata_url(url)
        metadata_length = len(json.dumps(metadata))

    # Define the byte range to read the data
    fseek = datapoint["begin"] + metadata_length + 2 + 8

    # Define the HTTP Range Request
    headers = {"Range": f'bytes={fseek}-{fseek + datapoint["length"] - 1}'}

    # Fetch the data
    response = requests.get(url, headers=headers)
    data = response.content

    # Convert the bytes to a rasterio object
    data_memory = BytesIO(data)
    with rio.open(data_memory) as src:
        data = src.read()
        metadata = src.meta

    return data, metadata


def encode_json_array(
    data: dict, shape: tuple[int, int], dtype: np.dtype
) -> np.ndarray:
    """Encode a dictionary as a NumPy array.

    Args:
        data (dict): The dictionary to encode.
        shape (tuple[int, int]): The shape of the NumPy array.
        dtype (np.dtype): The data type of the NumPy array.

    Returns:
        np.ndarray: The NumPy array.
    """

    # Convert dictionary to JSON string
    json_bytes = json.dumps(data).encode("utf-8")

    # Convert the NumPy array to bytes
    array = np.zeros(shape, dtype=dtype)
    byte_data = array.tobytes()

    # Convert from bytes to bytearray
    byte_data_arr = bytearray(byte_data)

    # Replace eight bytes with the length of the JSON string (UInt64)
    len_bytes = struct.pack("Q", len(json_bytes))
    byte_data_arr[:8] = len_bytes
    byte_data_arr[8 : (8 + len(json_bytes))] = json_bytes

    return np.frombuffer(byte_data_arr, dtype=np.uint16).reshape(array.shape)


def decode_json_array(array: np.ndarray) -> dict:
    """Decode a NumPy array as a dictionary.

    Args:
        data (dict): The dictionary to encode.
        shape (tuple[int, int]): The shape of the NumPy array.
        dtype (np.dtype): The data type of the NumPy array.

    Returns:
        np.ndarray: The NumPy array.
    """

    # Convert the NumPy array to bytes
    byte_data = array.tobytes()

    # Read the length of the JSON string
    len_bytes = byte_data[:8]
    header_len = struct.unpack("Q", len_bytes)[0]

    # Read the JSON string
    json_bytes = byte_data[8 : (8 + header_len)]

    # Convert the JSON string to a dictionary
    return json.loads(json_bytes.decode("utf-8"))


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except ValueError:
        return False
