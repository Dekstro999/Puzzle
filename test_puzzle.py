import pytest
from unittest.mock import patch, MagicMock
from main import Game
import threading

@pytest.fixture
def juego():
    app = Game()
    yield app
    app.destroy()

def test_initial_state(juego):
    assert juego.moves == 0
    assert juego.grid_size == 4
    assert juego.empty_tile == (3, 3)
    assert juego.text_shuffled.get() == "Mezclar"

def test_confirm_exit(juego):
    with patch('tkinter.messagebox.askokcancel', return_value=True):
        juego.quit = MagicMock()
        juego.confirm_exit()
        assert juego.quit.called

def test_confirm_return_to_menu(juego):
    with patch('tkinter.messagebox.askokcancel', return_value=True):
        juego.juego.create_main_menu = MagicMock()
        juego.confirm_return_to_menu()
        assert juego.juego.create_main_menu.called

def test_start_shuffle_thread(juego):
    with patch('threading.Thread.start', MagicMock()):
        juego.start_shuffle_thread()
        assert juego.mezclando is True
        assert threading.Thread.start.called

def test_check_win(juego):
    # Inicializar text_vars con las dimensiones correctas
    juego.text_vars = [[MagicMock() for _ in range(juego.grid_size)] for _ in range(juego.grid_size)]
    
    # Configurar text_vars con los valores esperados
    for row in range(juego.grid_size):
        for col in range(juego.grid_size):
            if (row, col) != juego.empty_tile:
                expected_num = row * juego.grid_size + col + 1
                juego.text_vars[row][col].get.return_value = str(expected_num)
    juego.text_vars[juego.empty_tile[0]][juego.empty_tile[1]].get.return_value = " "

    # Verificar que text_vars esté configurado correctamente
    for row in range(juego.grid_size):
        for col in range(juego.grid_size):
            if (row, col) != juego.empty_tile:
                expected_num = row * juego.grid_size + col + 1
                assert juego.text_vars[row][col].get() == str(expected_num)
    assert juego.text_vars[juego.empty_tile[0]][juego.empty_tile[1]].get() == " "

    # Verificar el resultado de check_win
    assert juego.check_win() is True

def test_message_win(juego):
    with patch('tkinter.messagebox.askquestion', return_value='no'):
        juego.quit = MagicMock()
        juego.message_win()
        assert juego.quit.called