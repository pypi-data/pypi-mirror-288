import os
import unittest
from app.python_utils.src.project_structure_gen import ProjectStructure

class TestProjectStructure(unittest.TestCase):
    """
    Unit test class for testing ProjectStructure functionality.

    This class tests the ProjectStructure class, specifically its ability 
    to generate and format the project's directory structure, excluding 
    files and directories specified in a .gitignore file, and save the 
    structure to a Markdown file.

    Methods:
    test_project_structure_generation(): Tests the generation of the project 
    structure and the creation of the Markdown file.
    """

    def setUp(self):
        """
        Set up the test environment.

        Initializes the ProjectStructure instance and prepares paths for 
        the test.
        """
        self.root_path = r'D:\repos\current\python-utility-functions'
        self.gitignore_file = os.path.join(self.root_path, '.gitignore')
        self.structure_path = os.path.join(self.root_path, r'app\python_utils\src\local_test\structure.md')
        self.project_structure = ProjectStructure(self.root_path, self.gitignore_file, self.structure_path)

    def tearDown(self):
        """
        Clean up after tests.

        Removes the Markdown file created during the test to avoid residual 
        files.
        """
        if os.path.exists(self.structure_path):
            os.remove(self.structure_path)

    def test_project_structure_generation(self):
        """
        Tests the generation of the project structure and the creation of 
        the Markdown file.

        This test:
        - Calls the generate() method of the ProjectStructure class.
        - Verifies that the Markdown file is created.
        - Checks that the Markdown file contains the formatted project structure.

        Assertions:
        - Ensures the Markdown file exists after generation.
        - Checks that the Markdown file contains the expected project structure.
        """
        # Generate the project structure and create the Markdown file
        self.project_structure.generate()

        # Check if the Markdown file was created
        self.assertTrue(os.path.exists(self.structure_path), "Markdown file was not created.")

        # Read the content of the Markdown file
        with open(self.structure_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Check if the Markdown file contains the root folder and other expected content
        root_folder = self.root_path.split('\\')[-1] + '/'
        self.assertIn(root_folder, content, "Root folder not found in Markdown file.")

        print('====================Project Structure Generator Test Successful.====================')

if __name__ == '__main__':
    unittest.main()
