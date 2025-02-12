from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def on_time_updated(self, elapsed_time):
        pass

    @abstractmethod
    def on_moves_updated(self, moves):
        pass