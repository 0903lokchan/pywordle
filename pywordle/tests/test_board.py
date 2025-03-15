import pytest
from models.board import Board

@pytest.fixture
def board():
    """Fixture to create a board for testing"""
    return Board("hello")

def test_board_initialization(board):
    """Test that a board is correctly initialized"""
    assert board.word == "hello"
    assert len(board.guesses) == 0
    assert not board.won

def test_correct_guess(board):
    """Test adding a correct guess"""
    board.add_guess("hello")
    assert board.won
    assert len(board.guesses) == 1

def test_incorrect_guess(board):
    """Test adding an incorrect guess"""
    board.add_guess("world")
    assert not board.won
    assert len(board.guesses) == 1

def test_multiple_guesses(board):
    """Test adding multiple guesses"""
    guesses = ["world", "helps", "hello"]
    for guess in guesses:
        board.add_guess(guess)
    
    assert board.won  # Last guess is correct
    assert len(board.guesses) == 3

def test_string_representation(board):
    """Test the string representation of the board"""
    board.add_guess("world")
    board.add_guess("hello")
    expected = "world\nhello"
    assert str(board) == expected 