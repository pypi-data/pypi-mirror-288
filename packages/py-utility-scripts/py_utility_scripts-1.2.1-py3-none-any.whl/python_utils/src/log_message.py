"""
This script provides a flexible logging mechanism that supports logging messages 
with dynamic log levels to both the console and a log file in JSON format. 
It also includes log file rotation to manage log file size.

Classes:
- Logger: Handles the creation, rotation, and logging of messages to the console 
  and a log file. It supports dynamic log levels that can be added or removed.

Usage:
- Create an instance of the Logger class with the desired log file path and maximum log file size.
- Use the add_log_level method to add new log levels.
- Call the log method with a message and a specific log level to log messages.
- The Logger class will automatically handle log file creation and rotation.

Note:
- Ensure the log file path is correctly set to the desired log file location.
- The log messages are written in JSON format to facilitate easy parsing.
"""

import json
from datetime import datetime
from pathlib import Path

# Constants for log levels
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

class Logger:
    """
    A class to handle logging messages to the console and a log file in JSON format.
    
    Attributes:
    log_file (str): Path to the log file.
    max_log_size (int): Maximum size of the log file before rotation (in bytes).
    log_levels (set): A set of log levels that are supported for logging.

    Methods:
    create_log_file(): Ensures the log file exists.
    rotate_log_file(): Rotates the log file when its size exceeds the maximum allowed size.
    log(message: str, level: str): Logs messages with a timestamp and a specific log level.
    add_log_level(level: str): Adds a new log level to the set of supported log levels.
    remove_log_level(level: str): Removes a log level from the set of supported log levels.
    """

    def __init__(self, log_file="logs/application.log", max_log_size=5 * 1024 * 1024):
        """
        Initializes the Logger with the log file path and maximum log file size.

        Parameters:
        log_file (str): Path to the log file.
        max_log_size (int): Maximum size of the log file before rotation (in bytes).
        """
        self.log_file = log_file
        self.max_log_size = max_log_size
        self.log_levels = {INFO, WARNING, ERROR}
        self.create_log_file()

    def create_log_file(self):
        """
        Ensures the log file exists.

        This function checks if the log file specified by log_file exists. 
        If it does not, the function creates an empty log file.
        
        Returns:
            None
        """
        if not Path(self.log_file).exists():
            Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, "x") as file:
                file.close()

    def rotate_log_file(self):
        """
        Rotates the log file when its size exceeds the maximum allowed size.

        This function checks if the current log file exceeds the predefined maximum
        size. If it does, the function renames the current log file to include
        a timestamp in its name and retains it as an old log file. The timestamp
        format used is 'YYYYMMDD_HHMMSS' to ensure uniqueness and chronological
        sorting of old log files.

        The log file is renamed with the format: 'YYYYMMDD_HHMMSS-application.log'.

        Returns:
            None
        """
        if Path(self.log_file).exists() and Path(self.log_file).stat().st_size > self.max_log_size:
            # Generate a timestamp for the old log file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_log_file_name = f"{timestamp}-{Path(self.log_file).name}"
            
            # Rotate the log file
            Path(self.log_file).rename(Path(self.log_file).parent / new_log_file_name)

    def log(self, message: str, level: str) -> None:
        """
        Logs messages with a timestamp and a specific log level.
        Supports logging to both the console and a file in JSON format.

        Args:
            message (str): The message to log.
            level (str): The log level (e.g., INFO, WARNING, ERROR).
        
        Returns:
            None

        Raises:
            ValueError: If the log level is not in the set of supported log levels.
        """
        if level not in self.log_levels:
            raise ValueError(f"Log level '{level}' is not supported. Available levels: {self.log_levels}")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        log_message_str = json.dumps(log_message)
        
        # Print log message to the console
        print(f"{timestamp} [{level}] {message}")
        
        # Rotate log file if necessary
        self.rotate_log_file()
        self.create_log_file()

        # Write log message to the log file
        with open(self.log_file, "a") as log_file:
            log_file.write(log_message_str + "\n")

    def add_log_level(self, level: str) -> None:
        """
        Adds a new log level to the set of supported log levels.

        Args:
            level (str): The log level to add.

        Returns:
            None
        """
        self.log_levels.add(level)

    def remove_log_level(self, level: str) -> None:
        """
        Removes a log level from the set of supported log levels.

        Args:
            level (str): The log level to remove.

        Returns:
            None

        Raises:
            KeyError: If the log level to remove does not exist in the set of supported log levels.
        """
        if level in self.log_levels:
            self.log_levels.remove(level)
        else:
            raise KeyError(f"Log level '{level}' not found in the set of supported log levels.")