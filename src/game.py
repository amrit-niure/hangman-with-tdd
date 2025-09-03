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
from dataclasses import dataclass
from typing import Optional, Set


class MaskingMode(Enum):
    """
    Enumeration for different masking modes in the Hangman game.

    WORD: Masks individual words (spaces remain visible)
    PHRASE: Masks entire phrases including spaces
    """
    WORD = auto()
    PHRASE = auto()


@dataclass(frozen=True)
class GuessResult:
    """
    Immutable data class representing the result of a player's guess.

    This class encapsulates all the information about a guess attempt,
    following the principle of data encapsulation and immutability.

    Attributes:
        outcome (str): The result of the guess - "correct", "incorrect",
                      "timeout", "repeat", "invalid", or "quit"
        revealed (str): Current state of the word/phrase with guessed letters shown
        remaining_lives (int): Number of lives remaining after this guess
        won (bool): True if the game is won after this guess
        lost (bool): True if the game is lost after this guess
    """
    outcome: str  # "correct", "incorrect", "timeout", "repeat", "invalid", "quit"
    revealed: str
    remaining_lives: int
    won: bool
    lost: bool


class Game:
    """
    Main Hangman Game Class

    This class implements the core game logic for Hangman, managing the game state,
    processing guesses, and determining win/loss conditions. It follows object-oriented
    design principles with clear separation of concerns.

    """
    def __init__(
            self,
            target: str,
            lives: int = 6,
            masking_mode: MaskingMode = MaskingMode.WORD,
            valid_chars: str = "abcdefghijklmnopqrstuvwxyz") -> None:
        """
        Initialize a new Hangman game.

        Args:
            target (str): The word or phrase to be guessed (case-insensitive)
            lives (int): Number of incorrect guesses allowed (default: 6)
            masking_mode (MaskingMode): How to mask the target (WORD or PHRASE)
            valid_chars (str): Characters that are considered valid guesses

        Raises:
            ValueError: If target is empty or not a string

        Examples:
            >>> game = Game("python", lives=5)
            >>> game = Game("hello world", masking_mode=MaskingMode.PHRASE)
        """
        # Input validation - ensure target is valid
        if not target or not isinstance(target, str):
            raise ValueError("Target must be a non-empty string")

        # Store original target for display purposes
        self.target_raw = target
        # Convert to lowercase for consistent comparison
        self.target = target.lower()

        # Game configuration
        self.masking_mode = masking_mode
        self.lives = lives

        # Set of valid characters for input validation
        self._valid_chars = set(valid_chars)

        # Game state - letters that have been guessed
        self._guessed: Set[str] = set()

        # Current revealed state (masked version of target)
        self._reveal_state = self._mask(self.target)

    @property
    def guessed(self) -> Set[str]:
        """
        Get a copy of all letters that have been guessed.

        Returns:
            Set[str]: Immutable copy of guessed letters for encapsulation
        """
        return set(self._guessed)

    @property
    def reveal(self) -> str:
        """
        Get the current revealed state of the target.

        Returns:
            str: The target with unguessed letters masked as underscores
        """
        return self._reveal_state

    @property
    def remaining_lives(self) -> int:
        """
        Get the number of remaining lives.

        Returns:
            int: Number of incorrect guesses still allowed
        """
        return self.lives

    def _mask(self, text: str) -> str:
        """
        Create a masked version of the text with underscores for letters.

        This private method implements the core masking logic, replacing
        alphabetic characters with underscores while preserving spaces
        and punctuation.

        Args:
            text (str): The text to mask

        Returns:
            str: Masked text with letters replaced by underscores
        """
        masked = []
        for ch in text:
            if ch.isalpha():
                masked.append("_")
            else:
                masked.append(ch)
        return "".join(masked)

    def _is_won(self) -> bool:
        """
        Check if the player has won the game.

        A game is won when all alphabetic characters have been revealed
        (no underscores remain in positions where letters should be).

        Returns:
            bool: True if all letters have been guessed correctly
        """
        for t, r in zip(self.target, self._reveal_state):
            if t.isalpha() and r == "_":
                return False
        return True

    def _is_lost(self) -> bool:
        """
        Check if the player has lost the game.

        A game is lost when the player has no remaining lives.

        Returns:
            bool: True if lives have been exhausted
        """
        return self.lives <= 0

    def _apply_reveal(self, letter: str) -> int:
        """
        Reveal all occurrences of a guessed letter in the target.

        This private method updates the reveal state by replacing underscores
        with the correctly guessed letter at all matching positions.

        Args:
            letter (str): The letter to reveal (must be single character)

        Returns:
            int: Number of positions where the letter was newly revealed
        """
        # Input validation
        if not letter or len(letter) != 1:
            return 0

        letter = letter.lower()
        reveal_list = list(self._reveal_state)
        count = 0

        # Check each position in the target
        for i, ch in enumerate(self.target):
            if ch == letter and reveal_list[i] == "_":
                reveal_list[i] = letter
                count += 1

        # Update the reveal state
        self._reveal_state = "".join(reveal_list)
        return count

    def make_guess(self, guess: Optional[str]) -> GuessResult:
        """
            Process a player's guess and return the result.

            This is the main method for game interaction, handling all types of
            input including valid guesses, invalid input, timeouts, and quit commands.
            It implements the core game logic while maintaining game state consistency.

            Args:
                guess (Optional[str]): The player's guess (None indicates timeout)

            Returns:
                GuessResult: Complete information about the guess outcome and game state

            Examples:
                >>> result = game.make_guess("a")
                >>> if result.outcome == "correct":
                ...     print("Good guess!")
            """
        # Handle timeout case (None input)
        if guess is None:
            self.lives -= 1
            return GuessResult(
                outcome="timeout",
                revealed=self._reveal_state,
                remaining_lives=self.lives,
                won=self._is_won(),
                lost=self._is_lost(),
            )

        # Clean and normalize input
        g = guess.strip().lower()
        # Validate input format and characters
        if len(g) != 1 or g not in self._valid_chars:
            return GuessResult(
                outcome="invalid",
                revealed=self._reveal_state,
                remaining_lives=self.lives,
                won=self._is_won(),
                lost=self._is_lost(),
            )
        # Check for repeated guess
        if g in self._guessed:
            return GuessResult(
                outcome="repeat",
                revealed=self._reveal_state,
                remaining_lives=self.lives,
                won=self._is_won(),
                lost=self._is_lost(),
            )
        # Process new valid guess
        self._guessed.add(g)
        revealed_now = self._apply_reveal(g)

        if revealed_now > 0:
            outcome = "correct"
        else:
            outcome = "incorrect"
            self.lives -= 1

        return GuessResult(
            outcome=outcome,
            revealed=self._reveal_state,
            remaining_lives=self.lives,
            won=self._is_won(),
            lost=self._is_lost(),
        )
