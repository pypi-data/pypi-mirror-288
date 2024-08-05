"""
This script provides functionalities for reading from and writing to Excel files using the pandas 
and xlsxwriter libraries. The ExcelReader class reads specified columns from an Excel file and 
returns the data as a list of dictionaries. The WriteToExcel class creates new Excel workbooks 
and worksheets, and writes data to them.

Classes:
- ExcelReader: Reads data from an Excel file.
- WriteToExcel: Writes data to an Excel file.

Usage:
- Instantiate the ExcelReader class with the path to the Excel file and optional selected columns.
- Call the read_excel method to read the file, and iterate_rows to get data as a list of dictionaries.
- Instantiate the WriteToExcel class with the path to the Excel file.
- Use the createWorkbook, closeWorkbook, createWorksheet, defineRowColumn, and write_data_to_excel methods to write data.
"""

import pandas as pd
import xlsxwriter

class ExcelReader:
    """
    A class to read data from an Excel file.

    Attributes:
    file_path (str): Path to the Excel file.
    df (pandas.DataFrame): DataFrame to store the Excel data.
    selected_columns (list): List of columns to read from the Excel file.

    Methods:
    read_excel(): Reads the Excel file using the 'openpyxl' engine.
    iterate_rows(): Iterates through the rows of the DataFrame and returns a list of dictionaries.
    """
    
    def __init__(self, file_path, selected_columns=None):
        """
        Initializes the ExcelReader with the file path and optional selected columns.

        Parameters:
        file_path (str): Path to the Excel file.
        selected_columns (list, optional): List of columns to read. Defaults to None.
        """
        self.file_path = file_path
        self.df = None
        self.selected_columns = selected_columns

    def read_excel(self):
        """
        Reads the Excel file using the 'openpyxl' engine and stores it in a DataFrame.
        
        Returns:
            None
        """
        self.df = pd.read_excel(self.file_path, engine='openpyxl')

    def iterate_rows(self):
        """
        Iterates through the rows of the DataFrame and returns a list of dictionaries.
        Each dictionary contains the data for one row, with keys as column names.

        Returns:
        list: A list of dictionaries, each representing a row of data.
        """
        if self.df is None:
            print("Error: DataFrame is not initialized. Call read_excel() first.")
            return

        if self.selected_columns is None:
            self.selected_columns = self.df.columns

        rows_data = []
        for index, row in self.df.iterrows():
            row_data = {column: row[column] for column in self.selected_columns}
            rows_data.append(row_data)

        return rows_data

class WriteToExcel:
    """
    A class to write data to an Excel file.

    Attributes:
    workbook (str): Path to the Excel file.

    Methods:
    createWorkbook(): Creates a new Excel workbook.
    closeWorkbook(workbook): Closes the opened workbook.
    createWorksheet(workbook, sheet): Creates a new worksheet in the workbook.
    defineRowColumn(rowNum, columnNum): Defines the initial row and column for writing data.
    write_data_to_excel(file_name, data): Writes data to an Excel file with headers and rows.
    """
    
    def __init__(self, file_name) -> None:
        """
        Initializes the WriteToExcel with the file path.

        Parameters:
        workbook (str): Path to the Excel file.
        """
        self.file_name = file_name
        self.workbook = None

    def createWorkbook(self):
        """
        Creates a new Excel workbook.

        Returns:
        xlsxwriter.Workbook: The created workbook object.
        """
        self.workbook = xlsxwriter.Workbook(self.file_name)
        return self.workbook
    
    def closeWorkbook(self):
        """
        Closes the opened workbook.

        Parameters:
        workbook (xlsxwriter.Workbook): The workbook object to close.

        Returns:
            None
        """
        if self.workbook:
            self.workbook.close()

    def createWorksheet(self, sheet_name):
        """
        Creates a new worksheet in the workbook.

        Parameters:
        workbook (xlsxwriter.Workbook): The workbook object.
        sheet (str): Name of the new worksheet.

        Returns:
        xlsxwriter.Workbook.worksheet: The created worksheet object.
        """
        if not self.workbook:
            raise ValueError("Workbook must be created before adding a worksheet.")
        worksheet = self.workbook.add_worksheet(sheet_name)
        return worksheet

    def write_data_to_excel(self, file_name, sheet_name, row, col, headers, data):
        """
        Writes data to an Excel file, including headers and data rows.

        Parameters:
        file_name (str): The name of the Excel file to create.
        data (list): A list of dictionaries containing the data to write.

        Returns:
        None
        """
        # Create a workbook and add a worksheet
        self.createWorkbook()
        worksheet = self.createWorksheet(sheet_name)

        # Write the column headers
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Write the data rows
        for row_num, row_data in enumerate(data, start=1):
            for col_num, cell_data in enumerate(row_data):
                worksheet.write(row_num, col_num, cell_data)

        # Close the workbook
        self.closeWorkbook()
