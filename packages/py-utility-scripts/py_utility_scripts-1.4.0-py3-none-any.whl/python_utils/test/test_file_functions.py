import unittest
import os
from app.python_utils.src.file_functions import FileRenamer

class TestFileFunctions(unittest.TestCase):
    """
    Unit test class for testing the FileRenamer class.

    Methods:
    test_file_renaming(): Tests the file renaming process using the FileRenamer class.
    """
    
    def test_file_renaming(self):
        """
        Tests the renaming of files in a specified directory.
        
        This test:
        - Sets up a FileRenamer instance with a given directory path, prefix, and name format.
        - Calls the rename_files method to rename files in the directory.
        - Verifies that the files have been renamed correctly.
        
        Note:
        - Ensure the test directory exists and contains files before running this test.
        - The test directory path and files should be properly configured in the testing environment.
        """
        # Define the test directory path and renaming parameters
        prefix = 'wallpaper'
        count = 0
        path = r'D:\repos\current\python-utility-functions\app\python_utils\src\local_test\walpapers'

        # Create an instance of FileRenamer with the specified parameters
        file_renamer = FileRenamer(path, prefix=prefix, name_format="{prefix}-{count:03d}")

        # Perform the file renaming
        file_renamer.rename_files()

        # Get the list of files in the directory after renaming
        files = os.listdir(path)

        # Check if files have been renamed correctly
        for i, file in enumerate(files):
            # Expected new file name based on the prefix and count
            expected_name = f"{prefix}-{i+1:03d}"
            # Extract the file extension
            extension = file.split('.')[-1]
            # Construct the expected file name with extension
            expected_file_name = f"{expected_name}.{extension}"
            # Verify that the file has the expected name
            self.assertIn(expected_file_name, files, f"File '{expected_file_name}' not found in directory.")
        
        print('====================File Function Test Successful.====================')

if __name__ == '__main__':
    unittest.main()
