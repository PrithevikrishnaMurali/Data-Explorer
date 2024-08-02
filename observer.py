class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, level, message):
        for observer in self._observers:
            observer.update(message, level)

class GeneralObserver:
    def update(self, message, level):
        print(f"[{level.upper()}] {message}")
