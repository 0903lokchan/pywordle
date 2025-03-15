import random

from board import Board

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
        self.answer = random.choice(WORD_LIST)
        self.board = Board(self.answer)
        self.game_over = False
        self.won = False
        
    def make_guess(self, guess: str) -> None:
        self.board.add_guess(guess)
        
        if self.board.won:
            self.game_over = True
            self.won = True
        elif len(self.board.guesses) >= MAX_GUESSES:
            self.game_over = True
            
    def __str__(self) -> str:
        return str(self.board)
