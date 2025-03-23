import pytest
from pywordle.models.guess import Guess


@pytest.mark.parametrize(
    "guess_word,answer,expected_states",
    [
        ("hello", "hello", [(True, False, False)] * 5),  # All correct
        (
            "world",
            "words",
            [
                (True, False, False),  # w
                (True, False, False),  # o
                (True, False, False),  # r
                (False, False, True),  # l
                (False, True, False),  # d
            ],
        ),
        (
            "heart",
            "earth",
            [
                (False, True, False),  # h
                (False, True, False),  # e
                (False, True, False),  # a
                (False, True, False),  # r
                (False, True, False),  # t
            ],
        ),
        ("quick", "happy", [(False, False, True)] * 5),  # All absent
    ],
)
def test_guess_states(guess_word, answer, expected_states):
    """Test different guess scenarios using parameterized inputs"""
    guess = Guess(guess_word, answer)
    for letter, (is_correct, is_present, is_absent) in zip(
        guess.letters, expected_states
    ):
        assert letter.is_correct == is_correct
        assert letter.is_present == is_present
        assert letter.is_absent == is_absent


@pytest.mark.parametrize(
    "guess_word,answer,expected_all_correct",
    [
        ("hello", "hello", True),
        ("world", "words", False),
        ("heart", "earth", False),
        ("quick", "happy", False),
    ],
)
def test_all_correct_flag(guess_word, answer, expected_all_correct):
    """Test the all_correct flag for different guesses"""
    guess = Guess(guess_word, answer)
    assert guess.all_correct == expected_all_correct


@pytest.mark.parametrize(
    "guess_word,answer,expected_str",
    [
        ("hello", "hello", "hello"),
        ("world", "words", "world"),
        ("test", "best", "test"),
    ],
)
def test_string_representation(guess_word, answer, expected_str):
    """Test string representation for different guesses"""
    guess = Guess(guess_word, answer)
    assert str(guess) == expected_str
