import pytest
from unittest.mock import patch
from models.game import Game, WORD_LIST, MAX_GUESSES

@pytest.fixture
def game():
    """Fixture to create a game with a fixed answer"""
    with patch('random.choice', return_value="hello"):
        return Game()

def test_game_initialization(game):
    """Test that a game is correctly initialized"""
    assert game.answer == "hello"
    assert not game.game_over
    assert not game.won
    assert len(game.board.guesses) == 0

def test_correct_guess(game):
    """Test making a correct guess"""
    game.make_guess("hello")
    assert game.game_over
    assert game.won
    assert len(game.board.guesses) == 1

def test_incorrect_guess(game):
    """Test making an incorrect guess"""
    game.make_guess("world")
    assert not game.game_over
    assert not game.won
    assert len(game.board.guesses) == 1

def test_max_guesses(game):
    """Test reaching maximum number of guesses"""
    for _ in range(MAX_GUESSES):
        game.make_guess("world")
    
    assert game.game_over
    assert not game.won
    assert len(game.board.guesses) == MAX_GUESSES

def test_game_over_after_win(game):
    """Test that game ends after a correct guess"""
    game.make_guess("hello")
    # Try to make another guess after winning
    with pytest.raises(ValueError):
        game.make_guess("world")
    assert game.game_over
    assert game.won
    assert len(game.board.guesses) == 1

def test_string_representation(game):
    """Test the string representation of the game"""
    game.make_guess("world")
    game.make_guess("hello")
    expected = "world\nhello"
    assert str(game) == expected

def test_word_list():
    """Test that the word list is not empty and contains valid words"""
    assert len(WORD_LIST) > 0
    for word in WORD_LIST:
        assert len(word) == 5  # All words should be 5 letters
        assert word.isalpha()  # All words should be alphabetic 