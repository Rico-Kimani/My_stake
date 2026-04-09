import random
import time


class Player:
    """Represents a player in the poker game."""

    def __init__(self, type="pc", cards=None, total_amount_bet=0, name="", amount=0):
        self.name = name
        self.type = type
        self.cards = cards if cards else []
        self.total_amount_bet = total_amount_bet
        self.amount = amount

    def place_initial_bet(self):
        """Prompts the player to place an initial bet and returns the bet amount."""
        while True:
            amount = input(f"Place initial bet. Current amount is {self.amount}: ")

            if amount.isdigit():
                n = int(amount)

                if 1 <= n <= self.amount:
                    self.amount -= n
                    return n

                print(f"Invalid amount. Enter between 1 and {self.amount}")
            else:
                print("Enter a valid number")

    def auto_match_or_raise(self, amount):
        """Automatically decides whether the PC should match or raise the given amount."""
        print("PC thinking...")
        time.sleep(2)

        # 1 = match, 2 = raise
        decision = random.randint(1, 2)

        raise_amount = amount + random.randint(10, 100)

        # If PC cannot afford raise → force match
        if raise_amount > self.amount:
            decision = 1

        # MATCH
        if decision == 1:
            if self.amount >= amount:
                self.amount -= amount
                print(f"PC matches: {amount}")
                return amount
            else:
                print("PC folds")
                return "fold"

        # RAISE
        self.amount -= raise_amount
        print(f"PC raises to {raise_amount}")
        return raise_amount
    
    def get_action(self, current_bet, can_check=False):
        if self.type == "human":
            while True:
                if can_check:
                    action = input("Choose action [check / raise]: ").lower()
                    if action in ["check", "raise"]:
                        return action
                else:
                    action = input("Choose action [call / fold / raise]: ").lower()
                    if action in ["call", "fold", "raise"]:
                        return action
                
                print("Invalid action. Try again.")
                
        else:
            import random
            if can_check:
                return random.choice(["check", "raise"])
            return random.choice(["call", "fold", "raise"])

    def update_amount_bet(self, amount):
        """Updates the total amount bet by adding the given amount."""
        self.total_amount_bet += amount

    def reset_amount_bet(self):
        """Resets the total amount bet to zero."""
        self.total_amount_bet = 0


if __name__ == "__main__":
    player = Player(type="human", name="John", amount=2000)

    bet = player.place_initial_bet()
    print("You bet:", bet)

    pc = Player(type="pc", name="AI", amount=2000)

    pc_action = pc.auto_match_or_raise(bet)
    print("PC action:", pc_action)

if __name__ == "__main__":
    p = Player(type="human", amount=1000)
    action = p.get_action(100)
    print("Action:", action)