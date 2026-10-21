from pygame import Rect


class Cell(Rect):
    def __init__(self, left: float, top: float, width: float, height: float, text: str = "")-> None:
        super().__init__(left, top, width, height)
        self.text = text
