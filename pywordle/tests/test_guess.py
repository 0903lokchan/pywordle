import pytest
from models.guess import Guess

def test_correct_guess():
    """Test a completely correct guess"""
    guess = Guess("hello", "hello")
    assert guess.all_correct
    assert all(letter.is_correct for letter in guess.letters)
    assert not any(letter.is_present for letter in guess.letters)
    assert not any(letter.is_absent for letter in guess.letters)

def test_partially_correct_guess():
    """Test a partially correct guess with some letters in wrong positions"""
    guess = Guess("world", "words")
    # 'w', 'o', 'r', 'd' should be correct
    assert guess.letters[0].is_correct  # w
    assert guess.letters[1].is_correct  # o
    assert guess.letters[2].is_correct  # r
    # 'l' should be absent
    assert guess.letters[3].is_absent  # l
    # 'd' should be present
    assert guess.letters[4].is_present   # d
    assert not guess.all_correct

def test_wrong_position_letters():
    """Test a guess with correct letters in wrong positions"""
    guess = Guess("heart", "earth")
    # 'h' should be present (wrong position)
    assert guess.letters[0].is_present
    # 'e', 'a', 'r', 't' should be present in wrong positions
    assert not guess.all_correct

def test_completely_wrong_guess():
    """Test a completely wrong guess"""
    guess = Guess("quick", "happy")
    assert not guess.all_correct
    assert all(letter.is_absent for letter in guess.letters)

def test_string_representation():
    """Test the string representation of a guess"""
    guess = Guess("test", "best")
    assert str(guess) == "test" 