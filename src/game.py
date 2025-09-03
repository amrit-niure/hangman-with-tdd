"""
Hangman Game Core Module

This module contains the core game logic for the Hangman game, implementing
Test-Driven Development (TDD) principles. It provides the main Game class
along with supporting enums and data structures.

Author: Charles Darwin University Software Engineering Student
Date: September 2025
Course: PRT582 Software Engineering Process and Tools
"""

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
    """
    Main Hangman Game Class
    
    This class implements the core game logic for Hangman, managing the game state,
    processing guesses, and determining win/loss conditions. It follows object-oriented
    design principles with clear separation of concerns.
    
    """
    def __init__(self, target, lives=6, masking_mode=MaskingMode.WORD):
        self.target = target.lower()
        self.lives = lives
        self.masking_mode = masking_mode
        self._reveal_state = "".join("_" if ch.isalpha() else ch for ch in self.target)

    @property
    def reveal(self) -> str:
        return self._reveal_state
    @property
    def remaining_lives(self) -> int:
        return self.lives
    