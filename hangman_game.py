"""
Task 1: Hangman Game
---------------------
A text-based version of the classic Hangman game.
- Uses a predefined list of words.
- Allows the user to guess letters one at a time.
- Tracks remaining attempts and displays the word progress.
"""

import random

HANGMAN_PICS = [
    """
       ------
       |    |
       |
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    --------
    """,
]

WORD_LIST = [
    "python", "hangman", "developer", "keyboard", "internship",
    "algorithm", "function", "variable", "computer", "django",
    "database", "practice", "challenge", "software", "network",
]

MAX_ATTEMPTS = len(HANGMAN_PICS) - 1


def choose_word(word_list):
    """Randomly select a word from the predefined list."""
    return random.choice(word_list).lower()


def display_progress(word, guessed_letters):
    """Show the word with guessed letters revealed and others as underscores."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def get_guess(guessed_letters):
    """Prompt the user for a single valid letter guess."""
    while True:
        guess = input("Guess a letter: ").lower().strip()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).")
        elif guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
        else:
            return guess


def play_hangman():
    word = choose_word(WORD_LIST)
    guessed_letters = set()
    wrong_guesses = 0

    print("=" * 50)
    print("WELCOME TO HANGMAN")
    print("=" * 50)
    print(f"The word has {len(word)} letters. You have {MAX_ATTEMPTS} wrong guesses allowed.\n")

    while wrong_guesses < MAX_ATTEMPTS:
        print(HANGMAN_PICS[wrong_guesses])
        print("Word: " + display_progress(word, guessed_letters))
        print(f"Wrong guesses: {wrong_guesses}/{MAX_ATTEMPTS}")
        if guessed_letters:
            print("Guessed letters: " + ", ".join(sorted(guessed_letters)))
        print()

        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in word:
            print(f"Good guess! '{guess}' is in the word.\n")
            if all(letter in guessed_letters for letter in word):
                print(HANGMAN_PICS[wrong_guesses])
                print(f"Word: {' '.join(word)}")
                print("\nCongratulations! You guessed the word correctly!")
                print(f"The word was: {word}")
                return
        else:
            wrong_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.\n")

    print(HANGMAN_PICS[wrong_guesses])
    print("You've run out of attempts! Game over.")
    print(f"The word was: {word}")


def main():
    play_again = "y"
    while play_again == "y":
        play_hangman()
        play_again = input("\nDo you want to play again? (y/n): ").lower().strip()
    print("\nThanks for playing Hangman! Goodbye.")


if __name__ == "__main__":
    main()
