from dataclasses import dataclass

@dataclass
class Letter:
    char: str
    is_correct: bool
    is_present: bool
    is_absent: bool

    def __str__(self) -> str:
        return self.char
