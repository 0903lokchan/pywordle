from pywordle.gui.gui_objects.board import Board
from pywordle.gui.gui_objects.cell import Cell


def test_create_cells_grid_layout():
    """Test that the board creates a 6x5 grid of cells laid out from its top-left"""
    board = Board(20, 20, 330, 395)
    board.create_cells(cell_size=60, cell_margin=5)

    assert len(board.cells) == 6
    assert all(len(row) == 5 for row in board.cells)
    assert all(isinstance(cell, Cell) for row in board.cells for cell in row)
    assert board.cells[0][0].topleft == (20, 20)
    assert board.cells[1][2].topleft == (20 + 2 * 65, 20 + 65)
    assert board.cells[5][4].size == (60, 60)


def test_create_cells_regenerates():
    """Test that calling create_cells again replaces the grid instead of appending"""
    board = Board(0, 0, 330, 395)
    board.create_cells(cell_size=60, cell_margin=5)
    board.create_cells(cell_size=50, cell_margin=5)

    assert len(board.cells) == 6
    assert board.cells[0][1].topleft == (55, 0)
