from random import shuffle
from SkullCard import *

class Deck:
    SIZE = sum(Sizes.values())
    def __init__(self):
        self.deck = []
        self.deck += [WhiteFlag() for _ in range(Sizes["WHITE"])]
        self.deck += [RedFlag(i + 1) for i in range(Sizes["RED"])]
        self.deck += [GreenFlag(i + 1) for i in range(Sizes["GREEN"])]
        self.deck += [BlueFlag(i + 1) for i in range(Sizes["BLUE"])]
        self.deck += [BlackFlag(i + 1) for i in range(Sizes["BLACK"])]
        self.deck += [Mermaid() for _ in range(Sizes["MERMAID"])]
        self.deck += [Pirate() for _ in range(Sizes["PIRATE"])]
        self.deck += [GreenPirate() for _ in range(Sizes["GREENPIRATE"])]
        self.deck += [SkullKing() for _ in range(Sizes["SKULLKING"])]
        self.shuffle()
        self.dealt = []

    def deal(self):
        if not self.deck:
            self.deck = self.dealt
            self.dealt = []
            shuffle(self.deck)

        return self.deck.pop()

    def shuffle(self):
        shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def __repr__(self):
        rpr = "[\n"
        for card in self.deck:
            rpr += f"\t{card},\n"
        rpr += "]"

        return rpr
