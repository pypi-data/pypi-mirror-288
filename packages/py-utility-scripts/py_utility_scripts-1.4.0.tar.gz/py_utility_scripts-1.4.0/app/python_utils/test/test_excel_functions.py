import unittest
from app.python_utils.src.excel_functions import ExcelReader, WriteToExcel

class TestExcelFunctions(unittest.TestCase):
    """
    Unit test class for testing ExcelReader and WriteToExcel functionalities.
    
    Methods:
    test_write_and_read_excel(): Tests writing to and reading from an Excel file.
    """
    
    def test_write_and_read_excel(self):
        """
        Tests the process of writing data to an Excel file and then reading it back.
        
        This test:
        - Creates an Excel file with specific headers and data.
        - Reads the data from the file using ExcelReader.
        - Verifies that the data read matches the data written.
        
        Note:
        - Ensure the test directory exists and is writable.
        - The test directory path and file names should be properly configured in the testing environment.
        """
        # Define the file path
        file_path = r'app\python_utils\src\local_test\example.xlsx'
        
        # Define headers and data to be written to the Excel file
        headers = ['name', 'age', 'score']
        scores = [
            ['ankit', 12, 1000],
            ['rahul', 13, 100],
            ['priya', 12, 300],
            ['harshita', 12, 50],
        ]

        # Create an instance of WriteToExcel to write data to the Excel file
        excel_writer = WriteToExcel(file_path)
        excel_writer.write_data_to_excel(file_path, "sheet_1", 0, 0, headers, scores)

        # Create an instance of ExcelReader to read data from the Excel file
        excel_reader = ExcelReader(file_path, selected_columns=['name', 'score'])
        excel_reader.read_excel()
        values = list(excel_reader.iterate_rows())

        # Define expected data
        expected_data = [
            {'name': 'ankit', 'score': 1000},
            {'name': 'rahul', 'score': 100},
            {'name': 'priya', 'score': 300},
            {'name': 'harshita', 'score': 50},
        ]

        # Verify that the data read from the file matches the expected data
        self.assertEqual(values, expected_data, "The data read from the Excel file does not match the expected data.")

        print('====================Excel Function Test Successful.====================')

if __name__ == '__main__':
    unittest.main()
