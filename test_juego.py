import pytest
from unittest.mock import Mock, patch
from Interface.juego import Juego
from tkinter import Tk

@pytest.fixture
def mock_master():
    root = Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    root.mezclando = False
    root.winfo_children = Mock(return_value=[])
    root.space = Mock()
    root.create_close_button = Mock()
    root.create_back_button = Mock()
    root.start_shuffle_thread = Mock()
    root.confirm_exit = Mock()
    root.confirm_return_to_menu = Mock()
    root.menu = Mock()
    root.menu.create_menu_widgets = Mock()
    root.historial = Mock()
    root.historial.show_history = Mock()
    root.historial.save_score = Mock()
    root.is_adjacent = Mock(return_value=True)
    root.check_win = Mock(return_value=True)
    root.update_tile_color = Mock()
    root.message_win = Mock()
    root.text_shuffled = Mock()
    root.text_vars = [[Mock() for _ in range(4)] for _ in range(4)]
    root.tiles = [[Mock() for _ in range(4)] for _ in range(4)]
    root.moves_label = Mock()
    root.time_label = Mock()
    root.empty_tile = (3, 3)
    root.grid_size = 4
    root.moves = 0
    root.start_time = 0
    root.paused_time = 0
    return root

@pytest.fixture
def juego(mock_master):
    return Juego(mock_master)

def test_create_main_menu(juego, mock_master):
    juego.create_main_menu()
    assert mock_master.space.called
    assert mock_master.create_close_button.called
    assert mock_master.create_back_button.called

def test_start_level(juego, mock_master):
    juego.start_level(1)
    assert mock_master.level == 1
    assert mock_master.grid_size == 4
    assert mock_master.shuffle_num == 100
    assert mock_master.start_shuffle_thread.called

def test_create_game_widgets(juego, mock_master):
    juego.create_game_widgets()
    assert mock_master.create_close_button.called
    assert mock_master.create_back_button.called
    assert mock_master.moves_label.pack.called
    assert mock_master.time_label.pack.called

def test_move_tile(juego, mock_master):
    juego.move_tile(2, 3)
    assert mock_master.moves == 1
    assert mock_master.moves_label.configure.called
    assert mock_master.historial.save_score.called
    assert mock_master.message_win.called

def test_update_time(juego, mock_master):
    with patch('time.time', return_value=100):
        juego.update_time()
        assert mock_master.time_label.configure.called

def test_shuffle_tiles(juego, mock_master):
    with patch('random.choice', side_effect=[(2, 3), (3, 2), (2, 3), (3, 2)]):
        juego.shuffle_tiles()
        assert mock_master.text_shuffled.set.called
        assert mock_master.update_idletasks.called
        assert mock_master.start_loading_animation.called
        assert mock_master.stop_loading_animation.called