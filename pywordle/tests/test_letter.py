import pytest
from models.letter import Letter


def test_letter_initialization():
    """Test that a Letter object is correctly initialized"""
    letter = Letter("a", False, False, False)
    assert letter.char == "a"
    assert not letter.is_correct
    assert not letter.is_present
    assert not letter.is_absent


@pytest.mark.parametrize(
    "char,is_correct,is_present,is_absent",
    [
        ("b", True, False, False),  # Correct letter
        ("c", False, True, False),  # Present but wrong position
        ("d", False, False, True),  # Absent letter
    ],
)
def test_letter_states(char, is_correct, is_present, is_absent):
    """Test different letter states using parameterized inputs"""
    letter = Letter(char, is_correct, is_present, is_absent)
    assert letter.is_correct == is_correct
    assert letter.is_present == is_present
    assert letter.is_absent == is_absent
