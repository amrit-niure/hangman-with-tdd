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

import argparse
from .providers import RandomWordProvider, RandomPhraseProvider, TimedInput
from .game import MaskingMode, Game


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


def print_game_rules(mode: str, timeout: int) -> None:
    """
    Display comprehensive game rules and instructions.

    Args:
        mode (str): The game mode (basic or intermediate)
        timeout (int): Timeout period for each guess
    """
    print("📋 GAME RULES:")
    print("─" * 40)
    print(f"• Mode: {mode.upper()}")
    print(f"• Time limit: {timeout} seconds per guess")
    print("• Guess one letter at a time")
    print("• Type 'quit' to exit the game")
    print("• Invalid guesses don't count against you")
    print("• Repeated guesses are ignored")
    print()


def print_hangman_art(lives_remaining: int) -> None:
    """
    Display ASCII art hangman based on remaining lives.

    Provides visual feedback about the game state through traditional
    hangman gallows artwork that updates as lives are lost.

    Args:
        lives_remaining (int): Number of lives left (0-6)
    """
    # Hangman art stages (6 lives to 0 lives)
    stages = [
        # 0 lives - game over
        """
        ┌───┐
        │   │
        │   O
        │  /│\\
        │  / \\
        │
        """,
        # 1 life
        """
        ┌───┐
        │   │
        │   O
        │  /│\\
        │  /
        │
        """,
        # 2 lives
        """
        ┌───┐
        │   │
        │   O
        │  /│\\
        │
        │
        """,
        # 3 lives
        """
        ┌───┐
        │   │
        │   O
        │  /│
        │
        │
        """,
        # 4 lives
        """
        ┌───┐
        │   │
        │   O
        │   │
        │
        │
        """,
        # 5 lives
        """
        ┌───┐
        │   │
        │   O
        │
        │
        │
        """,
        # 6 lives - full lives
        """
        ┌───┐
        │   │
        │
        │
        │
        │
        """
    ]

    # Ensure we have a valid index (clamp between 0 and 6)
    stage_index = max(0, min(6, lives_remaining))
    print(stages[6 - stage_index])


def print_game_status(game: Game, guessed_letters: set) -> None:
    """
    Display comprehensive game status information.

    Args:
        game (Game): The current game instance
        guessed_letters (set): Set of letters already guessed
    """
    print("🎮 GAME STATUS:")
    print("─" * 40)
    print(f"Word/Phrase: {game.reveal}")
    print(f"Lives remaining: {'_' * game.remaining_lives} ({game.remaining_lives}/6)")

    if guessed_letters:
        sorted_letters = sorted(list(guessed_letters))
        print(f"Letters guessed: {', '.join(sorted_letters)}")
    else:
        print("Letters guessed: None yet")
    print()


def print_guess_feedback(result) -> None:
    """
    Provide detailed feedback for each guess attempt.

    Args:
        result: GuessResult object containing outcome information
    """
    feedback_messages = {
        "correct": "🎉 EXCELLENT! That letter is in the word!",
        "incorrect": "❌ Oops! That letter isn't in the word. Life lost!",
        "timeout": "⏰ TIME'S UP! You didn't guess in time. Life lost!",
        "repeat": "🔄 You already tried that letter. Try a different one!",
        "invalid": "⚠️  Please enter a single letter (a-z only)."
    }

    message = feedback_messages.get(result.outcome, f"Unknown outcome: {result.outcome}")
    print(message)
    print()


def main() -> None:
    """
    Main entry point for the Hangman game CLI.

    Handles command-line arguments, initializes the game, manages the
    game loop, and provides comprehensive user interaction with enhanced
    visual feedback and professional presentation.
    """
    # Set up command-line argument parsing with detailed help
    parser = argparse.ArgumentParser(
        description="Hangman Game - TDD Edition",
        epilog="Example: python -m src.ui_cli --mode intermediate --lives 8 --timeout 20"
    )

    parser.add_argument(
        "--mode",
        choices=["basic", "intermediate"],
        default="basic",
        help="Game difficulty: 'basic' for single words, 'intermediate' for phrases"
    )

    parser.add_argument(
        "--lives",
        type=int,
        default=6,
        help="Number of incorrect guesses allowed (default: 6)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Time limit for each guess in seconds (default: 15)"
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Display welcome banner and game information
    print_welcome_banner()
    print_game_rules(args.mode, args.timeout)

    # Initialize game based on selected mode
    if args.mode == "basic":
        target = RandomWordProvider().get()
        masking = MaskingMode.WORD
        print("🎯 Starting BASIC mode - Guess the word!")
    else:
        target = RandomPhraseProvider().get()
        masking = MaskingMode.PHRASE
        print("🎯 Starting INTERMEDIATE mode - Guess the phrase!")

    print(f"📝 You have {args.lives} lives and {args.timeout} seconds per guess.")
    print()

    # Initialize game components
    game = Game(target=target, lives=args.lives, masking_mode=masking)
    timed = TimedInput()

    # Main game loop with enhanced UI
    while not game.is_finished():
        # Display current game status
        print_hangman_art(game.remaining_lives)
        print_game_status(game, game.guessed)

        # Get user input with timeout
        print("💭 What's your guess?")
        guess = timed.get("   Enter a letter (or 'quit' to exit): ", timeout_seconds=args.timeout)

        # Process the guess
        result = game.make_guess(guess)

        # Handle quit command
        if result.outcome == "quit":
            print("👋 Thanks for playing! You chose to quit the game.")
            print(f"📖 The answer was: '{game.target_raw}'")
            print("🎮 Come back and play again soon!")
            return

        # Provide feedback for the guess
        print_guess_feedback(result)

        # Check for game end conditions
        if result.won:
            print("🏆" * 20)
            print("🎉 CONGRATULATIONS! YOU WON! 🎉")
            print("🏆" * 20)
            print(f"✨ You successfully guessed: '{game.target_raw}'")
            print(f"💪 Lives remaining: {result.remaining_lives}")
            print(f"🎯 Total guesses made: {len(game.guessed)}")
            print("🌟 Excellent work! You're a Hangman champion!")
            return

        elif result.lost:
            print_hangman_art(0)  # Show final hangman
            print("💀" * 20)
            print("😵 GAME OVER - YOU LOST! 😵")
            print("💀" * 20)
            print(f"📖 The answer was: '{game.target_raw}'")
            print("🎯 Better luck next time! Practice makes perfect.")
            print("� Try again to improve your skills!")
            return

        # Add separator between rounds for clarity
        print("─" * 60)
        print()


if __name__ == "__main__":
    main()
