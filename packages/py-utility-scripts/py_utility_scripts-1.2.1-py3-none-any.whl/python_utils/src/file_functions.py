"""
This script renames all files in a specified directory to a sequentially 
numbered format with a user-defined prefix and format.

Classes:
- FileRenamer: Handles the file renaming process within a specified directory.

Usage:
- Ensure the 'path' variable in the main function is set to the target directory.
- Create an instance of FileRenamer with the desired path, prefix, and name format.
- Run the script to rename files based on the specified format.

Note:
- This script does not handle subdirectories; it processes files in the specified directory only.
- Ensure appropriate permissions and backups before running the script.
"""

import os

class FileRenamer:
    """
    A class to handle renaming files in a specified directory.

    Attributes:
    path (str): The path to the directory containing files to rename.
    prefix (str): The prefix to use for renamed files.
    count (int): The starting number for the file renaming sequence.
    name_format (str): The format string for renaming files.

    Methods:
    get_paths(): Returns all the files and directories in the given path.
    rename_file(old_name, new_name): Renames a file or folder.
    rename_files(): Renames all files in the specified directory to a sequentially numbered format with the prefix.
    """
    
    def __init__(self, path, prefix="wallpaper", count=0, name_format="{prefix}-{count}"):
        """
        Initializes the FileRenamer with the target directory path, prefix, starting count, and name format.

        Parameters:
        path (str): The path to the directory containing files to rename.
        prefix (str): The prefix to use for renamed files.
        count (int): The starting number for the file renaming sequence.
        name_format (str): The format string for renaming files.
        """
        self.path = path
        self.prefix = prefix
        self.count = count
        self.name_format = name_format

    def get_paths(self):
        """
        Returns all the files and directories in the given path.

        Returns:
        list: A list of files and directories in the specified path.
        """
        return os.listdir(self.path)

    def rename_file(self, old_name, new_name):
        """
        Renames a file or folder from old_name to new_name.

        Parameters:
        old_name (str): The current name of the file or folder.
        new_name (str): The new name for the file or folder.
        """
        os.rename(old_name, new_name)

    def rename_files(self):
        """
        Renames all files in the specified directory to a sequentially numbered format with the prefix.

        The function will:
        1. Retrieve all files from the given directory.
        2. Iterate through each file, generating a new name in the format '<PREFIX>-X.extension'.
        3. Rename each file to the new name.

        Notes:
        - This function does not handle subdirectories; it processes files in the specified directory only.
        - Ensure the specified path is correct and you have appropriate permissions.
        """
        files = self.get_paths()

        for file in files:
            extension = file.split(".")[-1]
            self.count += 1
            new_name = self.name_format.format(prefix=self.prefix, count=self.count) + f".{extension}"
            old_path = os.path.join(self.path, file)
            new_path = os.path.join(self.path, new_name)
            self.rename_file(old_path, new_path)