import pytest
from main import JuegoPuzzle
from GameObserver import GameObserver

class MockObserver:
    def __init__(self):
        self.time_updated = False
        self.moves_updated = False

    def on_time_updated(self, elapsed_time):
        self.time_updated = True

    def on_moves_updated(self, moves):
        self.moves_updated = True

@pytest.fixture
def juego_puzzle():
    return JuegoPuzzle()

def test_observer_notified(juego_puzzle):
    mock_observer = MockObserver()
    juego_puzzle.add_observer(mock_observer)

    # Simula una actualización de tiempo
    juego_puzzle.notify_time_updated(100)
    assert mock_observer.time_updated == True

    # Simula una actualización de movimientos
    juego_puzzle.notify_moves_updated(10)
    assert mock_observer.moves_updated == True