# System
import inspect
from typing import Any, Dict, List
from datetime import datetime
import os

# File
import pickle
import json
import toml
import h5py

# Math
import numpy as np


def check_file_exists(file_path: str) -> None:
    """
    Check if the specified file exists.

    Args:
        file_path (str): Path to the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")


def ensure_path_exists(path: str) -> None:
    """
    Ensure that the given path exists. If it's a directory, ensure the directory exists.
    If it's a file, ensure the directory containing the file exists.

    Args:
        path (str): Path to the file or directory.

    """
    # Determine if the path is a file or a directory
    if os.path.isfile(path) or os.path.splitext(path)[1]:
        # If it's a file, get the directory containing the file
        dir_path = os.path.dirname(path)
    else:
        # If it's a directory, use the path as is
        dir_path = path

    # Create the directory if it doesn't exist
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def read_pickle(file_path: str) -> Dict[str, Any]:
    """
    Read data from a Pickle file.

    Args:
        file_path (str): Path to the Pickle file.

    Returns:
        dict: Data read from the Pickle file.

    Raises:
        ValueError: If there is an error reading the Pickle file.
    """
    check_file_exists(file_path)
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
    except Exception as e:
        raise ValueError(f"Error reading Pickle file {file_path}") from e
    return data


def write_pickle(data: Dict[str, Any], file_path: str) -> None:
    """
    Write data to a Pickle file.

    Args:
        data (dict): Data to write to the Pickle file.
        file_path (str): Path to the Pickle file.

    Raises:
        ValueError: If there is an error writing to the Pickle file.
    """
    ensure_path_exists(file_path)
    try:
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        raise ValueError(f"Error writing to Pickle file {file_path}") from e


def read_json(file_path: str) -> Dict[str, Any]:
    """
    Read data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Python dictionary containing the parsed JSON data.
    """
    check_file_exists(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{file_path}': {e}")
        return None
    except Exception as e:
        raise (f"Unexpected error reading JSON from '{file_path}'") from e
    return data


def write_json(data: Dict[str, Any], file_path: str) -> None:
    """
    Write data to a JSON file.

    Args:
        data (dict): Data to write, should be a Python dictionary.
        file_path (str): Path to the JSON file.
    """

    ensure_path_exists(file_path)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Error writing JSON to {file_path}") from e


def read_toml(file_path: str) -> Dict[str, Any]:
    """
    Read data from a TOML file.

    Args:
        file_path (str): Path to the TOML file.

    Returns:
        dict: Python dictionary containing the parsed TOML data.
    """

    check_file_exists(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = toml.load(f)
    except toml.TomlDecodeError as e:
        raise ValueError(f"Error decoding TOML from {file_path}") from e
    return data


def write_toml(data: Dict[str, Any], file_path: str) -> None:
    """
    Write data to a TOML file.

    Args:
        data (dict): Data to write, should be a Python dictionary.
        file_path (str): Path to the TOML file.
    """

    ensure_path_exists(file_path)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            toml.dump(data, f)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Error writing TOML to {file_path}") from e


def read_hdf5(file_path: str) -> Dict[str, Any]:
    """
    Read data from an HDF5 file.

    Args:
        file_path (str): Path to the HDF5 file.

    Returns:
        dict: Python dictionary containing the data read from the HDF5 file.
    """

    check_file_exists(file_path)
    data = {}
    try:
        with h5py.File(file_path, "r") as f:
            for key, f_key in f.items():
                data[key] = np.array(f_key)
    except Exception as e:
        raise ValueError(f"Error reading HDF5 file {file_path}") from e
    return data


def write_hdf5(data: Dict[str, Any], file_path: str) -> None:
    """
    Write data to an HDF5 file.

    Args:
        data (dict): Data to write, should be a dictionary where values are numpy arrays.
        file_path (str): Path to the HDF5 file.
    """

    ensure_path_exists(file_path)
    try:
        with h5py.File(file_path, "w") as f:
            for key, value in data.items():
                f.create_dataset(key, data=value)
    except Exception as e:
        raise ValueError(f"Error writing to HDF5 file {file_path}") from e


def get_project_top_level_dir() -> str:
    """
    Get the top-level directory of the python project containing the current file.

    Returns:
        str: Absolute path to the top-level directory of the python project package.
    """

    stack = inspect.stack()
    caller_frame = stack[1]
    caller_file_path = os.path.abspath(caller_frame.filename)
    directory = os.path.dirname(caller_file_path)
    # Loop to find the top-level package directory
    while True:
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file):
            break
        directory = os.path.dirname(directory)

    return directory


def find_ros_package(package_name: str) -> str:
    import rospkg

    rospack = rospkg.RosPack()
    package_path = rospack.get_path(package_name)
    return package_path


def get_current_system_time() -> str:
    """
    Get the current system time in the format 'YYYYMMDDHHMMSS'.

    Returns:
        str: Current system time string in the format 'YYYYMMDDHHMMSS'.
    """

    current_time = datetime.now()
    return current_time.strftime("%Y%m%d%H%M%S")


def split_list_into_batches(
    list_to_split: List, batch_size: int, delete_last_one: bool = False
) -> List[List[Any]]:
    """
    Split a list into batches of a specified size.

    Args:
        list_to_split (list): The list to be split.
        batch_size (int): The size of each batch.
        delete_last_one (bool): Whether to delete the last batch if it is smaller than batch_size.

    Returns:
        list: A list of lists, where each inner list contains a batch of the original list.
    """

    batches = [
        list_to_split[i : i + batch_size]
        for i in range(0, len(list_to_split), batch_size)
    ]

    # Delete last one if flag is set
    if delete_last_one and len(batches[-1]) < batch_size:
        batches.pop()
    return batches


def get_list_segment(
    lst: List[Any], main_index: int, left_buffer: int, right_buffer: int
) -> List[Any]:
    """
    Get a segment from a list around a specified main index with left and right buffers.

    Args:
        lst (list): The list from which to extract the segment.
        main_index (int): The main index around which the segment is centered.
        left_buffer (int): Number of elements to include to the left of main_index.
        right_buffer (int): Number of elements to include to the right of main_index.

    Returns:
        list: A segment of the list centered around main_index with specified buffers.
    """
    length = len(lst)
    left_indices = [(main_index - i) % length for i in range(1, left_buffer + 1)]
    right_indices = [(main_index + i) % length for i in range(1, right_buffer + 1)]
    segment = (
        [lst[idx] for idx in left_indices[::-1]]
        + [lst[main_index]]
        + [lst[idx] for idx in right_indices]
    )
    return segment
