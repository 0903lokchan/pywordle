import random

from models.board import Board

WORD_LIST = [
    "apple",
    "hello",
    "world",
    "there",
    "these",
    "other",
    "which",
    "their",
    "about",
    "would",
]
MAX_GUESSES = 6

class Game:
    def __init__(self):
        answer = random.choice(WORD_LIST)
        self.board = Board(answer)
        self.game_over = False
        self.won = False
        self.max_attempts = MAX_GUESSES

    def make_guess(self, guess: str) -> None:
        self.board.add_guess(guess)
        
        if self.board.won:
            self.game_over = True
            self.won = True
        elif len(self.board.guesses) >= self.max_attempts:
            self.game_over = True
            
    @property
    def answer(self) -> str:
        return self.board.answer
    
    @answer.setter
    def answer(self, value: str) -> None:
        self.board.answer = value
            
    def __str__(self) -> str:
        return str(self.board)
