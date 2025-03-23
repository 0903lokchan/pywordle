import pytest
from unittest.mock import patch
from pywordle.models.game import Game, WORD_LIST, MAX_GUESSES


@pytest.fixture
def game():
    """Fixture to create a game with a fixed answer"""
    with patch("random.choice", return_value="hello"):
        return Game()


def test_game_initialization(game):
    """Test that a game is correctly initialized"""
    assert game.answer == "hello"
    assert not game.game_over
    assert not game.won
    assert len(game.board.guesses) == 0


@pytest.mark.parametrize(
    "guess_word,expected_game_over,expected_won,expected_guesses",
    [
        ("hello", True, True, 1),  # Correct guess
        ("world", False, False, 1),  # Incorrect guess
        ("helps", False, False, 1),  # Partially correct guess
    ],
)
def test_single_guess(
    game, guess_word, expected_game_over, expected_won, expected_guesses
):
    """Test making a single guess with different outcomes"""
    game.make_guess(guess_word)
    assert game.game_over == expected_game_over
    assert game.won == expected_won
    assert len(game.board.guesses) == expected_guesses


@pytest.mark.parametrize(
    "guesses,expected_game_over,expected_won,expected_guesses",
    [
        (["world", "helps", "hello"], True, True, 3),  # Win on last guess
        (["world", "helps", "words", "tests", "these", "other"], True, False, 6),  # Lose after max guesses
        (["hello"], True, True, 1),  # Win on first guess
    ],
)
def test_multiple_guesses(
    game, guesses, expected_game_over, expected_won, expected_guesses
):
    """Test making multiple guesses with different outcomes"""
    for guess in guesses:
        game.make_guess(guess)
    assert game.game_over == expected_game_over
    assert game.won == expected_won
    assert len(game.board.guesses) == expected_guesses


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


@pytest.mark.parametrize(
    "guesses,expected_str",
    [
        (["world", "hello"], "world\nhello"),
        (["helps", "words"], "helps\nwords"),
        (["hello"], "hello"),
    ],
)
def test_string_representation(game, guesses, expected_str):
    """Test string representation for different guess sequences"""
    for guess in guesses:
        game.make_guess(guess)
    assert str(game) == expected_str


@pytest.mark.parametrize("word", WORD_LIST)
def test_word_list_validity(word):
    """Test that each word in the word list is valid"""
    assert len(word) == 5  # All words should be 5 letters
    assert word.isalpha()  # All words should be alphabetic
