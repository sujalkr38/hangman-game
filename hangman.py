"""
Simple Hangman game — run this file:  python hangman.py
"""

import random

# Words the game can pick from (all lowercase for easy matching)
WORDS = [
    "python",
    "computer",
    "keyboard",
    "monitor",
    "program",
    "variable",
    "function",
    "string",
    "number",
    "puzzle",
    "garden",
    "planet",
    "rocket",
    "ocean",
    "tiger",
    "eagle",
    "castle",
    "bridge",
    "window",
    "shadow",
]

# How many wrong guesses before you lose
MAX_WRONG_GUESSES = 6


def pick_random_word():
    """Return one random word from WORDS."""
    return random.choice(WORDS)


def show_word_with_blanks(word, guessed_letters):
    """
    Show the word with letters filled in where guessed,
    and underscores where not guessed yet.
    """
    letters = []
    for char in word:
        if char in guessed_letters:
            letters.append(char.upper())
        else:
            letters.append("_")
    return " ".join(letters)


def is_full_word_guessed(word, guessed_letters):
    """True if every letter in the word was guessed."""
    return all(letter in guessed_letters for letter in word)


def format_guess_list(letters):
    """Turn a set of letters into a sorted string for display."""
    if not letters:
        return "(none)"
    return ", ".join(sorted(letters))


def play_one_game():
    """Run a single round of Hangman."""
    word = pick_random_word()
    guessed_letters = set()  # every letter the player tried
    wrong_letters = set()  # guessed but not in the word

    print("\n" + "=" * 40)
    print("           H A N G M A N")
    print("=" * 40)

    while True:
        remaining = MAX_WRONG_GUESSES - len(wrong_letters)

        print()
        print(show_word_with_blanks(word, guessed_letters))
        print()
        print(f"Remaining tries: {remaining}")
        print(f"Correct guesses: {format_guess_list(guessed_letters - wrong_letters)}")
        print(f"Wrong guesses:   {format_guess_list(wrong_letters)}")
        print()

        # Win: whole word revealed
        if is_full_word_guessed(word, guessed_letters):
            print(f"You won! The word was: {word.upper()}")
            return

        # Lose: too many wrong guesses
        if remaining <= 0:
            print(f"Game over! The word was: {word.upper()}")
            return

        guess = input("Guess a letter: ").strip().lower()

        # Check input is a single letter
        if len(guess) != 1:
            print("Please enter exactly one letter.")
            continue

        if not guess.isalpha():
            print("Only letters A–Z are allowed.")
            continue

        if guess in guessed_letters:
            print(f"You already tried '{guess.upper()}'.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"Good! '{guess.upper()}' is in the word.")
        else:
            wrong_letters.add(guess)
            print(f"Sorry, '{guess.upper()}' is not in the word.")


def main():
    """Start the game and offer to play again."""
    print("Welcome! Try to guess the word before you run out of tries.")
    while True:
        play_one_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y" and again != "yes":
            print("Thanks for playing. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
