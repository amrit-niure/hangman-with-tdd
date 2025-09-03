"""
Hangman Game Command Line Interface

This module provides the command-line interface for the Hangman game,
implementing a clean and user-friendly terminal-based experience with
enhanced visual feedback and comprehensive error handling.

The UI follows best practices for CLI design including clear prompts,
informative messages, and graceful error handling.

Author: Amrit Niure
StudentId: 396426
Date: 3 September 2025
Course: PRT582 Software Engineering Process and Tools
"""


def print_welcome_banner() -> None:
    """
    Display an attractive welcome banner for the game.

    Provides visual appeal and clear game identification using ASCII art
    and formatted text to create a professional user experience.
    """
    print("=" * 60)
    print("🎯 WELCOME TO HANGMAN - TEST DRIVEN DEVELOPMENT EDITION 🎯")
    print("=" * 60)
    print("│  Name: Amrit Niure                                      │")
    print("│  StudentId: 396426                                      │")
    print("│  A classic word-guessing game built with TDD principles │")
    print("│  Course: PRT582 Software Engineering Process and Tools  │")
    print("│  Charles Darwin University - S2 2025                    │")
    print("=" * 60)
    print()


def main() -> None:
    """
    Main entry point for the Hangman game CLI.

    Handles command-line arguments, initializes the game, manages the
    game loop, and provides comprehensive user interaction with enhanced
    visual feedback and professional presentation.
    """

    # Display welcome banner and game information
    print_welcome_banner()


if __name__ == "__main__":
    main()
