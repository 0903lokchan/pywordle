import pytest
from pywordle.models.board import Board


@pytest.fixture
def board():
    """Fixture to create a board for testing"""
    return Board("hello")


def test_board_initialization(board):
    """Test that a board is correctly initialized"""
    assert board.answer == "hello"
    assert len(board.guesses) == 0
    assert not board.won


@pytest.mark.parametrize(
    "guess_word,expected_won,expected_guesses",
    [
        ("hello", True, 1),  # Correct guess
        ("world", False, 1),  # Incorrect guess
        ("helps", False, 1),  # Partially correct guess
    ],
)
def test_single_guess(board, guess_word, expected_won, expected_guesses):
    """Test adding a single guess with different outcomes"""
    board.add_guess(guess_word)
    assert board.won == expected_won
    assert len(board.guesses) == expected_guesses


@pytest.mark.parametrize(
    "guesses,expected_won,expected_count",
    [
        (["world", "helps", "hello"], True, 3),  # Win on last guess
        (["world", "helps", "words"], False, 3),  # No win
        (["hello"], True, 1),  # Win on first guess
    ],
)
def test_multiple_guesses(board, guesses, expected_won, expected_count):
    """Test adding multiple guesses with different outcomes"""
    for guess in guesses:
        board.add_guess(guess)
    assert board.won == expected_won
    assert len(board.guesses) == expected_count


@pytest.mark.parametrize(
    "guesses,expected_str",
    [
        (["world", "hello"], "world\nhello"),
        (["helps", "words"], "helps\nwords"),
        (["hello"], "hello"),
    ],
)
def test_string_representation(board, guesses, expected_str):
    """Test string representation for different guess sequences"""
    for guess in guesses:
        board.add_guess(guess)
    assert str(board) == expected_str
