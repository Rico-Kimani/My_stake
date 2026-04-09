from deck import Deck
from players import Player


class Game:
    """Manages the flow and state of a poker game between a human player and a computer opponent."""

    def __init__(self):
        self.pots = {"main": 0, "current": 0}
        self.main_pot = 0
        self.current_pot = 0
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

        current_bet = 0

    # Human turn
        action = self.human.get_action(current_bet)
        if action == "fold":
            print("You folded. PC wins.")
            return False

        elif action == "call":
            bet = current_bet

        elif action == "raise":
            bet = int(input("Enter raise amount: "))
            current_bet = bet

        self.human.amount -= bet
        self.human.update_amount_bet(bet)

    # PC turn
        pc_action = self.pc.get_action(current_bet)

        if pc_action == "fold":
            print("PC folded. You win!")
            return False

        elif pc_action == "call":
            pc_bet = current_bet

        elif pc_action == "raise":
            pc_bet = current_bet + 50
            current_bet = pc_bet
            print(f"PC raises to {pc_bet}")

        self.pc.amount -= pc_bet
        self.pc.update_amount_bet(pc_bet)

    # Update pot
        self.current_pot = bet + pc_bet
        self.main_pot += self.current_pot

        print(f"Pot is now: {self.main_pot}")
        return True 
    

    def next_betting_round(self):
        """Execute a betting round after the flop, turn, or river."""
        print(f"\n--- {self.stage.upper()} BETTING ROUND ---")

        current_bet = 0

    # Human
        action = self.human.get_action(current_bet, can_check=True)

        if action == "check":
            human_bet = 0

        elif action == "raise":
            human_bet = int(input("Enter raise amount: "))
            current_bet = human_bet

        self.human.amount -= human_bet
        self.human.update_amount_bet(human_bet)

    # PC
        pc_action = self.pc.get_action(current_bet, can_check=True)

        if pc_action == "check":
            pc_bet = 0

        elif pc_action == "raise":
            pc_bet = current_bet + 50
            print(f"PC raises to {pc_bet}")

        self.pc.amount -= pc_bet
        self.pc.update_amount_bet(pc_bet)

    # Update pot
        self.current_pot = human_bet + pc_bet
        self.main_pot += self.current_pot
        
        print(f"Pot is now: {self.main_pot}")

    # -------------------------
    # COMMUNITY CARDS
    # -------------------------
    def deal_flop(self):
        """Deal the flop (first three community cards)."""
        print("\n--- FLOP ---")
        self.stage = "flop"

        self.deck .burn_card()  # burn a card before the flop

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
        self.next_betting_round()

        # Turn
        self.deal_turn()
        self.next_betting_round()

        # River
        self.deal_river()
        self.next_betting_round()

        self.determine_winner()


        print("\n--- END OF ROUNDS ---")


    def get_highest_card(self, cards):
        """Return the index of the highest card value from a list of cards."""
        values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        
        max_value = -1
        
        for card in cards:
            val = values.index(card.rank)
            if val > max_value:
                max_value = val
                
        return max_value
    
    def determine_winner(self):
        """Determine the winner by comparing player hands and award the pot to the winner."""
        print("\n--- SHOWDOWN ---")

        self.show_player_cards()
        self.show_pc_cards()

        human_score = self.get_highest_card(self.human.cards + self.community_cards)
        pc_score = self.get_highest_card(self.pc.cards + self.community_cards)

        if human_score > pc_score:
            print("You win!")
            self.human.amount += self.main_pot

        elif pc_score > human_score:
            print("PC wins!")
            self.pc.amount += self.main_pot

        else:
            print("Draw!")


if __name__ == "__main__":
    game = Game()
    game.play_round()