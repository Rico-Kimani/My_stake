from game import Game


def play_game():
    """Start and run a round of the Texas Hold'em game."""

    while True:
        game = Game()
        
        print("\n=== TEXAS HOLD'EM ===")
        
        game.play_round()

        play_again = input("Play another round? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break



if __name__ == "__main__":
    play_game() 