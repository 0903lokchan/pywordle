import pytest
from models.letter import Letter

def test_letter_initialization():
    """Test that a Letter object is correctly initialized"""
    letter = Letter('a', False, False, False)
    assert letter.char == 'a'
    assert not letter.is_correct
    assert not letter.is_present
    assert not letter.is_absent

def test_letter_states():
    """Test different letter states"""
    # Correct letter
    correct_letter = Letter('b', True, False, False)
    assert correct_letter.is_correct
    assert not correct_letter.is_present
    assert not correct_letter.is_absent

    # Present but wrong position letter
    present_letter = Letter('c', False, True, False)
    assert not present_letter.is_correct
    assert present_letter.is_present
    assert not present_letter.is_absent

    # Absent letter
    absent_letter = Letter('d', False, False, True)
    assert not absent_letter.is_correct
    assert not absent_letter.is_present
    assert absent_letter.is_absent 