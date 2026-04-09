from deck import Deck
from players import Player


class Game:
    """Manages the flow and state of a poker game between a human player and a computer opponent."""

    def __init__(self):
        self.pots = {"main": 0, "current": 0}
        self.stage = "pre-flop"   # track current stage o a game

        # Initialize deck
        self.deck = Deck()
        self.deck.shuffle()

        # Deal cards
        human_cards = [self.deck.give_card(), self.deck.give_card()]
        pc_cards = [self.deck.give_card(), self.deck.give_card()]

        # Initialize players
        self.human = Player(
            type="human",
            cards=human_cards,
            total_amount_bet=0,
            name="You",
            amount=2000
        )

        self.pc = Player(
            type="pc",
            cards=pc_cards,
            total_amount_bet=0,
            name="PC",
            amount=2000
        )

        self.turn = self.human   # human starts
        self.community_cards = []

    # -------------------------
    # SHOW CARDS
    # -------------------------
    def show_player_cards(self):
        """Display the human player's cards."""
        print("\nYour Cards:")
        for card in self.human.cards:
            card.print_card()

    def show_pc_cards(self):
        """Display the computer player's cards."""
        print("\nPC Cards:")
        for card in self.pc.cards:
            card.print_card()

    # -------------------------
    # TURN SWITCHING
    # -------------------------
    def switch_turn(self):
        """Switch the turn between the human player and the computer player."""
        if self.turn == self.human:
            self.turn = self.pc
        else:
            self.turn = self.human

    # -------------------------
    # FIRST BETTING ROUND
    # -------------------------
    def first_betting_round(self):
        """Execute the first betting round where human and PC place initial bets."""
        print("\n--- FIRST BETTING ROUND ---")

        human_bet = self.human.place_initial_bet()
        self.human.update_amount_bet(human_bet)

        pc_bet = self.pc.auto_match_or_raise(human_bet)

        if pc_bet == "fold":
            print("PC folded. You win!")
            return False

        self.pc.update_amount_bet(pc_bet)

        self.pots["current"] = human_bet + pc_bet
        self.pots["main"] += self.pots["current"]

        print(f"Current pot: {self.pots['main']}")
        return True

    # -------------------------
    # COMMUNITY CARDS
    # -------------------------
    def deal_flop(self):
        """Deal the flop (first three community cards)."""
        print("\n--- FLOP ---")
        self.stage = "flop"

        for _ in range(3):
            self.community_cards.append(self.deck.give_card())

        self.show_community_cards()

    def deal_turn(self):
        """Deal the turn (fourth community card)."""
        print("\n--- TURN ---")
        self.stage = "turn"

        self.community_cards.append(self.deck.give_card())
        self.show_community_cards()

    def deal_river(self):
        """Deal the river (fifth and final community card)."""
        print("\n--- RIVER ---")
        self.stage = "river"

        self.community_cards.append(self.deck.give_card())
        self.show_community_cards()

    def show_community_cards(self):
        """Display all community cards currently on the table."""
        print("Community Cards:")
        for card in self.community_cards:
            card.print_card()

    # -------------------------
    # SIMPLE ROUND FLOW
    # -------------------------
    def play_round(self):
        """Execute a complete poker round from dealing cards through to the river."""
        self.show_player_cards()

        # 1st betting round
        if not self.first_betting_round():
            return

        # Flop
        self.deal_flop()

        # Turn
        self.deal_turn()

        # River
        self.deal_river()

        print("\n--- END OF ROUND ---")
        print("Winner ideation to be implemented....")


if __name__ == "__main__":
    game = Game()
    game.play_round()