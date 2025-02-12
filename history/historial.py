from tkinter import messagebox
import os
import time

class Historial:
    def __init__(self, master):
        self.master = master
        self.history_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "History")
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

    def show_history(self):
        history_file = os.path.join(self.history_dir, f"{self.master.player_name}.txt")
        if os.path.exists(history_file):
            with open(history_file, "r") as file:
                history = file.read()
            messagebox.showinfo(f"Historial de '{self.master.player_name}'", history)
        else:
            messagebox.showinfo("Historial", f"No hay historial disponible para '{self.master.player_name}'.")

    def save_score(self):
        """Guarda el puntaje del jugador en un archivo de texto."""
        elapsed_time = int(time.time() - self.master.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        score = f"Nivel: {self.master.level} \n Movimientos: {self.master.moves}\n Tiempo: {minutes}:{seconds:02d}"

        filename = os.path.join(self.history_dir, f"{self.master.player_name}.txt")
        with open(filename, "a") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} \n- {score}\n\n")