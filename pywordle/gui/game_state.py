"""Game state management for the Wordle GUI"""

import pygame
from typing import Any
from models.game import Game


class GameState:
    """Manages the game state including current guess, messages, and timing"""

    def __init__(self):
        self.game = Game()
        self.current_guess = ""
        self.message = ""
        self.message_time = 0
        self.event_manager: Any = None  # Will be set by WordleGUI

    def update(self) -> None:
        """Update game state"""
        current_time = pygame.time.get_ticks()
        if self.message and current_time - self.message_time > 3000:
            self.message = ""

    def handle_backspace(self) -> None:
        """Handle backspace key press"""
        self.current_guess = self.current_guess[:-1]

    def handle_enter(self) -> None:
        """Handle enter key press"""
        if len(self.current_guess) == 5:
            try:
                self.game.make_guess(self.current_guess.lower())
                if self.game.won:
                    self.message = f"Congratulations! You won in {len(self.game.board.guesses)} attempts!"
                elif self.game.game_over:
                    self.message = (
                        f"Game Over! The word was: {self.game.answer.upper()}"
                    )
                self.current_guess = ""
            except ValueError as e:
                self.message = str(e)
                self.message_time = pygame.time.get_ticks()

    def handle_letter(self, key: str) -> None:
        """Handle letter key press"""
        if len(self.current_guess) < 5:
            self.current_guess += key
