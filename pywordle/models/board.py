from models.guess import Guess

class Board:
    """A class for handling the answer and guesses of the game.
    """
    def __init__(self, word: str):
        self.word = word
        self.guesses = []
        self.won = False

    def add_guess(self, guess_word: str) -> None:
        if self.won:
            raise ValueError("Game already won")
        
        self.guesses.append(Guess(guess_word, self.word))
        if self.guesses[-1].all_correct:
            self.won = True

    def __str__(self) -> str:
        return "\n".join(str(guess) for guess in self.guesses)
