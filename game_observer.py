from observer import Observer

class GameObserver(Observer):
    def __init__(self, juego_puzzle):
        self.juego_puzzle = juego_puzzle

    def on_time_updated(self, elapsed_time):
        print(f"Tiempo actualizado: {elapsed_time} segundos")

    def on_moves_updated(self, moves):
        print(f"Movimientos actualizados: {moves}")