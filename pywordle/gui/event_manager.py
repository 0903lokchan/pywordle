"""Event handling for the Wordle GUI"""

import pygame
from typing import Optional, Tuple, Any
from gui.constants import CELL_SIZE, CELL_MARGIN, BOARD_MARGIN, KEYBOARD_MARGIN


class EventManager:
    """Handles all input events for the Wordle GUI"""

    def __init__(self, game_state: Any, window_width: int, board_height: int):
        self.game_state = game_state
        self.window_width = window_width
        self.board_height = board_height
        self.keyboard = self.create_keyboard()

    def create_keyboard(self) -> list[list[str]]:
        """Create the on-screen keyboard layout"""
        return [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"],
        ]

    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                key = self.handle_keyboard_click(event.pos)
                if key:
                    self.handle_key_press(key)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.handle_key_press("BACKSPACE")
                elif event.key == pygame.K_RETURN:
                    self.handle_key_press("ENTER")
                elif event.unicode.isalpha():
                    self.handle_key_press(event.unicode.upper())
        return True

    def handle_keyboard_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """Handle clicks on the on-screen keyboard"""
        keyboard_y = self.board_height + BOARD_MARGIN + KEYBOARD_MARGIN

        # Check main keyboard
        for row_idx, row in enumerate(self.keyboard):
            row_width = len(row) * (CELL_SIZE + CELL_MARGIN) - CELL_MARGIN
            start_x = (self.window_width - row_width) // 2

            for col_idx, key in enumerate(row):
                x = start_x + col_idx * (CELL_SIZE + CELL_MARGIN)
                y = keyboard_y + row_idx * (CELL_SIZE + CELL_MARGIN)

                key_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                if key_rect.collidepoint(pos):
                    return key

        # Check ENTER and BACKSPACE buttons
        bottom_y = (
            keyboard_y
            + len(self.keyboard) * (CELL_SIZE + CELL_MARGIN)
            + KEYBOARD_MARGIN
        )
        button_width = CELL_SIZE * 2 + CELL_MARGIN

        # Check ENTER button
        enter_x = (self.window_width - (button_width + CELL_SIZE + button_width)) // 2
        enter_rect = pygame.Rect(enter_x, bottom_y, button_width, CELL_SIZE)
        if enter_rect.collidepoint(pos):
            return "ENTER"

        # Check BACKSPACE button
        backspace_x = enter_x + button_width + CELL_SIZE + CELL_MARGIN
        backspace_rect = pygame.Rect(backspace_x, bottom_y, button_width, CELL_SIZE)
        if backspace_rect.collidepoint(pos):
            return "BACKSPACE"

        return None

    def handle_key_press(self, key: str) -> None:
        """Handle keyboard input"""
        if key == "BACKSPACE":
            self.game_state.handle_backspace()
        elif key == "ENTER":
            self.game_state.handle_enter()
        elif len(key) == 1 and key.isalpha():
            self.game_state.handle_letter(key)
