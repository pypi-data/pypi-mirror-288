"""
Module: functions.py
Description: Provides utility classes and functions for managing database operations and middleware in a FastAPI application.

This module includes:

1. **LoggingMiddleware**: Middleware for logging HTTP request and response details, including method, URL, headers, and status codes.

2. **Settings**: A configuration class that uses Pydantic's BaseSettings to load environment variables for MySQL database configuration.

3. **SqlConnection**: Manages MySQL database connections using a connection pool with retry mechanisms for robustness. It includes methods to create a connection pool and retrieve a connection with retry logic.

4. **SqlResponse**: Handles the structure and formatting of SQL operation responses. It provides methods to format successful and error responses for SQL operations.

5. **SqlExecution**: Provides methods for executing SQL queries and transactions. It includes methods to execute single queries and manage transactions, returning responses formatted with success status and error messages if applicable.

6. **SqlHandler**: A class that executes asynchronous functions with standard exception handling. It formats responses for both successful operations and errors, using the SqlResponse class to ensure consistent response formatting.

Imports:
- `json`, `time`, `datetime`: Standard libraries for JSON handling, time management, and date-time operations.
- `pydantic_settings.BaseSettings`: For loading configuration from environment variables.
- `mysql.connector`, `mysql.connector.pooling`: For MySQL database connection and pooling.
- `fastapi.Request`, `fastapi.status`, `fastapi.HTTPException`, `fastapi.responses.JSONResponse`: For handling HTTP requests, responses, and exceptions in FastAPI.
- `starlette.middleware.base.BaseHTTPMiddleware`: For creating custom middleware in FastAPI.
- `typing.Dict`, `typing.Any`, `typing.Optional`, `typing.Callable`: For type hints and annotations.

Note:
- Ensure that environment variables for database configuration are set in the `.env` file as specified in the Settings class.
- Logging is managed through the Logger class defined in `log_message.py`.
"""


import json
import time
from datetime import datetime
from pydantic_settings import BaseSettings
from pydantic import ValidationError, ConfigDict
import mysql.connector
from mysql.connector import Error
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional, Callable
from mysql.connector.pooling import MySQLConnectionPool
from starlette.middleware.base import BaseHTTPMiddleware
from .log_message import Logger

# Constants for log levels
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

# Initialize the logger
logger = Logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP request and response details.

    This middleware logs information about incoming HTTP requests and outgoing responses,
    including timestamp, method, URL, headers, and response status code.

    Methods:
        dispatch(request, call_next): Logs request and response details.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Log request details before processing and response details after processing.

        Args:
            request (Request): The incoming HTTP request object.
            call_next (callable): A callable to invoke the next middleware or route handler.

        Returns:
            Response: The HTTP response object.
        """
        # Log request details
        log_message = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers)
        }
        logger.log(message=json.dumps(log_message), level=INFO)

        # Process the request and get the response
        response = await call_next(request)

        # Log response details
        log_message = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status_code": response.status_code
        }
        logger.log(message=json.dumps(log_message), level=INFO)

        return response


class Settings(BaseSettings):
    """
    Configuration class for loading settings from environment variables.

    Uses Pydantic's BaseSettings to automatically load environment variables for database configuration.

    Attributes:
        MYSQL_PASSWORD (str): The root password for MySQL.
        MYSQL_DATABASE (str): The name of the MySQL database.
        MYSQL_USER (str): The MySQL user.
        MYSQL_HOST (str): The MySQL host.
        MYSQL_PORT (int): The port for MySQL connection.

    Config:
        env_file (str): Specifies the environment file to load settings from.
    """

    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_HOST: str
    MYSQL_PORT: int

    @classmethod
    def config(cls) -> ConfigDict:
        return ConfigDict(env_file=".env")


class SqlConnection:
    """
    Manages MySQL database connections using a connection pool.

    Provides methods to create a connection pool and retrieve a connection from the pool
    with retry mechanisms for robustness.

    Attributes:
        retries (int): Number of retry attempts for pool creation and connection acquisition.
        pool_name (str): Name of the connection pool.
        pool_size (int): Size of the connection pool.
        timeout (int): Timeout for establishing a database connection.

    Methods:
        create_connection_pool(): Creates a MySQL connection pool with retries.
        get_db_connection(): Retrieves a MySQL database connection from the pool with retries.
    """

    def __init__(self, retries=3, pool_name='My_App_Pool', pool_size=10, timeout=300):
        """
        Initialize the SqlConnection with specified parameters.

        Args:
            retries (int, optional): Number of retry attempts. Defaults to 3.
            pool_name (str, optional): Name of the connection pool. Defaults to 'My_App_Pool'.
            pool_size (int, optional): Number of connections in the pool. Defaults to 10.
            timeout (int, optional): Timeout for establishing a database connection. Defaults to 300.
        """
        self.retries = retries
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.timeout = timeout
        self.connection_pool = self.create_connection_pool()  # Initialize the connection pool

    def create_connection_pool(self) -> MySQLConnectionPool:
        """
        Create a MySQL connection pool with retry logic.

        Attempts to create a MySQL connection pool with specified settings. Retries if an error occurs.

        Returns:
            MySQLConnectionPool: A pool of MySQL connections.

        Raises:
            HTTPException: If the connection pool cannot be created after retries.
        """
        # Initialize settings from environment variables
        try:
            settings = Settings()
        except ValidationError as e:
            # Log the detailed validation error for debugging
            print(f"Error loading settings: {e}")

            # Provide a user-friendly error message
            print("Failed to load environment variables. Please check your .env file for correctness.")
            print("""
                Sample .env file is,
                  
                MYSQL_PASSWORD: str
                MYSQL_DATABASE: str
                MYSQL_USER: str
                MYSQL_HOST: str
                MYSQL_PORT: int
            """)

            # Optionally, you can provide fallback values or exit the application
            # For example, you can exit with a specific status code
            exit(1)

        for attempt in range(self.retries):
            try:
                logger.log("Creating connection pool...", INFO)
                return MySQLConnectionPool(
                    pool_name=self.pool_name,
                    pool_size=self.pool_size,
                    pool_reset_session=True,
                    host=settings.MYSQL_HOST,
                    user=settings.MYSQL_USER,
                    password=settings.MYSQL_PASSWORD,
                    database=settings.MYSQL_DATABASE,
                    port=settings.MYSQL_PORT,
                    connection_timeout=self.timeout
                )
            except Error as err:
                logger.log(f"Attempt {attempt + 1}: Error creating connection pool: {err}", ERROR)
                if attempt + 1 == self.retries:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Database connection pool creation error"
                    )
                time.sleep(2)  # Wait before retrying

    def get_db_connection(self) -> mysql.connector.MySQLConnection:
        """
        Retrieve a MySQL database connection from the pool with retry logic.

        Attempts to acquire a connection from the pool. Retries if an error occurs or no connection is available.

        Returns:
            MySQLConnection: A MySQL database connection.

        Raises:
            HTTPException: If a connection cannot be acquired after retries.
        """
        for attempt in range(self.retries):
            try:
                connection = self.connection_pool.get_connection()
                if connection.is_connected():
                    logger.log("SQL Connection Successful", INFO)
                    return connection
            except Error as err:
                logger.log(f"Attempt {attempt + 1}: Error getting connection: {err}", ERROR)
                if attempt + 1 == self.retries:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Database connection error"
                    )
                time.sleep(2)  # Wait before retrying


class SqlResponse:
    """
    Handles the structure and formatting of SQL operation responses.

    Attributes:
        success (bool): Indicates if the operation was successful.
        result (Any): The result data to be included in the response.
        status_code (int): The HTTP status code of the response.
        response (JSONResponse): The JSON response object.
        error (Optional[str]): An optional error message if the operation failed.

    Methods:
        format_response(): Formats the JSON response for successful operations.
        format_error_response(e): Formats the error response for HTTP exceptions.
    """

    def __init__(self, success: bool, result: Any, status_code: int, response: JSONResponse, 
                 error: Optional[str] = None):
        """
        Initialize the SqlResponse with the provided parameters.

        Args:
            success (bool): Indicates if the operation was successful.
            result (Any): The result data to be included in the response.
            status_code (int): The HTTP status code of the response.
            response (JSONResponse): The JSON response object.
            error (Optional[str], optional): An optional error message if the operation failed. Defaults to None.
        """
        self.success = success
        self.result = result
        self.status_code = status_code
        self.response = response
        self.error = error

    def format_response(self) -> Dict[str, Any]:
        """
        Format the JSON response for successful operations.

        Returns:
            Dict[str, Any]: The formatted JSON response with success status, result, headers, and optional error message.
        """

        # Create response headers dynamically
        headers = {
            "Content-Length": str(len(str(self.result))),
            "Content-Type": self.response.headers.get("content-type", "application/json"),
            "Date": self.response.headers.get("date"),
            "Server": self.response.headers.get("server", "uvicorn")
        }

        # Create final response format
        formatted_response = {
            "success": self.success,
            "result": {
                "statusCode": self.status_code,
                "headers": headers,
                "body": self.result
            },
            "error": self.error
        }

        return formatted_response

    def format_error_response(self, e: Exception) -> JSONResponse:
        """
        Format the error response for HTTP exceptions.

        Args:
            e (Exception): The exception object containing the error details.

        Returns:
            JSONResponse: A JSON response containing the error details including message and status code.
        """
        # Determine status code from the exception or default to 500
        status_code = getattr(e, 'status_code', 500)
        
        # Extract error message from the exception
        message = str(e.detail) if hasattr(e, 'detail') else str(e)
        
        # Create and return the JSON response with error details
        return JSONResponse(
            content={"message": message},
            status_code=status_code
        )


class SqlExecution:
    """
    Handles the execution of SQL queries and transactions.

    Provides methods for executing single SQL statements and managing database transactions.

    Methods:
        execute_single_query(query: str, params: Optional[Dict[str, Any]] = None): Executes a single SQL query.
        execute_transaction(queries: Dict[str, str], params: Optional[Dict[str, Any]] = None): Executes multiple SQL queries within a transaction.
    """

    @staticmethod
    def execute_single_query(db_conn, query: str, params: Optional[Dict[str, Any]] = None) -> SqlResponse:
        """
        Execute a single SQL query and return a formatted JSON response.

        Args:
            query (str): The SQL query to be executed.
            params (Optional[Dict[str, Any]], optional): Parameters for the SQL query. Defaults to None.

        Returns:
            SqlResponse: The response object containing the success status, result, and optional error message.
        """
        try:
            connection = db_conn
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            sql_response = SqlResponse(
                success=True,
                result=result,
                status_code=status.HTTP_200_OK,
                response=JSONResponse(content={"result": result}),
            )
            return sql_response.format_response()
        except Error as e:
            sql_response = SqlResponse(
                success=False,
                result={},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response=JSONResponse(content={"message": str(e)}),
                error=str(e)
            )
            return sql_response.format_response()

    @staticmethod
    def execute_transaction(db_conn, queries: Dict[str, str], params: Optional[Dict[str, Any]] = None) -> SqlResponse:
        """
        Execute multiple SQL queries within a transaction and return a formatted JSON response.

        Args:
            queries (Dict[str, str]): Dictionary containing SQL queries to be executed.
            params (Optional[Dict[str, Any]], optional): Parameters for the SQL queries. Defaults to None.

        Returns:
            SqlResponse: The response object containing the success status, result, and optional error message.
        """
        try:
            connection = db_conn
            cursor = connection.cursor(dictionary=True)
            for query in queries.values():
                cursor.execute(query, params or ())
            connection.commit()
            cursor.close()
            connection.close()
            sql_response = SqlResponse(
                success=True,
                result={"message": "Transaction successful"},
                status_code=status.HTTP_200_OK,
                response=JSONResponse(content={"message": "Transaction successful"}),
            )
            return sql_response.format_response()
        except Error as e:
            sql_response = SqlResponse(
                success=False,
                result={},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response=JSONResponse(content={"message": str(e)}),
                error=str(e)
            )
            return sql_response.format_response()

class SqlHandler:
    """
    A class to handle SQL operations with standard exception handling.

    Methods:
        execute_with_handling(func, *args, **kwargs): Execute an asynchronous function with error handling.
    """
    @staticmethod
    async def execute_with_handling(func: Callable[..., Any], *args, **kwargs) -> JSONResponse:
        """
        Executes an asynchronous function with standard exception handling, formatting responses for both success and error scenarios.

        Args:
            func (Callable[..., Any]): The asynchronous function to execute.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            JSONResponse: A JSON response representing the result of the function or an error message.
        """
        try:
            # Attempt to execute the function and return its result
            result = await func(*args, **kwargs)
            return result
        except HTTPException as e:
            # Handle HTTP exceptions with specific formatting
            error_response = JSONResponse(
                content={"message": str(e.detail)},
                status_code=e.status_code
            )
            sql_response = SqlResponse(
                success=False,
                result=None,
                status_code=e.status_code,
                response=error_response,
                error=str(e.detail)
            )
            formatted_response = sql_response.format_response()
            return JSONResponse(content=formatted_response, status_code=e.status_code)
        except Exception as e:
            # Handle other exceptions with generic formatting
            error_response = JSONResponse(
                content={"message": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            sql_response = SqlResponse(
                success=False,
                result=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response=error_response,
                error=str(e)
            )
            formatted_response = sql_response.format_response()
            return JSONResponse(content=formatted_response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
