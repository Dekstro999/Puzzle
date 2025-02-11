from observer import Observer

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_time_updated(self, elapsed_time):
        for observer in self._observers:
            observer.on_time_updated(elapsed_time)

    def notify_moves_updated(self, moves):
        for observer in self._observers:
            observer.on_moves_updated(moves)