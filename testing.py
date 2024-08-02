import unittest
from logger import Logger, ConsoleLogAdapter, FileLogAdapter, ErrorObserver, WarningObserver

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger.get_instance()
        self.logger.set_handler(ConsoleLogAdapter())
        self.error_observer = ErrorObserver()
        self.warning_observer = WarningObserver()
        self.logger.add_observer(self.error_observer)
        self.logger.add_observer(self.warning_observer)
        self.log_file = "/home/krish/patterns/log.txt"
        self.error_warning_log_file = "/home/krish/patterns/error_warninglog.txt"

    def tearDown(self):
        self.logger = None

    def test_info_log(self):
        self.logger.set_log_level("info")
        self.logger.info("Info log message")
        self.assertTrue(self.check_log_content(self.log_file, "INFO"))

    def test_warning_log(self):
        self.logger.set_log_level("warning")
        self.logger.warning("Warning log message")
        self.assertTrue(self.check_log_content(self.log_file, "WARNING"))
        self.assertTrue(self.check_log_content(self.error_warning_log_file, "WARNING"))

    def test_error_log(self):
        self.logger.set_log_level("error")
        self.logger.error("Error log message")
        self.assertTrue(self.check_log_content(self.log_file, "ERROR"))
        self.assertTrue(self.check_log_content(self.error_warning_log_file, "ERROR"))

    def check_log_content(self, file, level):
        with open(file, 'r') as log_file:
            content = log_file.read()
        return level in content

if __name__ == '__main__':
    unittest.main()
