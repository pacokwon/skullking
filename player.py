from skullconstants import HEADER_SIZE, SkullEnum
import socket


class Player:
    """
    Player class
    A player has cards, and id and a score
    """

    ID = 0

    def __init__(self, sock):
        self.cards = []
        self.id = Player.ID
        Player.ID += 1
        self.score = 0
        self.sock = sock

    def set_cards(self, cards):
        """
        Set player's cards
        params:
            cards: player's new set of cards
        """
        self.cards = cards

    def show_cards(self):
        """
        Show the set of cards that this player currently has
        """
        message = ""
        message += f"\n------- Your Cards --------\n"
        for idx, card in enumerate(self.cards):
            message += f"{idx + 1}:\t{card}\n"
        message += "---------------------------\n"

        self.send(message)

        if DEBUG:
            print(message)

    def choose(self, theme_of_table):
        """
        Show the player's cards and make the player choose a card
        params:
            theme_of_table: theme of the cards on the table
        returns:
            SkullCard object chosen by the player
        """
        self.show_cards()
        _has_theme = self.has_theme(theme_of_table)
        special_tuple = (
            SkullEnum.WHITE,
            SkullEnum.MERMAID,
            SkullEnum.PIRATE,
            SkullEnum.GREENPIRATE,
            SkullEnum.SKULLKING,
        )

        idx = 0
        while idx < 1:
            chosen = input(
                f"Player {self.id} - Choose Card: ( 1 ~ {len(self.cards)} ): "
            )
            if not chosen.isdecimal():
                print(f"Choose a number between 1 and {len(self.cards)}")
                idx -= 1
            elif not (1 <= int(chosen) <= len(self.cards)):
                print(f"Choose a number between 1 and {len(self.cards)}")
                idx -= 1
            elif (
                _has_theme
                and self.cards[int(chosen) - 1].CARDTYPE not in special_tuple
                and self.cards[int(chosen) - 1].CARDTYPE != theme_of_table
            ):
                print(
                    f"You have a card of the theme {theme_of_table}. You must choose that card"
                )
                idx -= 1

            idx += 1

        return self.cards.pop(int(chosen) - 1)

    def yohoho(self):
        """
        Yohoho!
        """
        self.show_cards()
        chosen = input(f"Player {self.id + 1} - Yo ho ho!: ")
        while not chosen.isdecimal():
            print(f"Choose a number!")
            chosen = input(f"Player {self.id + 1} - Yo ho ho!: ")

        return int(chosen)

    def has_theme(self, theme):
        """
        evaluate if player's current set of cards has a specific theme
        params:
            theme: the desired theme to investigate on
        returns:
            True if there is a card of the given theme
            False otherwise
        """
        for card in self.cards:
            if card.CARDTYPE == theme:
                return True

        return False

    def send(self, data):
        encoded_data = data.encode("utf-8")
        header = f"{len(encoded_data):<{HEADER_SIZE}}".encode("utf-8")
        self.sock.send(header + encoded_data)

    def __repr__(self):
        """
        repr function of Player class
        """
        rpr = f"\nPlayer {self.id}:\n"
        for card in self.cards:
            rpr += f"\t{card},\n"

        return rpr
