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


def test_initial_masking_phrase():
    """
    Test that phrase masking correctly handles multi-word content.

    Ensures that PHRASE masking mode preserves spaces and punctuation
    while masking only alphabetic characters.
    """
    g = Game("clean code!", lives=3, masking_mode=MaskingMode.PHRASE)
    assert g.reveal == "_____ ____!"  # spaces/punct stay visible


def test_correct_guess_reveals_all_occurrences():
    """
    Test that a correct guess reveals all instances of the letter.

    Verifies that when a letter appears multiple times in the target,
    all occurrences are revealed simultaneously without losing lives.
    """
    g = Game("testing", lives=5)
    res = g.make_guess("t")
    assert res.outcome == "correct"
    assert res.revealed.count("t") == 2
    assert res.remaining_lives == 5


def test_incorrect_guess_loses_life():
    """
    Test that incorrect guesses properly decrement remaining lives.

    Ensures the game correctly handles wrong guesses by reducing
    the life count and maintaining proper game state.
    """
    g = Game("python", lives=2)
    res = g.make_guess("z")
    assert res.outcome == "incorrect"
    assert res.remaining_lives == 1


def test_timeout_loses_life():
    """
    Test that timeout conditions are handled correctly.

    Verifies that when a player doesn't guess within the time limit
    (simulated by None input), a life is lost and game state is updated.
    """
    g = Game("python", lives=1)
    res = g.make_guess(None)  # simulate timer expiry
    assert res.outcome == "timeout"
    assert res.remaining_lives == 0
    assert res.lost


def test_repeat_guess_marked_repeat_no_life_loss():
    """
    Test that repeat guesses are identified without penalty.

    Ensures that guessing the same letter twice doesn't result in
    additional life loss, maintaining fair gameplay.
    """
    g = Game("hangman", lives=3)
    assert g.make_guess("a").outcome == "correct"
    res = g.make_guess("a")
    assert res.outcome == "repeat"
    assert res.remaining_lives == 3
