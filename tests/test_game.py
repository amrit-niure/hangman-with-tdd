"""
Hangman Game Unit Tests

This module contains comprehensive unit tests for the Hangman game implementation,
following Test-Driven Development (TDD) principles. The tests cover all core
functionality including game initialization, guess processing, win/loss conditions,
and edge cases.

Test Coverage Areas:
    - Game initialization and setup

Author: Amrit Niure
StudentId: 396426
Date: 3 September 2025
Course: PRT582 Software Engineering Process and Tools
Assignment: A2 Individual Software Unit Testing Report (30%)
"""
from src.game import Game, MaskingMode


def test_initial_masking_word():
    """
    games takes three arguments, the trarget letter , number
    of lives given , and the masking mode.
    when initiated, with these arguments, it should reveal all
    underscores and should have 3 remaining lives.
    """
    g = Game("Python", lives=3, masking_mode=MaskingMode.WORD)

    assert g.reveal == "______"
    assert g.remaining_lives == 3
