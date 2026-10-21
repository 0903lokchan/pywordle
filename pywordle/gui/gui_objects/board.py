from pygame import Rect

from pywordle.gui.gui_objects.cell import Cell


class Board(Rect):
    def __init__(self, left: float, top: float, width: float, height: float)-> None:
        super().__init__(left, top, width, height)
        self.cells: list[list[Cell]] = [] # A row-first grid

    def create_cells(self, cell_size: int, cell_margin: int)-> None:
        # regenerate the cells if they exist
        if self.cells:
            self.cells = []

        n_row = 6
        n_letter = 5

        for row in range(n_row):
            y = self.top + row * (cell_size + cell_margin)
            self.cells.append([
                Cell(self.left + col * (cell_size + cell_margin), y, cell_size, cell_size)
                for col in range(n_letter)
            ])
