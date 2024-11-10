import os
import shutil
from tkinter import filedialog, messagebox


def select_origin_folder() -> str:
    """
    Prompts the user to select the origin folder using a file dialog.

    Returns:
        str: The path to the selected origin folder.
    """
    print("Select the folder where the files are located")
    path = filedialog.askdirectory(title="Select origin folder")
    if not os.path.exists(path):
        print("The path does not exist")
        return select_origin_folder()
    return path


def select_destination_folder() -> str:
    """
    Prompts the user to select the destination folder using a file dialog.

    Returns:
        str: The path to the selected destination folder.
    """
    print("Select the forder where the files will be moved")
    path = filedialog.askdirectory(title="Select destination folder")
    if not os.path.exists(path):
        print("The path does not exist")
        return select_destination_folder()
    return path


def select_file_name() -> str:
    """
    Prompts the user to enter the file name to move.

    Returns:
        str: The entered file name. If left blank, returns an empty string.
    """
    print("Select the file name to move")
    name = input("Enter the file name (leave blank for all): ")
    return name


def select_file_extension() -> str:
    """
    Prompts the user to enter the file extension to move.

    Returns:
        str: The entered file extension. If left blank, returns an empty string.
    """
    print("Select the file extension to move")
    extension = input("Enter the file extension (leave blank for all): ")
    if extension[0] != ".":
        extension = "." + extension
    return extension


def preview_files(origin: str, name: str, extension: str, starts_with: bool, case_sensitive: bool) -> None:
    """
    Prints a preview of the files to be moved based on the given criteria.

    Args:
        origin (str): The path to the origin folder.
        name (str): The file name or part of the file name to match.
        extension (str): The file extension to match.
        starts_with (bool): Whether to match files that start with the given name.
        case_sensitive (bool): Whether the matching should be case-sensitive.
    """
    print("Files to move:")
    for file in os.listdir(origin):
        if case_sensitive:
            if starts_with:
                if if_filename_starts_and_ends(name, extension, file):
                    print(file)
            else:
                if if_filename_contains_and_ends(name, extension, file):
                    print(file)
        else:
            if starts_with:
                if if_filename_starts_and_ends(name.lower(), extension.lower(), file.lower()):
                    print(file)
            else:
                if if_filename_contains_and_ends(name.lower(), extension.lower(), file.lower()):
                    print(file)


def list_files_to_move(origin: str, name: str, extension: str, starts_with: bool, case_sensitive: bool) -> list[
    tuple[str, bool]]:
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
    for file in os.listdir(origin):
        if case_sensitive:
            if starts_with:
                if if_filename_starts_and_ends(name, extension, file):
                    files.append((file, True))
            else:
                if if_filename_contains_and_ends(name, extension, file):
                    files.append((file, True))
        else:
            if starts_with:
                if if_filename_starts_and_ends(name.lower(), extension.lower(), file.lower()):
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


def move_files(origin: str, destination: str, name: str, extension: str) -> None:
    """
    Moves files from the origin folder to the destination folder based on the given name and extension.

    Args:
        origin (str): The path to the origin folder.
        destination (str): The path to the destination folder.
        name (str): The file name or part of the file name to match.
        extension (str): The file extension to match.
    """
    for file in os.listdir(origin):
        if name in file and file.endswith(extension):
            os.rename(os.path.join(origin, file), os.path.join(destination, file))


def move_files_list(origin: str, destination: str, files: list[tuple[str, bool]]) -> None:
    """
    Moves the specified files from the origin folder to the destination folder.

    Args:
        origin (str): The path to the origin folder.
        destination (str): The path to the destination folder.
        files (list[tuple[str, bool]]): A list of tuples containing the file name and a boolean indicating whether the file should be moved.
    """
    for file, move in files:
        if move:
            file_path = os.path.join(origin, file)
            try:
                shutil.move(file_path, destination)
            except PermissionError as e:
                messagebox.showerror("Permission Error", f"Failed to move {file_path} to {destination}: {e}")

def change_move_option(files: list[tuple[str, bool]], index: int) -> list[tuple[str, bool]]:
    """
    Changes the move option for the specified file in the list.

    Args:
        files (list[tuple[str, bool]]): A list of tuples containing the file name and a boolean indicating whether the file should be moved.
        index (int): The index of the file to change the move option for.

    Returns:
        list[tuple[str, bool]]: The updated list of files.
    """
    if 0 <= index < len(files):
        files[index] = (files[index][0], not files[index][1])
    return files