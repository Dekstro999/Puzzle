from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event, *args, **kwargs):
        pass