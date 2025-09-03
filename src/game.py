from enum import Enum, auto

class MaskingMode(Enum):
    """
    Enumeration for different masking modes in the Hangman game.
    
    WORD: Masks individual words (spaces remain visible)
    PHRASE: Masks entire phrases including spaces
    """
    WORD = auto()
    PHRASE = auto()


class Game:
    def __init__(self, target, lives=6, masking_mode=MaskingMode.WORD, valid_chars="abcdefghijklmnopqrstuvwxyz"):
        self.target = target.lower()
        self.lives = lives
        self.masking_mode = masking_mode
        self._reveal_state = "".join("_" if ch.isalpha() else ch for ch in self.target)
    @property
    def reveal(self):
        return self._reveal_state
    @property
    def remaining_lives(self):
        return self.lives