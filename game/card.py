"""Module for representing a playing card."""

class card:
    """A class representing a standard playing card."""

    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
             "J", "Q", "K", "A"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def print_card(self):
        """Print the card information to the console."""
        print(f"{self.rank} of {self.suit}")

    def get_card_info(self):
        """Return the card information as a string."""
        return f"{self.rank} of {self.suit}"
    
if __name__ == "__main__":
    card = card("Hearts", "A")
    card.print_card()