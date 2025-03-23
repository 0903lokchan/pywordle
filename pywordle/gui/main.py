"""Main GUI module for the Wordle game"""

import pygame
import sys
from gui.constants import (
    CELL_SIZE,
    CELL_MARGIN,
    BOARD_MARGIN,
    KEYBOARD_MARGIN,
)
from gui.game_state import GameState
from gui.event_manager import EventManager
from gui.renderer import Renderer


class WordleGUI:
    """Main GUI class for the Wordle game"""

    def __init__(self):
        pygame.init()
        self.game_state = GameState()

        # Calculate board dimensions
        self.board_width = 5 * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
        self.board_height = 6 * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN

        # Calculate keyboard dimensions
        self.keyboard_height = 3 * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
        self.keyboard_width = 10 * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN

        # Calculate control buttons dimensions
        self.button_width = CELL_SIZE * 2 + CELL_MARGIN
        self.control_buttons_width = (self.button_width * 2) + CELL_SIZE + CELL_MARGIN

        # Calculate window dimensions
        self.window_width = (
            max(self.board_width, self.keyboard_width, self.control_buttons_width)
            + 2 * BOARD_MARGIN
        )
        self.window_height = (
            self.board_height
            + self.keyboard_height
            + KEYBOARD_MARGIN  # Space between board and keyboard
            + CELL_SIZE
            + CELL_MARGIN  # Space for control buttons
            + 2 * BOARD_MARGIN
            + 40  # Extra space for message
        )

        # Create window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Wordle")

        # Initialize components
        self.event_manager = EventManager(
            self.game_state, self.window_width, self.board_height
        )
        self.renderer = Renderer(self.screen, self.game_state, self.window_width)
        self.game_state.event_manager = (
            self.event_manager
        )  # Add reference to event manager

    def run(self) -> None:
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.event_manager.handle_events()
            self.game_state.update()
            self.renderer.draw()

            if self.game_state.game.game_over:
                pygame.time.wait(3000)
                running = False

            clock.tick(60)

        pygame.quit()
        sys.exit()


def main():
    """Entry point for the GUI game"""
    try:
        gui = WordleGUI()
        gui.run()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

