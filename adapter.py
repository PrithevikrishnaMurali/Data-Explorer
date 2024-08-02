from logger import LoggerOutputAdapter

class ConsoleLogAdapter(LoggerOutputAdapter):
    def write(self, message):
        print(message)

class FileLogAdapter(LoggerOutputAdapter):
    def __init__(self, filename):
        self.filename = filename

    def write(self, message):
        with open(self.filename, 'a') as file:
            file.write(message + '\n')
