import unittest
import os
from app.python_utils.src.log_message import Logger

# Constants for log levels
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

class TestLogFunctions(unittest.TestCase):
    """
    Unit test class for testing Logger functionality.
    
    Methods:
    test_log_message(): Tests logging messages with various log levels and log level management.
    """

    def setUp(self):
        """
        Set up the test environment.
        
        Initializes the Logger instance and prepares the log file path for testing.
        """
        self.log_file = 'app/python_utils/src/local_test/test_log.log'
        self.logger = Logger(log_file=self.log_file)

    def tearDown(self):
        """
        Clean up after tests.
        
        Removes the log file created during the test to avoid residual files.
        """
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_log_message(self):
        """
        Tests logging messages with different log levels and log level management.
        
        This test:
        - Logs messages with predefined log levels (INFO, WARNING, ERROR).
        - Adds a new log level and logs a message with it.
        - Removes an existing log level and verifies its removal.
        
        Assertions:
        - Check if the log file is created and contains messages.
        - Ensure the log messages match the expected format.
        """
        # Log messages with different log levels
        self.logger.log("This is an info message.", INFO)
        self.logger.log("This is a warning message.", WARNING)
        self.logger.log("This is an error message.", ERROR)

        # Check if the log file exists and contains logged messages
        self.assertTrue(os.path.exists(self.log_file), "Log file does not exist.")
        
        with open(self.log_file, 'r') as file:
            log_contents = file.readlines()

        # Verify log contents for INFO message
        self.assertTrue(any(INFO in line for line in log_contents), "INFO log message not found in log file.")
        # Verify log contents for WARNING message
        self.assertTrue(any(WARNING in line for line in log_contents), "WARNING log message not found in log file.")
        # Verify log contents for ERROR message
        self.assertTrue(any(ERROR in line for line in log_contents), "ERROR log message not found in log file.")

        # Add a new log level and log a message with it
        self.logger.add_log_level("DEBUG")
        self.logger.log("This is a debug message.", "DEBUG")
        
        # Check if the DEBUG message is written to the log file
        with open(self.log_file, 'r') as file:
            log_contents = file.readlines()

        self.assertTrue(any("DEBUG" in line for line in log_contents), "DEBUG log message not found in log file.")

        # Remove an existing log level
        self.logger.remove_log_level("DEBUG")
        
        # Check if DEBUG log level has been removed
        with self.assertRaises(ValueError):
            self.logger.log("This should raise an error.", "DEBUG")
        
        print('====================Log Message Test Successful.====================')

if __name__ == '__main__':
    unittest.main()
