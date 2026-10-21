"""Rendering for the Wordle GUI"""

import pygame

from pywordle.gui.constants import (
    BLACK,
    BOARD_MARGIN,
    CELL_MARGIN,
    CELL_SIZE,
    DARK_GRAY,
    GRAY,
    GREEN,
    KEYBOARD_MARGIN,
    WHITE,
    YELLOW,
)
from pywordle.gui.game_state import GameState
from pywordle.gui.gui_objects.board import Board
from pywordle.gui.gui_objects.cell import Cell
from pywordle.models.letter import Letter


class Renderer:
    """Handles all rendering for the Wordle GUI"""

    def __init__(
        self, game_state: GameState, config: dict[str, int] | None=None
    ):
        self.game_state = game_state
        self.font = pygame.font.Font(None, 36)
        self.set_dimension_variables(config)
        self.screen = self.create_screen()
        self.board = self.create_board()
        self.rect_tree = [self.board]

    def set_dimension_variables(self, config: dict[str, int] | None)-> None:
        """Setup all dimension variables either from a provided config object or constants"""
        if config:
            self.cell_size = config["cell_size"]
            self.cell_margin = config["cell_margin"]
            self.board_margin = config["board_margin"]
            self.keyboard_margin = config["keyboard_margin"]
        else:
            self.cell_size = CELL_SIZE
            self.cell_margin = CELL_MARGIN
            self.board_margin = BOARD_MARGIN
            self.keyboard_margin = KEYBOARD_MARGIN

    def draw(self) -> None:
        """Draw game state"""
        self.screen.fill(BLACK)
        self.draw_board()
        self.draw_keyboard()
        self.draw_message()
        pygame.display.flip()

    def get_letter_color(self, letter: Letter) -> tuple[int, int, int]:
        """Get the color for a letter based on its state"""
        if letter.is_correct:
            return GREEN
        elif letter.is_present:
            return YELLOW
        elif letter.is_absent:
            return DARK_GRAY
        return GRAY
    
    def get_board_dimensions(self)-> tuple[int, int]:
        """Calculate the board dimensions from constants"""
        # 6 rows of 5-letter guesses
        board_row = 6
        board_column = 5

        board_width = board_column * (self.cell_size + self.cell_margin) + self.cell_margin
        board_height = board_row * (self.cell_size + self.cell_margin) + self.cell_margin
        return board_width, board_height
    
    def get_keyboard_dimensions(self)-> tuple[int, int]:
        """Calculate the keyboard dimensions from constants"""
        # Simulate a QWERTY keyboard with 3 rows and 10 keys on the widest row
        keyboard_row = 3
        keyboard_column = 10

        keyboard_width = keyboard_column * (self.cell_size + self.cell_margin) + self.cell_margin
        keyboard_height = keyboard_row * (self.cell_size + self.cell_margin) + self.cell_margin
        return keyboard_width, keyboard_height
    
    def get_control_button_dimensions(self)-> tuple[int, int]:
        """Calculate control buttons dimensions"""
        # Control buttons are 2-cell wide
        button_width = self.cell_size * 2 + self.cell_margin
        control_buttons_width = (button_width * 2) + self.cell_size + self.cell_margin
        control_buttons_height = self.cell_size + self.cell_margin * 2
        return control_buttons_width, control_buttons_height
    
    def get_window_dimensions(self)-> tuple[int, int]:
        """Decide window dimensions based on all the components' dimensions"""

        component_dimensions = {
            "board": self.get_board_dimensions(),
            "kyboard_padding": (0, self.keyboard_margin), # flexible width
            "keyboard": self.get_keyboard_dimensions(),
            "control_buttons": self.get_control_button_dimensions(),
            "message_box": (0, 40) # flexible width
        }

        # Calculate window dimensions
        component_widths = [dimensions[0] for _, dimensions in component_dimensions.items()]
        window_width = max(component_widths) + 2 * self.board_margin #the widest component + margins
        window_height = sum([dimensions[1] for _, dimensions in component_dimensions.items()]) + 2 * self.board_margin
        return window_width, window_height
    
    def create_screen(self)-> pygame.Surface:
        """Create a pygame screen for displaying the game"""
        self.window_width, self.window_height = self.get_window_dimensions()
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Wordle")
        return screen

    def create_board(self)-> Board:
        """Create the board and its grid of cells"""
        board = Board(self.board_margin, self.board_margin, *self.get_board_dimensions())
        board.create_cells(self.cell_size, self.cell_margin)
        return board

    def draw_cell(self, cell: Cell, color: tuple[int, int, int]) -> None:
        """Draw a single cell with its letter"""
        pygame.draw.rect(self.screen, color, cell, border_radius=5)

        if cell.text:
            text = self.font.render(cell.text, True, WHITE)
            text_rect = text.get_rect(center=cell.center)
            self.screen.blit(text, text_rect)

    def draw_board(self) -> None:
        """Draw the game board"""
        for row, cells in enumerate(self.board.cells):
            for col, cell in enumerate(cells):
                color = GRAY
                if row < len(self.game_state.game.board.guesses):
                    letter = self.game_state.game.board.guesses[row].letters[col]
                    color = self.get_letter_color(letter)
                    cell.text = str(letter)
                elif row == len(self.game_state.game.board.guesses):
                    # Draw current guess
                    cell.text = (
                        self.game_state.current_guess[col]
                        if col < len(self.game_state.current_guess)
                        else ""
                    )
                else:
                    cell.text = ""
                self.draw_cell(cell, color)

    def draw_keyboard(self) -> None:
        """Draw the on-screen keyboard"""
        keyboard_y = 6 * (self.cell_size + self.cell_margin) + BOARD_MARGIN + KEYBOARD_MARGIN

        # Draw main keyboard
        if not self.game_state.event_manager:
            raise ValueError("EventManager is not passed to GameState when this is run")
        for row_idx, row in enumerate(self.game_state.event_manager.keyboard):
            row_width = len(row) * (self.cell_size + self.cell_margin) - self.cell_margin
            start_x = (self.window_width - row_width) // 2

            for col_idx, key in enumerate(row):
                x = start_x + col_idx * (self.cell_size + self.cell_margin)
                y = keyboard_y + row_idx * (self.cell_size + self.cell_margin)

                # Draw key
                key_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, GRAY, key_rect, border_radius=5)

                # Draw key text
                text = self.font.render(key, True, WHITE)
                text_rect = text.get_rect(center=key_rect.center)
                self.screen.blit(text, text_rect)

        # Draw ENTER and BACKSPACE buttons below the keyboard
        bottom_y = (
            keyboard_y
            + len(self.game_state.event_manager.keyboard) * (self.cell_size + self.cell_margin)
            + KEYBOARD_MARGIN
        )
        button_width = self.cell_size * 2 + self.cell_margin  # Make buttons wider

        # Draw ENTER button
        enter_x = (self.window_width - (button_width + self.cell_size + button_width)) // 2
        enter_rect = pygame.Rect(enter_x, bottom_y, button_width, self.cell_size)
        pygame.draw.rect(self.screen, GRAY, enter_rect, border_radius=5)
        text = self.font.render("ENTER", True, WHITE)
        text_rect = text.get_rect(center=enter_rect.center)
        self.screen.blit(text, text_rect)

        # Draw BACKSPACE button
        backspace_x = enter_x + button_width + self.cell_size + self.cell_margin
        backspace_rect = pygame.Rect(backspace_x, bottom_y, button_width, self.cell_size)
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
