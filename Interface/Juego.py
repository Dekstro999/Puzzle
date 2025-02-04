from History.Historial import Historial
import customtkinter as ctk
import tkinter as tk
import random
import time

class Juego:
    def __init__(self, master):
        self.master = master
        self.historial = Historial(master)

    def create_main_menu(self):
        if not self.master.mezclando:
            for widget in self.master.winfo_children():
                widget.destroy()
            self.master.space(1)
            
            for level in range(1, 4):
                button = ctk.CTkButton(self.master, text=f"Nivel {level}", command=lambda l=level: self.start_level(l), font=("OCR A Extended", 50))
                button.pack(pady=20)
            self.master.history_button = ctk.CTkButton(self.master, text="Mostrar Historial", command=self.master.historial.show_history, font=("OCR A Extended", 50))
            self.master.history_button.pack(pady=30)

            self.master.bind("<Escape>", lambda event: self.master.confirm_exit())
            self.master.bind("<BackSpace>", lambda event: self.master.menu.create_menu_widgets())
            
            self.master.create_close_button()
            self.master.create_back_button(self.master.menu.create_menu_widgets)

    def start_level(self, grid_size):
        self.master.level = grid_size
        self.master.grid_size = grid_size + 3
        self.master.shuffle_num = 100 * grid_size
        self.master.percentage_points = {
            1: "5",
            int(self.master.shuffle_num * 0.2): "4",
            int(self.master.shuffle_num * 0.4): "3",
            int(self.master.shuffle_num * 0.6): "2",
            int(self.master.shuffle_num * 0.8): "1",
            int(self.master.shuffle_num * 0.9): "¡Vamos!"
        }
        self.create_game_widgets()
        self.master.start_shuffle_thread()

    def create_game_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.board_frame = ctk.CTkFrame(self.master, width=400, height=400)
        self.master.board_frame.pack(pady=20)

        self.master.tiles = [[None for _ in range(self.master.grid_size)] for _ in range(self.master.grid_size)]
        self.master.text_vars = [[tk.StringVar() for _ in range(self.master.grid_size)] for _ in range(self.master.grid_size)]
        for row in range(self.master.grid_size):
            for col in range(self.master.grid_size):
                text_var = self.master.text_vars[row][col]
                tile = ctk.CTkButton(
                    self.master.board_frame,
                    textvariable=text_var,
                    width=80,
                    height=80,
                    font=("Arial Black", 30, "bold"),
                    command=lambda r=row, c=col: self.move_tile(r, c),
                )
                tile.grid(row=row, column=col, padx=5, pady=5)
                self.master.tiles[row][col] = tile

        self.master.shuffle_button = ctk.CTkButton(self.master, textvariable=self.master.text_shuffled, command=self.master.start_shuffle_thread)
        self.master.shuffle_button.pack(pady=10)
        self.master.create_close_button()
        self.master.create_back_button(self.master.confirm_return_to_menu)

        self.master.moves_label = ctk.CTkLabel(self.master, text="Movimientos: 0", font=("OCR A Extended", 16))
        self.master.moves_label.pack()

        self.master.time_label = ctk.CTkLabel(self.master, text="Tiempo: 0s", font=("OCR A Extended", 16), text_color='#157227', fg_color='black', corner_radius=20)
        self.master.time_label.pack()

        self.master._5_Go = ctk.CTkLabel(self.master, 
            textvariable=tk.StringVar(value=""), 
            font=("OCR A Extended", 100),
        )

        self.master._5_Go.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.master.loading_label = ctk.CTkLabel(self.master, text="")
        self.master.loading_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
        self.master.bind("<Escape>", lambda event: self.master.confirm_exit())
        self.master.bind("<BackSpace>", lambda event: self.master.confirm_return_to_menu())

        self.update_time()

    def move_tile(self, row, col, update_moves=True):
        if self.master.is_adjacent(row, col, *self.master.empty_tile):
            empty_row, empty_col = self.master.empty_tile

            self.master.text_vars[empty_row][empty_col].set(self.master.text_vars[row][col].get())
            self.master.text_vars[row][col].set(" ")

            self.master.update_tile_color(empty_row, empty_col)
            self.master.update_tile_color(row, col)

            self.master.empty_tile = (row, col)

            if update_moves:
                self.master.moves += 1
                self.master.moves_label.configure(text=f"Movimientos: {self.master.moves}")

            if not self.master.mezclando:
                if self.master.check_win():
                    self.historial.save_score()
                    self.master.message_win()

    def update_time(self):
        if hasattr(self.master, 'time_label') and self.master.time_label.winfo_exists():
            elapsed_time = int(time.time() - self.master.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            if self.master.paused_time:
                self.master.time_label.configure(text=f"Tiempo: {minutes}:{seconds:02d} (Pausado)")
            else:
                self.master.time_label.configure(text=f"Tiempo: {minutes}:{seconds:02d}")
                self.master.after(1000, self.update_time)

    def shuffle_tiles(self):
        """Mezcla las fichas realizando movimientos válidos."""
        self.master.text_shuffled.set("Mezclando...")
        self.master.update_idletasks()

        self.master.start_loading_animation()

        self.master.mezclando = True
        
        self.master._5_Go.configure(textvariable=tk.StringVar(value=self.master.percentage_points[1]))
        self.master.update_idletasks()
        numbers = list(range(1, self.master.grid_size * self.master.grid_size))
        numbers.append(" ")

        for row in range(self.master.grid_size):
            for col in range(self.master.grid_size):
                number = numbers.pop(0)
                self.master.text_vars[row][col].set(str(number) if number != " " else " ")
                self.master.update_tile_color(row, col)
                if number == " ":
                    self.master.empty_tile = (row, col)

        for i in range(self.master.shuffle_num):
            row, col = self.master.empty_tile
            possible_moves = []
            if row > 0: possible_moves.append((row - 1, col))
            if row < self.master.grid_size - 1: possible_moves.append((row + 1, col))
            if col > 0: possible_moves.append((row, col - 1))
            if col < self.master.grid_size - 1: possible_moves.append((row, col + 1))
            target = random.choice(possible_moves)
            self.move_tile(*target, update_moves=False)
            self.master.time_label.configure(text=f"Tiempo: 0:00")

            if i in self.master.percentage_points:
                self.master._5_Go.configure(textvariable=tk.StringVar(value=self.master.percentage_points[i]))
                self.master.update_idletasks()
            
        self.master._5_Go.configure(textvariable=tk.StringVar(value="")) 
        self.master.mezclando = False
        self.master.text_shuffled.set("Mezclar")
        self.master.moves = 0
        self.master.moves_label.configure(text="Movimientos: 0")
        self.master.start_time = time.time()
        self.master.stop_loading_animation()