from observer import Observer

class GameObserver(Observer):
    def __init__(self, juego_puzzle):
        self.juego_puzzle = juego_puzzle

    def on_time_updated(self, elapsed_time):
        minutes, seconds = divmod(elapsed_time, 60)
        self.juego_puzzle.master.time_label.configure(text=f"Tiempo: {minutes}:{seconds:02d}")

    def on_moves_updated(self, moves):
        self.juego_puzzle.master.moves_label.configure(text=f"Movimientos: {moves}")