"""Rendering for the Wordle GUI"""

import pygame
from typing import Optional, Tuple
from gui.constants import (
    BLACK,
    WHITE,
    GRAY,
    YELLOW,
    GREEN,
    DARK_GRAY,
    CELL_SIZE,
    CELL_MARGIN,
    BOARD_MARGIN,
    KEYBOARD_MARGIN,
)
from gui.game_state import GameState
from models.letter import Letter


class Renderer:
    """Handles all rendering for the Wordle GUI"""

    def __init__(
        self, screen: pygame.Surface, game_state: GameState, window_width: int
    ):
        self.screen = screen
        self.game_state = game_state
        self.window_width = window_width
        self.font = pygame.font.Font(None, 36)

    def draw(self) -> None:
        """Draw game state"""
        self.screen.fill(BLACK)
        self.draw_board()
        self.draw_keyboard()
        self.draw_message()
        pygame.display.flip()

    def get_letter_color(self, letter: Letter) -> Tuple[int, int, int]:
        """Get the color for a letter based on its state"""
        if letter.is_correct:
            return GREEN
        elif letter.is_present:
            return YELLOW
        elif letter.is_absent:
            return DARK_GRAY
        return GRAY

    def draw_cell(
        self, letter: Optional[str], x: int, y: int, color: Tuple[int, int, int]
    ) -> None:
        """Draw a single cell with a letter"""
        cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, cell_rect, border_radius=5)

        if letter:
            text = self.font.render(letter, True, WHITE)
            text_rect = text.get_rect(center=cell_rect.center)
            self.screen.blit(text, text_rect)

    def draw_board(self) -> None:
        """Draw the game board"""
        for row in range(6):
            for col in range(5):
                x = BOARD_MARGIN + col * (CELL_SIZE + CELL_MARGIN)
                y = BOARD_MARGIN + row * (CELL_SIZE + CELL_MARGIN)

                if row < len(self.game_state.game.board.guesses):
                    letter = self.game_state.game.board.guesses[row].letters[col]
                    color = self.get_letter_color(letter)
                    self.draw_cell(str(letter), x, y, color)
                elif row == len(self.game_state.game.board.guesses):
                    # Draw current guess
                    letter = (
                        self.game_state.current_guess[col]
                        if col < len(self.game_state.current_guess)
                        else None
                    )
                    self.draw_cell(letter, x, y, GRAY)
                else:
                    self.draw_cell(None, x, y, GRAY)

    def draw_keyboard(self) -> None:
        """Draw the on-screen keyboard"""
        keyboard_y = 6 * (CELL_SIZE + CELL_MARGIN) + BOARD_MARGIN + KEYBOARD_MARGIN

        # Draw main keyboard
        if not self.game_state.event_manager:
            raise ValueError("EventManager is not passed to GameState when this is run")
        for row_idx, row in enumerate(self.game_state.event_manager.keyboard):
            row_width = len(row) * (CELL_SIZE + CELL_MARGIN) - CELL_MARGIN
            start_x = (self.window_width - row_width) // 2

            for col_idx, key in enumerate(row):
                x = start_x + col_idx * (CELL_SIZE + CELL_MARGIN)
                y = keyboard_y + row_idx * (CELL_SIZE + CELL_MARGIN)

                # Draw key
                key_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, key_rect, border_radius=5)

                # Draw key text
                text = self.font.render(key, True, WHITE)
                text_rect = text.get_rect(center=key_rect.center)
                self.screen.blit(text, text_rect)

        # Draw ENTER and BACKSPACE buttons below the keyboard
        bottom_y = (
            keyboard_y
            + len(self.game_state.event_manager.keyboard) * (CELL_SIZE + CELL_MARGIN)
            + KEYBOARD_MARGIN
        )
        button_width = CELL_SIZE * 2 + CELL_MARGIN  # Make buttons wider

        # Draw ENTER button
        enter_x = (self.window_width - (button_width + CELL_SIZE + button_width)) // 2
        enter_rect = pygame.Rect(enter_x, bottom_y, button_width, CELL_SIZE)
        pygame.draw.rect(self.screen, GRAY, enter_rect, border_radius=5)
        text = self.font.render("ENTER", True, WHITE)
        text_rect = text.get_rect(center=enter_rect.center)
        self.screen.blit(text, text_rect)

        # Draw BACKSPACE button
        backspace_x = enter_x + button_width + CELL_SIZE + CELL_MARGIN
        backspace_rect = pygame.Rect(backspace_x, bottom_y, button_width, CELL_SIZE)
        pygame.draw.rect(self.screen, GRAY, backspace_rect, border_radius=5)
        text = self.font.render("BACK", True, WHITE)
        text_rect = text.get_rect(center=backspace_rect.center)
        self.screen.blit(text, text_rect)

    def draw_message(self) -> None:
        """Draw the message at the bottom of the screen"""
        if self.game_state.message:
            text = self.font.render(self.game_state.message, True, WHITE)
            text_rect = text.get_rect(
                center=(self.window_width // 2, self.screen.get_height() - 20)
            )
            self.screen.blit(text, text_rect)
