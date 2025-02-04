import customtkinter as ctk
from tkinter import messagebox

class Menu:
    def __init__(self, master):
        self.master = master

    def create_menu_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.welcome_label = ctk.CTkLabel(self.master, text="Bienvenido al \nPuzzle Deslizante", font=("OCR A Extended", 70))
        self.master.welcome_label.pack(pady=20)
        self.master.space(1)
        self.master.name_entry = ctk.CTkEntry(self.master, width=600, font=("OCR A Extended", 50), justify="center")
        self.master.name_entry.pack(pady=10)
        self.master.name_entry.insert(0, ">Ingrese su nombre<")
        self.master.name_entry.bind("<FocusIn>", self.on_entry_click)
        self.master.name_entry.bind("<FocusOut>", self.on_focus_out)
        self.master.name_entry.bind("<KeyRelease>", self.check_name_length)

        self.master.error_label = ctk.CTkLabel(self.master, text="", font=("OCR A Extended", 16), text_color="red")
        self.master.error_label.pack(pady=5)

        self.master.start_button = ctk.CTkButton(self.master, 
                                                text="ENTRAR", 
                                                command=self.start_game, 
                                                font=("OCR A Extended", 36, 'bold'), 
                                                width=200,
                                                height=50,
                                                corner_radius=20,
                                                fg_color='#157227', 
                                                hover_color='#1f9d2d', 
                                                text_color='black')
        self.master.start_button.pack(pady=20)

        self.master.bind("<Return>", lambda event: self.start_game())
        self.master.bind("<Escape>", lambda event: self.master.confirm_exit())

    def on_entry_click(self, event):
        if self.master.name_entry.get() == ">Ingrese su nombre<":
            self.master.name_entry.delete(0, "end")

    def on_focus_out(self, event):
        if self.master.name_entry.get() == "":
            self.master.name_entry.insert(0, ">Ingrese su nombre<")

    def check_name_length(self, event):
        if len(self.master.name_entry.get()) > 17:
            self.master.error_label.configure(text="Máximo 17 caracteres")
        else:
            self.master.error_label.configure(text="")

    def start_game(self):
        self.master.player_name = self.master.name_entry.get()
        if self.master.player_name:
            self.master.juego.create_main_menu()
        else:
            messagebox.showerror("Error", "Por favor, ingrese su nombre.")
