from letter import Letter

class Guess:
    """
    A class that represents a guess in the game. With a check method to check if the guess is correct.
    """
    def __init__(self, word: str, answer: str):
        self.letters = [Letter(char, False, False, False) for char in word]
        self.check_guess(answer)
        self.all_correct = all(letter.is_correct for letter in self.letters)

    def check_guess(self, answer: str) -> None:
        for i, letter in enumerate(self.letters):
            if letter.char == answer[i]:
                letter.is_correct = True
            elif letter.char in answer:
                letter.is_present = True
            else:
                letter.is_absent = True

    def __str__(self) -> str:
        return "".join([letter.char for letter in self.letters])

