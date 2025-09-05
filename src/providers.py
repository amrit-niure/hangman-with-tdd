"""
Hangman Game Providers Module

This module provides the words and phrases to the main game Module,
i have used the provider pattern to encapsulate the required and to provide it to the game.
It also has a timed input mechanism for user interaction.

"""

from __future__ import annotations

import random
import threading
import time
from pathlib import Path
from typing import Optional

# Path to the data directory containing word and phrase files
DATA_DIR = Path(__file__).resolve().parents[1] / "data"


class RandomWordProvider:
    """
    Provider class for random single words from a text file.
    This class implements the provider pattern to supply random words
    for the basic Hangman game mode. It reads from a configurable
    text file and returns random selections.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        """
        Initialize the word provider with a data source.

        Args:
            path (Optional[Path]): Path to the words file. If None,
                                 defaults to data/words.txt
        """
        self.path = (path or DATA_DIR / "words.txt")

    def get(self) -> str:
        """
        Get a random word from the data file.

        Reads the entire file, filters out empty lines, and returns
        a randomly selected word. This method ensures clean data
        by stripping whitespace and removing empty entries.

        Returns:
            str: A randomly selected word

        Raises:
            FileNotFoundError: If the words file doesn't exist
            IndexError: If the file is empty or contains no valid words
        """
        # Read the entire file content
        text = self.path.read_text(encoding="utf-8")

        # Split into lines and clean up whitespace
        lines = text.splitlines()
        stripped_lines = [w.strip() for w in lines]

        # Filter out empty lines for data quality
        words = [w for w in stripped_lines if w]

        # Return a random selection
        return random.choice(words)

    def __len__(self) -> int:
        """Return the number of available words."""
        text = self.path.read_text(encoding="utf-8")
        return len([w.strip() for w in text.splitlines() if w.strip()])

    def __repr__(self) -> str:
        return f"<RandomWordProvider source={self.path}>"


class RandomPhraseProvider:
    """
    Provider class for random phrases from a text file.

    This class provides random phrases for the intermediate Hangman
    game mode, handling multi-word content that may include spaces
    and punctuation.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        """
        Initialize the phrase provider with a data source.

        Args:
            path (Optional[Path]): Path to the phrases file. If None,
                                 defaults to data/phrases.txt
        """
        self.path = (path or DATA_DIR / "phrases.txt")

    def get(self) -> str:
        """
        Get a random phrase from the data file.

        Similar to RandomWordProvider but handles multi-word content
        including spaces, punctuation, and longer text strings.

        Returns:
            str: A randomly selected phrase

        Raises:
            FileNotFoundError: If the phrases file doesn't exist
            IndexError: If the file is empty or contains no valid phrases
        """
        # Read the entire file content
        text = self.path.read_text(encoding="utf-8")

        # Split into lines and clean up whitespace
        lines = text.splitlines()
        stripped_phrases = [p.strip() for p in lines]

        # Filter out empty lines for data quality
        phrases = [p for p in stripped_phrases if p]

        # Return a random selection
        return random.choice(phrases)

    def __len__(self) -> int:
        """Return the number of available words."""
        text = self.path.read_text(encoding="utf-8")
        return len([w.strip() for w in text.splitlines() if w.strip()])

    def __repr__(self) -> str:
        return f"<RandomWordProvider source={self.path}>"


class TimedInput:
    """
    Thread-safe input handler with timeout functionality and countdown display.

    This class provides a mechanism for reading user input with a specified
    timeout, essential for the timed gameplay feature. It uses threading
    to avoid blocking the main game loop while waiting for input and displays
    a visual countdown timer.

    The implementation follows thread-safety principles and handles
    edge cases like EOF and timeout conditions gracefully.
    """

    def __init__(self) -> None:
        """
        Initialize the timed input handler.

        Sets up the internal buffer for thread-safe communication
        between the input thread and the main game thread.
        """
        self._buffer: Optional[str] = None
        self._input_received = False

    def _reader(self, prompt: str) -> None:
        """
        Internal method to read input in a separate thread.

        This private method runs in a daemon thread to read user input
        without blocking the main thread. It handles EOF gracefully
        and stores the result in the internal buffer.

        Args:
            prompt (str): The prompt message to display to the user
        """
        try:
            # Attempt to read user input
            self._buffer = input(prompt)
            self._input_received = True
        except EOFError:
            # Handle end-of-file (Ctrl+D) gracefully
            self._buffer = None
            self._input_received = True

    def get(self, prompt: str, timeout_seconds: int) -> Optional[str]:
        """
        Get user input with a timeout mechanism and visual countdown.

        This method creates a separate thread for input reading to avoid
        blocking the main thread. If the user doesn't provide input within
        the specified timeout, it returns None. Shows a countdown timer
        to create urgency and improve user experience.

        Args:
            prompt (str): The message to display to the user
            timeout_seconds (int): Maximum time to wait for input

        Returns:
            Optional[str]: The user's input, or None if timeout occurred

        Examples:
            >>> timed = TimedInput()
            >>> result = timed.get("Enter guess: ", 10)
            >>> if result is None:
            ...     print("Timeout occurred!")
        """
        # Reset the state for a fresh read
        self._buffer = None
        self._input_received = False

        # Display the initial prompt
        print(prompt, end="", flush=True)

        # Create and start the input reading thread
        # Using daemon=True ensures the thread doesn't prevent program exit
        thread = threading.Thread(target=self._reader, args=("",), daemon=True)
        thread.start()

        # Show countdown timer
        for remaining in range(timeout_seconds, 0, -1):
            if self._input_received:
                break

            # Clear the current line and show countdown
            print(f"\r{prompt}⏱️  {remaining}s ", end="", flush=True)
            time.sleep(1)

        # Wait a bit more to see if input comes in the last moment
        if not self._input_received:
            time.sleep(0.1)

        # Clear the countdown line
        print(f"\r{prompt}{'':20}", end="", flush=True)

        # Check if input was received in time
        if self._input_received:
            print(f"\r{prompt}{self._buffer}")  # Show what was typed
            return self._buffer

        print(f"\r{prompt}⏰ TIMEOUT!")  # Show timeout message
        return None

    def last_input(self) -> Optional[str]:
        """Return the last input received (or None if none)."""
        return self._buffer

    def __repr__(self) -> str:
        return f"<TimedInput received={self._input_received} buffer={self._buffer}>"
