"""
Hangman Game Package

This package contains a complete implementation of the classic Hangman word-guessing
game, developed using Test-Driven Development (TDD) principles and best practices
in software engineering.

Package Structure:
    - game.py: Core game logic and state management
    - ui_cli.py: Command-line user interface

The implementation demonstrates:
    - Object-oriented design principles
    - Test-driven development methodology
    - Clean code practices with comprehensive documentation
    - Modular architecture with separation of concerns
    - Professional CLI user experience

Author: Amrit Niure
StudentId: 396426
Date: 3 September 2025
Course: PRT582 Software Engineering Process and Tools
Assignment: A2 Individual Software Unit Testing Report (30%)

"""

# Package version information
__version__ = "1.0.0"
__author__ = "Amrit Niure"
__course__ = "PRT582 Software Engineering Process and Tools"
__assignment__ = "A2 Individual Software Unit Testing Report"


from .game import Game, MaskingMode


__all__ = [
    "Game",
    "MaskingMode"
]
