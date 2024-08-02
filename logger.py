from abc import ABC, abstractmethod

class LogHandler(ABC):
    @abstractmethod
    def log(self, message, level):
        pass

class ConsoleLogAdapter(LogHandler):
    def log(self, message, level):
        print(f"[{level.upper()}] {message}")

class FileLogAdapter(LogHandler):
    def __init__(self, filename):
        self.filename = filename

    def log(self, message, level):
        with open(self.filename, 'a') as file:
            file.write(f"[{level.upper()}] {message}\n")

class Observer(ABC):
    @abstractmethod
    def update(self, message, level):
        pass

class ErrorObserver(Observer):
    def update(self, message, level):
        if level == "error":
            with open("/home/krish/patterns/error_warninglog.txt", 'a') as file:
                file.write(f"[{level.upper()}] {message}\n")

class WarningObserver(Observer):
    def update(self, message, level):
        if level == "warning":
            with open("/home/krish/patterns/error_warninglog.txt", 'a') as file:
                file.write(f"[{level.upper()}] {message}\n")

class UIObserver(Observer):
    def __init__(self):
        self.logs = []

    def update(self, message, level):
        if level in ["info", "update", "warning"]:
            self.logs.append((message, level))

    def get_logs(self):
        return self.logs

class Logger:
    _instance = None

    def __init__(self):
        self.handler = None
        self.levels = {"info": 1, "update": 2, "warning": 3, "error": 4}
        self.current_level = 1  # Default to INFO level
        self.observers = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_handler(self, handler):
        self.handler = handler

    def set_log_level(self, level):
        if level == "all":
            self.current_level = 0  # Log all messages
        else:
            self.current_level = self.levels.get(level, 1)  # Default to INFO level

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message, level):
        for observer in self.observers:
            observer.update(message, level)

    def _log(self, message, level):
        if self.handler and (self.current_level == 0 or self.levels.get(level, 1) >= self.current_level):
            self.handler.log(message, level)
            self.notify_observers(message, level)

    def info(self, message):
        self._log(message, "info")

    def update(self, message):
        self._log(message, "update")

    def warning(self, message):
        self._log(message, "warning")

    def error(self, message):
        self._log(message, "error")
