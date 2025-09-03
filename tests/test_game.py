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


def test_invalid_input_does_not_change_state():
    """
    Test that invalid input is rejected without affecting game state.

    Verifies that multi-character input, numbers, or other invalid
    characters don't alter the game state or consume lives.
    """
    g = Game("code", lives=3)
    res = g.make_guess("ab")  # invalid: more than one char
    assert res.outcome == "invalid"
    assert g.reveal == "____"
    assert g.remaining_lives == 3


def test_win_condition():
    """
    Test that win conditions are properly detected.

    Ensures that when all letters in the target are guessed,
    the game correctly identifies a win state.
    """
    g = Game("aa", lives=5)
    g.make_guess("a")
    assert g.is_finished()
    assert g.reveal == "aa"


def test_lose_condition():
    """
    Test that loss conditions are properly detected.

    Verifies that when all lives are exhausted, the game
    correctly identifies a loss state.
    """
    g = Game("a", lives=1)
    g.make_guess("b")  # wrong
    assert g.is_finished()
    assert g.remaining_lives == 0


def test_quit_command_handling():
    """
    Test that quit commands are properly processed.

    Ensures that typing 'quit' returns the appropriate outcome
    without affecting other game state variables.
    """
    g = Game("test", lives=3)
    res = g.make_guess("quit")
    assert res.outcome == "quit"
    assert res.remaining_lives == 3


def test_case_insensitive_guessing():
    """
    Test that the game handles both uppercase and lowercase input.

    Verifies that letter case doesn't affect guess processing,
    ensuring consistent behavior regardless of input case.
    """
    g = Game("Python", lives=3)
    res_lower = g.make_guess("p")
    assert res_lower.outcome == "correct"

    # Reset for uppercase test
    g2 = Game("Python", lives=3)
    res_upper = g2.make_guess("P")
    assert res_upper.outcome == "correct"


def test_empty_string_invalid():
    """
    Test that empty string input is handled as invalid.

    Ensures that empty or whitespace-only input is properly
    rejected without affecting game state.
    """
    g = Game("test", lives=3)
    res = g.make_guess("")
    assert res.outcome == "invalid"
    assert g.remaining_lives == 3


def test_game_state_consistency():
    """
    Test that game state remains consistent throughout gameplay.

    Verifies that the game maintains proper state consistency
    across multiple guess operations.
    """
    g = Game("hello", lives=6)

    # Make several guesses and verify state consistency
    result1 = g.make_guess("h")  # correct
    assert result1.outcome == "correct"
    assert "h" in g.guessed

    result2 = g.make_guess("x")  # incorrect
    assert result2.outcome == "incorrect"
    assert result2.remaining_lives == 5

    result3 = g.make_guess("e")  # correct
    assert result3.outcome == "correct"
    assert "e" in g.guessed

    # Verify final state
    assert len(g.guessed) == 3
    assert g.remaining_lives == 5
