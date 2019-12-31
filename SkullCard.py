from SkullConstants import SkullEnum, Sizes

class SkullCard(object):
    """
    Base class for types of cards in the game
    """
    CARDTYPE = None
    def __repr__(self):
        return f"{self.CARDTYPE}"

class NumberCard(SkullCard):
    def __repr__(self):
        return f"{self.CARDTYPE} {self.number}"

class WhiteFlag(SkullCard):
    CARDTYPE = SkullEnum.WHITE
    SIZE = Sizes["WHITE"]

class RedFlag(NumberCard):
    CARDTYPE = SkullEnum.RED
    SIZE = Sizes["RED"]
    def __init__(self, number):
        self.number = number

class GreenFlag(NumberCard):
    CARDTYPE = SkullEnum.GREEN
    SIZE = Sizes["GREEN"]
    def __init__(self, number):
        self.number = number

class BlueFlag(NumberCard):
    CARDTYPE = SkullEnum.BLUE
    SIZE = Sizes["BLUE"]
    def __init__(self, number):
        self.number = number

class BlackFlag(NumberCard):
    CARDTYPE = SkullEnum.BLACK
    SIZE = Sizes["BLACK"]
    def __init__(self, number):
        self.number = number

class Mermaid(SkullCard):
    CARDTYPE = SkullEnum.MERMAID
    SIZE = Sizes["MERMAID"]

class Pirate(SkullCard):
    CARDTYPE = SkullEnum.PIRATE
    SIZE = Sizes["PIRATE"]

class GreenPirate(SkullCard):
    CARDTYPE = SkullEnum.GREENPIRATE
    SIZE = Sizes["GREENPIRATE"]

class SkullKing(SkullCard):
    CARDTYPE = SkullEnum.SKULLKING
    SIZE = Sizes["SKULLKING"]

