import pytest
import pygame
from unittest.mock import patch, MagicMock
from pywordle.gui.main import WordleGUI
from pywordle.gui.game_state import GameState
from pywordle.gui.event_manager import EventManager
from pywordle.gui.renderer import Renderer
from pywordle.gui.constants import (
    CELL_SIZE,
    CELL_MARGIN,
    BOARD_MARGIN,
    KEYBOARD_MARGIN,
)


@pytest.fixture
def game_state():
    """Fixture to create a game state instance for testing"""
    return GameState()


@pytest.fixture
def event_manager(game_state):
    """Fixture to create an event manager instance for testing"""
    return EventManager(game_state, 800, 400)


@pytest.fixture
def renderer(game_state):
    """Fixture to create a renderer instance for testing"""
    pygame.init()
    screen = MagicMock()
    renderer = Renderer(screen, game_state, 800)
    yield renderer
    pygame.quit()


@pytest.fixture
def gui():
    """Fixture to create a GUI instance for testing"""
    with patch("pygame.init"), patch("pygame.display.set_mode"), patch(
        "pygame.display.set_caption"
    ), patch("pygame.font.Font"):
        gui = WordleGUI()
        gui.screen = MagicMock()
        return gui


def test_game_state_initialization(game_state):
    """Test that game state is correctly initialized"""
    assert game_state.current_guess == ""
    assert game_state.message == ""
    assert game_state.message_time == 0
    assert not game_state.game.game_over
    assert not game_state.game.won


def test_game_state_handlers(game_state):
    """Test game state handlers"""
    # Test letter handling
    game_state.handle_letter("A")
    assert game_state.current_guess == "A"

    game_state.handle_letter("B")
    assert game_state.current_guess == "AB"

    # Test backspace
    game_state.handle_backspace()
    assert game_state.current_guess == "A"

    # Test enter with valid word
    with patch.object(game_state.game, "make_guess"):
        game_state.current_guess = "HELLO"
        game_state.handle_enter()
        assert game_state.current_guess == ""

    # Test enter with invalid word
    game_state.current_guess = "ABC"
    game_state.handle_enter()
    assert game_state.current_guess == "ABC"  # Should not clear invalid guess


def test_event_manager_initialization(event_manager):
    """Test that event manager is correctly initialized"""
    assert len(event_manager.keyboard) == 3  # Three rows of keys
    assert len(event_manager.keyboard[0]) == 10  # First row: Q-P
    assert len(event_manager.keyboard[1]) == 9  # Second row: A-L
    assert len(event_manager.keyboard[2]) == 7  # Third row: Z-M


def test_event_handling(event_manager):
    """Test event handling"""
    # Test keyboard events
    with patch("pygame.event.get") as mock_get:
        # Test backspace
        mock_get.return_value = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE})
        ]
        event_manager.handle_events()
        assert event_manager.game_state.current_guess == ""

        # Test enter
        mock_get.return_value = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
        ]
        event_manager.handle_events()

        # Test letter
        mock_get.return_value = [
            pygame.event.Event(pygame.KEYDOWN, {"key": ord("A"), "unicode": "a"})
        ]
        event_manager.handle_events()
        assert event_manager.game_state.current_guess == "A"


def test_renderer_letter_colors(renderer):
    """Test letter color assignment"""
    from pywordle.models.letter import Letter

    # Test correct letter (green)
    correct_letter = Letter("A", True, False, False)
    assert renderer.get_letter_color(correct_letter) == (
        76,
        175,
        80,
    )  # Material design green

    # Test present letter (yellow)
    present_letter = Letter("B", False, True, False)
    assert renderer.get_letter_color(present_letter) == (204, 172, 0)  # Muted yellow

    # Test absent letter (dark gray)
    absent_letter = Letter("C", False, False, True)
    assert renderer.get_letter_color(absent_letter) == (64, 64, 64)  # DARK_GRAY


def test_window_dimensions(gui):
    """Test window size calculations"""
    # Test board dimensions
    assert gui.board_width == 330  # 5 * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
    assert gui.board_height == 395  # 6 * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN

    # Test keyboard dimensions
    assert gui.keyboard_height == 200  # 3 * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
    assert gui.keyboard_width == 655  # 10 * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN

    # Test window dimensions
    assert (
        gui.window_width
        >= max(gui.board_width, gui.keyboard_width, gui.control_buttons_width)
        + 2 * BOARD_MARGIN
    )
    assert gui.window_height >= (
        gui.board_height
        + gui.keyboard_height
        + KEYBOARD_MARGIN
        + CELL_SIZE
        + CELL_MARGIN
        + 2 * BOARD_MARGIN
        + 40
    )
