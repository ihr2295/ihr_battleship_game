import random


class Player:
    def __init__(self, name, boardsize, num_ships):
        self.name = name
        self.boardsize = boardsize
        self.num_ships = num_ships
        self.board = [['.'for _ in range(boardsize)] for _ in range(boardsize)]
        self.ships = []
        self.guesses = []
        self.score = 0

    def place_ships(self):
        for _ in range(self.num_ships):
            while True:
                row, col = (
                    random.randint(0, self.boardsize - 1),
                    random.randint(0, self.boardsize - 1),
                )
                if (row, col) not in self.ships:
                    self.ships.append((row, col))
                    self.board[row][col] = '@ '
                    break

    def make_guess(self, opponent):
        while True:
            boarddisplay = (
                f"{self.name}'s Board:\n" + self.displayboard(opponent.guesses)
            )
            guess_prompt = "\nGuess a row: "
            guess = input(boarddisplay + guess_prompt).upper()
            if (not guess.isdigit() or
                int(guess) < 0 or
                    int(guess) >= self.boardsize):
                print(
                    f"Wrong. Enter between 0 and {self.boardsize - 1}")
                continue

            row = int(guess)
            while True:
                guess = input(f"Guess a column for row {row}: ").upper()
                if (not guess.isdigit() or
                    int(guess) < 0 or
                        int(guess) >= self.boardsize):
                    print(
                        f"Wrong. Enter between 0 and {self.boardsize - 1}")
                    continue
                col = int(guess)

                if (row, col) not in self.guesses:
                    self.guesses.append((row, col))
                    if (row, col) in opponent.ships:
                        print(f"{self.name} got a hit!")
                        opponent.board[row][col] = 'X '  # Mark as 'X' for hits
                        self.score += 1  # Assign a point to the player
                        return True
                    else:
                        print(f"{self.name} missed.")
                        opponent.board[row][col] = 'M '  # Update opponent bord
                        return False
                else:
                    print("You've already guessed this coordinate. Try again.")

    def all_ships_sunk(self):
        return len(self.ships) == 0

    def displayboard(self, guesses):
        board_str = ""
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                if (i, j) in guesses:
                    if (i, j) in self.ships:
                        if self.name == "Computer":
                            board_str += '. '  # Hide computer's ship locations
                        else:
                            board_str += 'X '  # Display 'X' for hits
                    else:
                        board_str += 'M '  # Display 'M' for misses
                else:
                    if self.name == "Computer":
                        board_str += '. '  # Hide computer's ship locations
                    else:
                        if (i, j) in self.ships:
                            board_str += '@ '  # Display player's ships
                        else:
                            board_str += '. '  # Not guessed yet
            board_str += '\n'
        return board_str


def welcome_message():
    print("-----------------------------------")
    print(" Welcome to IHR BATTLESHIPS GAME!!")
    print(" Board Size: 5. Number of ships: 4")
    print(" Top left corner is row: 0, col: 0")
    print("-----------------------------------")


def play_game(player, computer):
    player_score = 0
    computer_score = 0
    max_guesses = 10

    while True:
        if (len(player.guesses) >= max_guesses and
                len(computer.guesses) >= max_guesses):
            print("\nMax number of guesses reached. The game is a tie!")
            break

        if len(player.guesses) >= max_guesses:
            print(f"\nMax number of guesses reached. {player.name} loses!")
            break

        if len(computer.guesses) >= max_guesses:
            print("\nMax number of guesses reached. Computer loses!")
            break

        print("\nComputer's Board:")
        # Display computer's board with player's guesses
        print(computer.displayboard(player.guesses))

        player_turn = player.make_guess(computer)

        print(f"\n{player.name} guessed:", player.guesses[-1])
        if player_turn:
            print(f"{player.name} got a hit!")
            player_score += 1  # Assign a point to the player

        if player.all_ships_sunk():
            print(
                f"Congrats, {player.name}! You sank all the ships. You win!")
            break

        computer_turn = False
        computer_guess = (0, 0)  # Initialize to avoid NameError
        while not computer_turn:
            computer_guess = (
                random.randint(0, player.boardsize - 1),
                random.randint(0, player.boardsize - 1),
            )
            if computer_guess not in computer.guesses:
                computer.guesses.append(computer_guess)
                if computer_guess in player.ships:
                    print("Computer guessed:", computer_guess)
                    print("Computer got a hit!")
                    player.board[computer_guess[0]][computer_guess[1]] = 'X '
                    computer_score += 1  # Assign a point to the computer
                else:
                    print("Computer guessed:", computer_guess)
                    print("Computer missed this time.")
                    player.board[computer_guess[0]][computer_guess[1]] = 'M '
                computer_turn = True

        print("-----------------------------------")
        print("After this round, the scores are:")
        print(f"{player.name}: {player_score}. Computer: {computer_score}")
        print("-----------------------------------")

        if computer.all_ships_sunk():
            print("Computer sank all your ships. You lose!")
            break

    # Display the final state of the game boards
    print("\nFinal State of the Game Boards:")
    print(f"{player.name}'s Board:")
    print(player.displayboard(player.guesses))
    print("Computer's Board:")
    print(computer.displayboard(computer.guesses))

    if player_score > computer_score:
        print(f"{player.name} wins!")
    elif player_score < computer_score:
        print(f"{player.name} loses!")
    else:
        print("The game is a tie!")


def play_battleships():
    welcome_message()

    boardsize = 5
    num_ships = 4

    player = Player(input("Please enter your name: "), boardsize, num_ships)
    computer = Player("Computer", boardsize, num_ships)

    player.place_ships()
    computer.place_ships()

    play_game(player, computer)


if __name__ == "__main__":
    play_battleships()
