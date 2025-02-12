from observer import Observer

class Observable:
    def __init__(self):
        self._observers : list[Observer]= []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify_observers(self, event, *args, **kwargs):
        for observer in self._observers:
            observer.update(event, *args, **kwargs)