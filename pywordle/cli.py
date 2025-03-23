import sys
from typing import Optional
from models.game import Game
from models.letter import Letter


class WordleCLI:
    def __init__(self):
        self.game = Game()
        self.attempts = 0
        self.max_attempts = 6

    def display_board(self) -> None:
        """Display the current state of the game board"""
        print("\n" + "=" * 30)
        # print the status of each guess
        for guess in self.game.board.guesses:
            self.display_guess_result(guess.letters)
        print("=" * 30 + "\n")

    def get_valid_guess(self) -> Optional[str]:
        """Get a valid guess from the user"""
        while True:
            guess = input("Enter your guess (5 letters): ").strip().lower()

            if guess == "quit":
                return None

            if len(guess) != 5:
                print("Guess must be 5 letters long!")
                continue

            if not guess.isalpha():
                print("Guess must contain only letters!")
                continue

            return guess

    def display_letter_status(
        self, letter: str, is_correct: bool, is_present: bool
    ) -> str:
        """Display a letter with appropriate formatting"""
        if is_correct:
            return f"\033[92m{letter.upper()}\033[0m"  # Green
        elif is_present:
            return f"\033[93m{letter.upper()}\033[0m"  # Yellow
        else:
            return f"\033[90m{letter.upper()}\033[0m"  # Gray

    def display_guess_result(self, guess: list[Letter]) -> None:
        """Display the result of a guess with colored output"""
        result = []
        for letter in guess:
            result.append(self.display_letter_status(str(letter), letter.is_correct, letter.is_present))
        print(" ".join(result))

    def play(self) -> None:
        """Main game loop"""
        print("\nWelcome to Wordle!")
        print("Type 'quit' to exit the game")
        print(f"You have {self.game.max_attempts} attempts to guess the 5-letter word\n")

        while not self.game.game_over:
            self.display_board()

            guess = self.get_valid_guess()
            if guess is None:
                print(f"\nYou quit! The word was: {self.game.answer.upper()}")
                break

            try:
                self.game.make_guess(guess)
                self.display_guess_result(self.game.board.guesses[-1].letters)

                if self.game.won:
                    print(f"\nCongratulations! You won in {len(self.game.board.guesses)} attempts!")
                    break

            except ValueError as e:
                print(f"Error: {e}")
                continue

        print(f"\nGame Over! The word was: {self.game.answer.upper()}")


def main():
    """Entry point for the CLI game"""
    try:
        cli = WordleCLI()
        cli.play()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
