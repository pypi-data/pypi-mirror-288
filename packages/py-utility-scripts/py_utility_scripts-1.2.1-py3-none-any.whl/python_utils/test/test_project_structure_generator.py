import os
import unittest
from src.project_structure_generator import ProjectStructure

class TestSqlFunctions(unittest.TestCase):
    def test_sql_functions(self):
        root_path = r'D:\repos\python-utility-functions'
        gitignore_file = os.path.join(root_path, '.gitignore')

        project_structure = ProjectStructure(root_path, gitignore_file)
        project_structure.generate()
        pass

if __name__ == '__main__':
    unittest.main()