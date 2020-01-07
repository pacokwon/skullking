from deck import Deck
from player import Player
from server import Server
from skullconstants import DEBUG, SkullEnum
import select
import socket
import time


class Game:
    """
    Game class
    Some terminology:
        This program consists of 10 'rounds',
        each of which have N 'games' where N is the current round number
    """

    def __init__(self):
        """
        Game class constructor
        """
        self.server = Server()
        self.round_count = 3
        self.goes_first = 0
        self.deck = Deck()
        self.players = [Player(sock) for sock in self.server.client_sockets]
        self.yohoho_list = [0 for _ in self.players]

    def operate_round(self):
        """
        Operate a single round
        """
        if DEBUG:
            print(f"------- Round {self.round_count} Start -------")
        # initialize each players' win counts for this round
        wins_count = [0] * len(self.players)

        # deal cards
        for player in self.players:
            player.set_cards([self.deck.deal() for _ in range(self.round_count)])

        if DEBUG:
            print(f"Deal Complete\n{self.players}")

        self.yohoho()

        # operate games
        for _ in range(self.round_count):
            self.goes_first = self.operate_game()
            wins_count[self.goes_first] += 1

        # update score
        for ith, tup in enumerate(zip(self.yohoho_list, wins_count)):
            if tup[0] == tup[1]:
                self.players[ith].score += (
                    10 * self.round_count if tup[0] == 0 else 20 * tup[0]
                )
            else:
                self.players[ith].score -= 10 * abs(tup[0] - tup[1])

        broadcast_message = f"\n------- Round {self.round_count:<2} standings -------\n"
        for ith, player in enumerate(self.players):
            print(f"Player {ith}\t{player.score}")
            broadcast_message += f"Player {ith}\t{player.score}\n"
        broadcast_message += f"----------------------------------\n"
        self.broadcast(broadcast_message)

        if DEBUG:
            print(f"-------- Round {self.round_count} Fin --------")

        self.round_count += 1

    def yohoho(self):
        """
        Send a yohoho request and asynchronously receive responses
        """
        for ith, player in enumerate(self.players):
            if DEBUG:
                print(f"Sending Yohoho request to player {ith + 1}")
            player.yohoho()

        player_cnt = 0
        while player_cnt < len(self.players):
            readable, _, _ = select.select(self.server.client_sockets, [], [])

            for sock in readable:
                idx = self.server.client_sockets[sock]
                data = self.players[idx].receive()
                if DEBUG:
                    print(f"Received data {data} from client {idx + 1}")
                self.yohoho_list[idx] = data["payload"]
                player_cnt += 1

        if DEBUG:
            print(f"Complete yohoho list is {self.yohoho_list}")

    def operate_game(self):
        """
        Operate a single game

        params:
            there are no parameters
        returns:
            the id of the winner
        """
        cards_on_table = []
        player_idx = 0
        self.broadcast(f"Player {self.goes_first + 1} will go first")
        # take turns choosing a card
        while player_idx < len(self.players):
            who_goes_idx = (self.goes_first + player_idx) % len(self.players)
            chosen = self.players[who_goes_idx].choose(
                self.extract_theme(cards_on_table)
            )  # choose() returns a card object

            if DEBUG:
                print(f"Player {who_goes_idx} chose {chosen}")

            cards_on_table.append(chosen)
            player_idx += 1

        # evaluate winner of this game
        self.goes_first = (
            self.evaluate_winner(cards_on_table) + len(self.players) - self.goes_first
        ) % len(self.players)

        self.broadcast(f"Player {self.goes_first + 1} wins!")

        return self.goes_first

    def evaluate_two(self, card1, card2):
        """
        Evaluate which card is the winner among card1 & card2

        params:
            card1: SkullCard Object 1
            card2: SkullCard Object 2
        returns:
            True    if card1 wins over card2
            False   if card1 loses to card2

        The types of cards goes:
            white, red, green, blue, black, mermaid, pirate, gpirate, skull king

        9 * 9 equals 81!
        However, assuming that there are no duplicate skull kings,
        a total of 80 combinations is possible
        """

        rgb_tuple = (SkullEnum.RED, SkullEnum.GREEN, SkullEnum.BLUE)
        TYPE1 = card1.CARDTYPE
        TYPE2 = card2.CARDTYPE

        if TYPE1 == SkullEnum.WHITE:
            # 9 combinations
            return False

        elif TYPE1 == SkullEnum.SKULLKING:
            # 8 combinations
            return False if TYPE2 == SkullEnum.MERMAID else True

        elif TYPE1 == SkullEnum.MERMAID:
            # 9 combinations
            return False if TYPE2 in (SkullEnum.PIRATE, SkullEnum.GREENPIRATE) else True

        elif TYPE1 == SkullEnum.PIRATE or TYPE1 == SkullEnum.GREENPIRATE:
            # 18 combinations
            return False if TYPE2 == SkullEnum.SKULLKING else True

        elif TYPE1 in rgb_tuple:  # 9
            if TYPE2 in rgb_tuple:
                return card1.number > card2.number if TYPE1 == TYPE2 else True
            elif TYPE2 in (
                SkullEnum.BLACK,
                SkullEnum.MERMAID,
                SkullEnum.PIRATE,
                SkullEnum.GREENPIRATE,
                SkullEnum.SKULLKING,
            ):
                return False

            return True  # white

        elif TYPE1 == SkullEnum.BLACK:  # 9
            if TYPE2 == SkullEnum.WHITE or TYPE2 in rgb_tuple:
                return True

            elif TYPE2 == SkullEnum.BLACK:
                return card1.number > card2.number

            return False

    def evaluate_winner(self, cards_on_table):
        """
        Evaluate the winner among the list of SkullCard objects

        params:
            cards_on_table: list of SkullCard objects

        returns:
            the index of the winner
        """
        theme = None
        winning = -1
        theme_tuple = (SkullEnum.RED, SkullEnum.GREEN, SkullEnum.BLUE, SkullEnum.BLACK)

        if DEBUG:
            print("\n------- Evaluation Start -------")
            print("Cards on Table:")
            print(cards_on_table)

        for idx, choice in enumerate(cards_on_table):
            if DEBUG:
                print(f"\nPlayer {idx}'s turn")

            if theme == None and choice.CARDTYPE in theme_tuple:
                theme = choice.CARDTYPE
                if DEBUG:
                    print(f"\tThe turn's theme became {theme}")

            if winning == -1:
                if choice.CARDTYPE != SkullEnum.WHITE:
                    winning = idx
                    if DEBUG:
                        print(f"\tPlayer {idx} is the leader of this turn")
                continue

            if not self.evaluate_two(cards_on_table[winning], cards_on_table[idx]):
                if DEBUG:
                    print(
                        f"\tPlayer {idx} {cards_on_table[idx]} & Player {winning} {cards_on_table[winning]} Evaluation -> Winner is {cards_on_table[idx]}"
                    )
                winning = idx

        if DEBUG:
            print(
                f"\nWinner of this turn is Player {winning + 1}, with {cards_on_table[winning]}"
            )
            print("-------- Evaluation Fin --------\n")

        return winning

    def winners(self):
        """
        a function that returns a tuple of winners
        the reason the return type is a tuple is because there might be multiple winners

        params:
            there are no parameters
        returns:
            tuple of Player objects
        """
        max_score = self.players[0].score
        winners = []
        for _, player in enumerate(self.players):
            if max_score == player.score:
                winners.append(player)
            elif max_score > player.score:
                winners = [player]

        return tuple(winners)

    def extract_theme(self, cards):
        """
        Extract theme from a list of cards
        params:
            cards: list of SkullCard objects
        returns:
            the theme of the parameter 'cards'
            None if there is no theme
        """
        color_tuple = (SkullEnum.RED, SkullEnum.GREEN, SkullEnum.BLUE, SkullEnum.BLACK)

        for card in cards:
            if card.CARDTYPE in color_tuple:
                return card.CARDTYPE

        return None

    def broadcast(self, message):
        for player in self.players:
            player.send("out", message)

    def close(self):
        self.server.close()

