class Player:
    """
    Player class
    A player has cards, and id and a score
    """
    ID = 0
    def __init__(self):
        self.cards = []
        self.id = Player.ID
        Player.ID += 1
        self.score = 0

    def set_cards(self, cards):
        self.cards = cards

    def show_cards(self):
        print("------- CARDS --------")
        for idx, card in enumerate(self.cards):
            print(f"{idx + 1}:\t{card}")
        print("----------------------\n")

    def choose(self):
        """
        Show the player's cards and make the player choose a card
        """
        self.show_cards()
        chosen = input(f"Player {self.id} - Choose Card: ( 1 ~ {len(self.cards)} ): ")
        while not ( chosen.isdecimal() and 1 <= int(chosen) <= len(self.cards) ):
            print(f"Choose a number between 1 and {len(self.cards)}")
            chosen = input(f"Player {self.id} - Choose Card: ( 1 ~ {len(self.cards)} ): ")

        return self.cards.pop(int(chosen) - 1)

    def yohoho(self):
        """
        Yohoho!
        """
        self.show_cards()
        chosen = input(f"Player {self.id} - Yo ho ho!: ")
        while not chosen.isdecimal():
            print(f"Choose a number!")
            chosen = input(f"Player {self.id} - Yo ho ho!: ")

        return int(chosen)

    def __repr__(self):
        rpr = f"Player {self.id}:\n"
        rpr += "[\n"
        for card in self.cards:
            rpr += f"\t{card},\n"
        rpr += "]"

        return rpr
