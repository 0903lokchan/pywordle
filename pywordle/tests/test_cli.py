import re
import pytest
from unittest.mock import patch, MagicMock
from cli import WordleCLI
from models.guess import Guess

@pytest.fixture
def cli():
    """Fixture to create a CLI instance for testing"""
    return WordleCLI()


def test_cli_initialization(cli):
    """Test that CLI is correctly initialized"""
    assert cli.attempts == 0
    assert cli.max_attempts == 6
    assert not cli.game.game_over
    assert not cli.game.won


@pytest.mark.parametrize(
    "input_value,expected_output",
    [
        ("hello", "hello"),
        ("quit", None),
    ],
)
def test_get_valid_guess(cli, input_value, expected_output):
    """Test getting valid guesses from user"""
    with patch("builtins.input", return_value=input_value):
        guess = cli.get_valid_guess()
        assert guess == expected_output
        

@pytest.mark.parametrize(
    "input_sequence,expected_output",
    [
        (["12345", "quit"], "Guess must contain only letters!\n"),
        (["abc", "quit"], "Guess must be 5 letters long!\n",),
    ],
)
def test_get_valid_guess_invalid_input(cli, input_sequence, expected_output, capsys):
    """Test getting invalid guesses from user"""
    with patch("builtins.input", side_effect=input_sequence):
        guess = cli.get_valid_guess()
        captured = capsys.readouterr()
        assert expected_output in captured.out


def test_display_letter_status(cli):
    """Test letter status display formatting"""
    # Test correct letter (green)
    correct_string = cli.display_letter_status("a", True, False)
    assert "\033[92m" in correct_string  # Green color code
    assert "A" in correct_string

    # Test present letter (yellow)
    present_string = cli.display_letter_status("b", False, True)
    assert "\033[93m" in present_string  # Yellow color code
    assert "B" in present_string

    # Test absent letter (gray)
    absent_string = cli.display_letter_status("c", False, False)
    assert "\033[90m" in absent_string  # Gray color code
    assert "C" in absent_string


def test_display_board(cli, capsys):
    """Test board display"""
    # create a mock board with a guess
    mock_board = MagicMock()
    mock_board.guesses = [Guess("hello", "hello")]
    cli.game.board = mock_board
    
    cli.display_board()
    captured = capsys.readouterr()
    
    assert "=" * 30 in captured.out
    for letter in "hello":
        # pattern match the output
        assert re.search(r"\033\[9[0-9]m" + letter.upper() + r"\033\[0m", captured.out)


@pytest.mark.parametrize(
    "input_sequence,expected_output",
    [
        (["hello"], "Congratulations!"),
        (["world"] * 6, "Game Over!"),
        (["quit"], "Game Over!"),
    ],
)
def test_play_game(cli, input_sequence, expected_output, capsys):
    """Test the main game loop with different scenarios"""
    # set the word to guess
    cli.game.answer = "hello"
    
    with patch("builtins.input", side_effect=input_sequence):
        cli.play()
        captured = capsys.readouterr()
        assert expected_output in captured.out


# TODO: Fix this test. It causes pytest to enter an infinite loop.
# def test_error_handling(cli):
#     """Test error handling in the game loop"""
#     with patch("builtins.input", return_value="hello"), patch.object(
#         cli.game, "make_guess", side_effect=ValueError("Test error")
#     ):
#         cli.play()
#         # Verify the game continues after an error
#         assert cli.attempts == 0
