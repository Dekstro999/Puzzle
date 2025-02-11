from observer import Observer

class GameObserver(Observer):
    def __init__(self, juego_puzzle):
        self.juego_puzzle = juego_puzzle
        # self.juego_puzzle.add_observer(self)

    def on_time_updated(self, elapsed_time):
        # Actualiza la interfaz de usuario con el tiempo transcurrido
        print(f"Tiempo actualizado: {elapsed_time} segundos")

    def on_moves_updated(self, moves):
        # Actualiza la interfaz de usuario con los movimientos realizados
        print(f"Movimientos actualizados: {moves}")