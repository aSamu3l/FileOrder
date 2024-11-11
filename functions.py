import os
import shutil
from CTkMessagebox import CTkMessagebox as CTkM
from customtkinter import filedialog as fd


def select_origin_folder() -> str:
    """
    Prompts the user to select the origin folder using a file dialog.

    Returns:
        str: The path to the selected origin folder.
    """
    path = fd.askdirectory(title="Select origin folder")
    if not os.path.exists(path) and path != "":
        CTkM(title = "Error", message = "The path does not exist", icon = "cancel")
    return path


def select_destination_folder() -> str:
    """
    Prompts the user to select the destination folder using a file dialog.

    Returns:
        str: The path to the selected destination folder.
    """
    path = fd.askdirectory(title="Select destination folder")
    if not os.path.exists(path):
        CTkM(title = "Error", message = "The path does not exist", icon = "cancel")
        return ""
    return path


def list_files_to_move(origin: str, name: str, extension: str, starts_with: bool, case_sensitive: bool) -> list[tuple[str, bool]]:
    """
    Lists the files to be moved based on the given criteria.

    Args:
        origin (str): The path to the origin folder.
        name (str): The file name or part of the file name to match.
        extension (str): The file extension to match.
        starts_with (bool): Whether to match files that start with the given name.
        case_sensitive (bool): Whether the matching should be case-sensitive.

    Returns:
        list[tuple[str, bool]]: A list of tuples containing the file name and a boolean indicating whether the file should be moved.
    """
    files = []
    if extension != "" and not extension.startswith("."):
        extension = "." + extension
    for file in os.listdir(origin):
        if os.path.isdir(os.path.join(origin, file)):
            continue
        if case_sensitive:
            if starts_with:
                if extension == "":
                    if if_filename_starts(name, file):
                        files.append((file, True))
                else:
                    if if_filename_starts_and_ends(name, extension, file):
                        files.append((file, True))
            else:
                if extension == "":
                    if if_filename_contains(name, file):
                        files.append((file, True))
                else:
                    if if_filename_contains_and_ends(name, extension, file):
                        files.append((file, True))
        else:
            if starts_with:
                if extension == "":
                    if if_filename_starts(name.lower(), file.lower()):
                        files.append((file, True))
                else:
                    if if_filename_starts_and_ends(name.lower(), extension.lower(), file.lower()):
                        files.append((file, True))
            else:
                if extension == "":
                    if if_filename_contains(name.lower(), file.lower()):
                        files.append((file, True))
                else:
                    if if_filename_contains_and_ends(name.lower(), extension.lower(), file.lower()):
                        files.append((file, True))
    return files


def if_filename_starts(name: str, file: str) -> bool:
    """
    Checks if the file name starts with the given name.

    Args:
        name (str): The name to check.
        file (str): The file name.

    Returns:
        bool: True if the file name starts with the given name, False otherwise.
    """
    return file.startswith(name)


def if_filename_contains(name: str, file: str) -> bool:
    """
    Checks if the file name contains the given name.

    Args:
        name (str): The name to check.
        file (str): The file name.

    Returns:
        bool: True if the file name contains the given name, False otherwise.
    """
    return name in file


def if_filename_ends(extension: str, file: str) -> bool:
    """
    Checks if the file name ends with the given extension.

    Args:
        extension (str): The extension to check.
        file (str): The file name.

    Returns:
        bool: True if the file name ends with the given extension, False otherwise.
    """
    return file.endswith(extension)


def if_filename_starts_and_ends(name: str, extension: str, file: str) -> bool:
    """
    Checks if the file name starts with the given name and ends with the given extension.

    Args:
        name (str): The name to check.
        extension (str): The extension to check.
        file (str): The file name.

    Returns:
        bool: True if the file name starts with the given name and ends with the given extension, False otherwise.
    """
    return if_filename_starts(name, file) and if_filename_ends(extension, file)


def if_filename_contains_and_ends(name: str, extension: str, file: str) -> bool:
    """
    Checks if the file name contains the given name and ends with the given extension.

    Args:
        name (str): The name to check.
        extension (str): The extension to check.
        file (str): The file name.

    Returns:
        bool: True if the file name contains the given name and ends with the given extension, False otherwise.
    """
    return if_filename_contains(name, file) and if_filename_ends(extension, file)


def move_files_list(origin: str, destination: str, files: list[tuple[str, bool]]) -> None:
    """
    Moves the specified files from the origin folder to the destination folder.

    Args:
        origin (str): The path to the origin folder.
        destination (str): The path to the destination folder.
        files (list[tuple[str, bool]]): A list of tuples containing the file name and a boolean indicating whether the file should be moved.
    """
    exceptionCount = 0
    for file, move in files:
        if move:
            file_path = os.path.join(origin, file)
            try:
                shutil.move(file_path, destination)
            except PermissionError as e:
                CTkM(title="Permission Error", message=f"Failed to move {file_path} to {destination}", icon="cancel")
                exceptionCount += 1
            except shutil.Error as e:
                CTkM(title="Error", message=f"Failed to move {file_path} to {destination}", icon="cancel")
                exceptionCount += 1

    return exceptionCount

def copy_files_list(origin: str, destination: str, files: list[tuple[str, bool]]) -> None:
    """
    Copies the specified files from the origin folder to the destination folder.

    Args:
        origin (str): The path to the origin folder.
        destination (str): The path to the destination folder.
        files (list[tuple[str, bool]]): A list of tuples containing the file name and a boolean indicating whether the file should be copied.
    """
    exceptionCount = 0
    for file, copy in files:
        if copy:
            file_path = os.path.join(origin, file)
            try:
                shutil.copy(file_path, destination)
            except PermissionError as e:
                CTkM(title="Permission Error", message=f"Failed to copy {file_path} to {destination}", icon="cancel")
                exceptionCount += 1
            except shutil.Error as e:
                CTkM(title="Error", message=f"Failed to copy {file_path} to {destination}", icon="cancel")
                exceptionCount += 1

    return exceptionCount