from gui.menu import Menu
from gui.juego import Juego
from history.historial import Historial
import customtkinter as ctk
from customtkinter import CTkImage
import tkinter as tk
from tkinter import messagebox
import time
import os
from PIL import Image
import threading

class Game(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Puzzle Deslizante")
        self.geometry("750x750")
        self.resizable(False, False)

        self.player_name = None
        self.grid_size = 4
        self.empty_tile = (self.grid_size - 1, self.grid_size - 1)
        self.tiles = []
        self.text_vars = []
        self.level = 1
        self.text_shuffled = tk.StringVar(value="Mezclar")
        self.moves = 0
        self.start_time = time.time()
        self.paused_time = 0
        self.mezclando = False
        self.shuffle_num = 100  
        self.percentage_points = {
            1: "5",
            int(self.shuffle_num * 0.2): "4",
            int(self.shuffle_num * 0.4): "3",
            int(self.shuffle_num * 0.6): "2",
            int(self.shuffle_num * 0.8): "1",
            int(self.shuffle_num * 0.9): "¡Vamos!"
        }

        self.sprites = []
        for i in range(8):
            file_path = os.path.join(os.path.dirname(__file__), f"assets/Frame_loading_{i}.png")
            if os.path.exists(file_path):
                image = Image.open(file_path)
                ctk_image = CTkImage(image, size=(80, 80))  
                self.sprites.append(ctk_image)
            else:
                print(f"Error: No se pudo cargar {file_path}")

        self.sprite_index = 0

        self.menu = Menu(self)
        self.juego = Juego(self)
        self.historial = Historial(self)

        self.menu.create_menu_widgets()

    def space(self, n):
        self.space_label = ctk.CTkLabel(self, text="")
        self.space_label.pack(pady=n*10)

    def confirm_exit(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.quit()

    def confirm_return_to_menu(self):
        self.paused_time = time.time() - self.start_time  # Pausar el tiempo
        
        if messagebox.askokcancel("Regresar al menú", "¿Estás seguro de que quieres regresar al menú? \nTu progreso no se guardará."):
            self.juego.create_main_menu()
        else:
            self.start_time = time.time() - self.paused_time  # Reanudar el tiempo
            self.paused_time = 0
            self.juego.update_time()

    def create_close_button(self):
        self.close_button = ctk.CTkButton(self, text="Cerrar", command=self.confirm_exit, font=("OCR A Extended", 25), fg_color='#9f0000', hover_color='#ff0000')
        self.close_button.place(relx=0.99, rely=0.99, anchor=tk.SE)

    def create_back_button(self, comando):
        self.back_button = ctk.CTkButton(self, text="Regresar", command=comando, font=("OCR A Extended", 25))
        self.back_button.place(relx=0.01, rely=0.99, anchor=tk.SW)

    def start_shuffle_thread(self):
        """Inicia un hilo separado para mezclar las fichas."""
        if not self.mezclando:  
            shuffle_thread = threading.Thread(target=self.juego.shuffle_tiles)
            self.mezclando = True
            shuffle_thread.start()

    def update_tile_color(self, row, col):
        """Actualiza el color de la ficha según su texto."""
        if self.text_vars[row][col].get() == " ":
            self.tiles[row][col].configure(fg_color=self.board_frame.cget("fg_color"), hover_color=self.board_frame.cget("fg_color"))
        else:
            self.tiles[row][col].configure(fg_color='#02458a', hover_color='#025d8a')

    def is_adjacent(self, row1, col1, row2, col2):
        """Comprueba si dos celdas son adyacentes."""
        return abs(row1 - row2) + abs(col1 - col2) == 1

    def check_win(self):
        """Comprueba si las fichas están ordenadas correctamente."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) != self.empty_tile:
                    expected_num = row * self.grid_size + col + 1
                    if self.text_vars[row][col].get() != str(expected_num):
                        return False
        return True

    def message_win(self):
        result = messagebox.askquestion("¡Ganaste!", "¡Felicidades! Completaste el puzzle.\n¿Quieres volver a jugar?", icon='info')
        if result == 'yes':
            self.juego.shuffle_tiles()
        else:
            self.quit()


    def start_loading_animation(self):
        """Inicia la animación de carga."""
        if self.mezclando:
            if self.sprites:
                self.loading_label.configure(image=self.sprites[self.sprite_index])
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                self.loading_label.after(70, self.start_loading_animation)

    def stop_loading_animation(self):
        """Detiene la animación de carga."""
        self.mezclando = False
        empty_image = CTkImage(Image.new('RGBA', (1, 1), (0, 0, 0, 0)), size=(1, 1))
        self.loading_label.configure(image=empty_image)
        self.sprite_index = 0

if __name__ == "__main__":
    app = Game()
    app.mainloop()