"""Main GUI module for the Wordle game"""

import sys

import pygame

from pywordle.gui.event_manager import EventManager
from pywordle.gui.game_state import GameState
from pywordle.gui.renderer import Renderer


class WordleGUI:
    """Main GUI class for the Wordle game"""

    def __init__(self):
        pygame.init()
        self.game_state = GameState()

        # Initialize components
        self.renderer = Renderer(self.game_state)
        #TODO remove the dependency to display dimensions from EventManager
        window_width = self.renderer.get_window_dimensions()[0]
        board_height = self.renderer.get_board_dimensions()[1]
        self.event_manager = EventManager(
            self.game_state, window_width, board_height
        )
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
    except Exception as e:  # noqa: BLE001 - top-level catch-all reports any error and exits
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

