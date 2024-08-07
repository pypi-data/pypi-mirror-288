import json
import pathlib
from typing import List, Tuple, Union

import numpy as np
import pandas as pd

import mlstac.utils


def load_metadata(path: Union[str, pathlib.Path]) -> pd.DataFrame:
    """Load a MLSTAC file

    Args:
        path (Union[str, pathlib.Path]): The path to the MLSTAC file.
            It can be a local path or a URL. If it is a URL, the
            server must support the HTTP Range requests.

    Returns:
        pd.DataFrame: The dataframe with three columns: 'datapoint_id',
            'begin', and 'length'. The 'datapoint_id' is the ID of the
            datapoint, 'begin' is the byte where the datapoint starts,
            and 'length' is the length of the datapoint in bytes.
    """

    # Obtain the file metadata
    if mlstac.utils.is_valid_url(path):
        dataset = mlstac.utils.read_mlstac_metadata_url(path)
        status = "remote"
    else:
        dataset = mlstac.utils.read_mlstac_metadata_local(path)
        status = "local"

    # Obtaint the length header
    length_dataset = len(json.dumps(dataset))

    # Convert dataset to DataFrame
    datapoints = list(dataset.items())
    metadata = pd.DataFrame(datapoints, columns=["datapoint_id", "values"])

    # Expand 'values' into 'begin' and 'length' columns
    metadata[["begin", "length"]] = pd.DataFrame(
        metadata["values"].tolist(), index=metadata.index
    )
    metadata = metadata.drop(columns="values")
    metadata.attrs.update(
        {"status": status, "path": path, "length_dataset": length_dataset}
    )

    return metadata


def load_data(
    dataset: pd.DataFrame,
    save_metadata_datapoint: bool = False,
    quiet: bool = False
) -> Union[np.ndarray, List[Tuple[np.ndarray, dict]]]:
    """Download the data of a MLSTAC file.

    Args:
        dataset (pd.DataFrame): A DataFrame with byte ranges of
            the datapoints.
        save_metadata_datapoint (bool, optional): Each datapoint
            has associated metadata. If True, the function returns
            a list of tuples with the data and metadata of each
            datapoint. If False, the function returns a numpy array
            with the data of each datapoint. Defaults to False.
        quiet (bool, optional): Whether to print the progress of
            the download. If the file is local, the progress is
            not printed. Defaults to False.

    Returns:
        Union[np.ndarray, List[Tuple[np.ndarray, dict]]]: The data
            of the datapoints. If save_metadata_datapoint is True,
            the function returns a list of tuples with the data and
            metadata of each datapoint. If save_metadata_datapoint
            is False, the function returns a numpy array with the
            data of each datapoint.
    """

    content = []
    if dataset.attrs["status"] == "remote":
        for idx, row in dataset.iterrows():

            # Print the progress of the download
            if not quiet:
                print(f"Downloading datapoint: {row['datapoint_id']}")

            # Read the data and metadata of the datapoint
            data, metadata = mlstac.utils.read_mlstac_data_url(
                url=dataset.attrs["path"],
                datapoint=row,
                metadata_length=dataset.attrs["length_dataset"],
            )

            # Whether to save the metadata of the datapoint
            if save_metadata_datapoint:
                content.append((data, metadata))
            else:
                content.append(data)
    else:
        for idx, row in dataset.iterrows():
            # Read the data and metadata of the datapoint
            data, metadata = mlstac.utils.read_mlstac_data_local(
                file=dataset.attrs["path"],
                datapoint=row,
                metadata_length=dataset.attrs["length_dataset"],
            )

            # Whether to save the metadata of the datapoint
            if save_metadata_datapoint:
                content.append((data, metadata))
            else:
                content.append(data)

    # Convert the content to a numpy array if not save_metadata_datapoint
    if not save_metadata_datapoint:
        content = np.array(content)

    return content
