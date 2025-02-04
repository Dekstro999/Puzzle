class GameObserver:
    def __init__(self, juego_puzzle):
        self.juego_puzzle = juego_puzzle
        self.juego_puzzle.add_observer(self)

    def update(self, event, *args):
        if event == 'time_updated':
            elapsed_time = args[0]
            # Actualiza la interfaz de usuario con el tiempo transcurrido
        elif event == 'moves_updated':
            moves = args[0]
            # Actualiza la interfaz de usuario con los movimientos realizados