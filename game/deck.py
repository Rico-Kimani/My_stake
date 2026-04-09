import random

from card import card


class Deck:
    """A class representing a deck of playing cards."""

    def __init__(self):
        self.deck = []
        for suit in card.SUITS:
            for rank in card.RANKS:
                self.deck.append(card(suit, rank))

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.deck)

    def print_deck(self):
        """Print all cards in the deck."""
        print(f"Deck size is {len(self.deck)}")
        print("-------------")
        for card in self.deck:
            card.print_card()

    def give_card(self):
        """Remove and return the top card from the deck."""
        if len(self.deck) == 0:
            return None
        return self.deck.pop(0)

    def burn_card(self):
        """Remove and display the top card as burned."""
        if len(self.deck) > 0:
            burned = self.deck.pop(0)
            print("Burned card:")
            burned.print_card()


if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    deck.print_deck()
    print("\nDealing a card...")
    card = deck.give_card()
    if card:
        card.print_card()
    print("\nBurning a card...")
    deck.burn_card()