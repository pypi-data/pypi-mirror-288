"""
Module: test_sql_functions.py
Description: Contains unit tests for the SqlHandler class in the sql_functions module. 

This module uses the unittest framework to test the behavior of the execute_with_handling method in the SqlHandler class. It includes tests for successful execution, HTTP exceptions, and generic exceptions.

Tests:
    - test_execute_with_handling_success: Verifies the correct handling of successful executions.
    - test_execute_with_handling_http_exception: Verifies the handling of HTTP exceptions.
    - test_execute_with_handling_generic_exception: Verifies the handling of generic exceptions.

Imports:
    - unittest: For creating and running unit tests.
    - asyncio: For running asynchronous tests.
    - AsyncMock: For mocking asynchronous functions.
    - fastapi.HTTPException: For simulating HTTP exceptions.
    - fastapi.status: For HTTP status codes.
    - fastapi.responses.JSONResponse: For simulating JSON responses.
    - app.python_utils.src.sql_functions.SqlHandler: The class being tested.
    - json: For handling JSON data.

Note:
    - Ensure that the SqlHandler class is correctly implemented and imported from the correct module path.
"""

import unittest
import asyncio
from unittest.mock import AsyncMock
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.python_utils.src.sql_functions import SqlHandler
import json

class TestSqlHandler(unittest.TestCase):
    """
    Unit test class for the SqlHandler class.

    This class contains test cases for the execute_with_handling method in the SqlHandler class.
    It includes tests for successful execution, HTTP exceptions, and generic exceptions.
    """

    def setUp(self):
        """
        Set up the test environment for SqlHandler.

        Initializes an instance of the SqlHandler class to be used in the test methods.
        """
        self.sql_handler = SqlHandler()

    async def async_test_execute_with_handling(self, mock_func, expected_status, expected_body):
        """
        Asynchronous helper method to test execute_with_handling.

        Executes the provided mock function using execute_with_handling and compares the result
        with the expected status and body.

        Args:
            mock_func (AsyncMock): The mock function to be tested.
            expected_status (int): The expected HTTP status code of the result.
            expected_body (str): The expected JSON body of the result.

        Asserts:
            The status code and body of the result against the expected values.
        """
        result = await self.sql_handler.execute_with_handling(mock_func)
        self.assertEqual(result.status_code, expected_status)
        # Decode bytes to string and load JSON for comparison
        actual_body = result.body.decode('utf-8')
        self.assertEqual(json.loads(actual_body), json.loads(expected_body))

    def test_execute_with_handling_success(self):
        """
        Test the execute_with_handling method for a successful execution.

        Mocks a successful function and verifies that execute_with_handling returns the correct
        status code and body for a successful operation.
        """
        mock_func = AsyncMock(return_value=JSONResponse(content={"success": True}, status_code=status.HTTP_200_OK))
        asyncio.run(self.async_test_execute_with_handling(mock_func, status.HTTP_200_OK, '{"success": true}'))

    def test_execute_with_handling_http_exception(self):
        """
        Test the execute_with_handling method for an HTTPException.

        Mocks an HTTPException and verifies that execute_with_handling returns the correct
        status code, body, and error message for an HTTP exception.
        """
        mock_func = AsyncMock(side_effect=HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request"))
        expected_response = {
            "success": False,
            "result": {
                "statusCode": 400,
                "headers": {
                    "Content-Length": "4",
                    "Content-Type": "application/json",
                    "Date": None,
                    "Server": "uvicorn"
                },
                "body": None
            },
            "error": "Bad Request"
        }
        expected_body = json.dumps(expected_response)
        asyncio.run(self.async_test_execute_with_handling(mock_func, status.HTTP_400_BAD_REQUEST, expected_body))

    def test_execute_with_handling_generic_exception(self):
        """
        Test the execute_with_handling method for a generic exception.

        Mocks a generic exception and verifies that execute_with_handling returns the correct
        status code, body, and error message for a generic exception.
        """
        mock_func = AsyncMock(side_effect=Exception("An unexpected error occurred"))
        expected_response = {
            "success": False,
            "result": {
                "statusCode": 500,
                "headers": {
                    "Content-Length": "4",
                    "Content-Type": "application/json",
                    "Date": None,
                    "Server": "uvicorn"
                },
                "body": None
            },
            "error": "An unexpected error occurred"
        }
        expected_body = json.dumps(expected_response)
        asyncio.run(self.async_test_execute_with_handling(mock_func, status.HTTP_500_INTERNAL_SERVER_ERROR, expected_body))

        print('====================SQL Function Test Successful.====================')

if __name__ == '__main__':
    unittest.main()
