from Deck import Deck
from Player import Player
from SkullConstants import SkullEnum

class Game:
    """
    Game class
    Some terminology:
        This program consists of 10 'rounds',
        each of which have N 'games' where N is the current round number
    """
    def __init__(self, nplayers):
        """
        Game class constructor

        params:
            nplayers: number of players in this game
        """
        self.round_count = 3
        self.goes_first = 0
        self.deck = Deck()
        self.players = [Player() for _ in range(nplayers)]
        self.yohoho = [0 for _ in range(nplayers)]
        self.debug = True

    def operate_round(self):
        """
        Operate a single round
        """
        # initialize each players' win counts for this round
        wins_count = [0] * len(self.players)

        # deal cards
        for player in self.players:
            player.set_cards([self.deck.deal() for _ in range(self.round_count)])

        if self.debug:
            print("Deal Complete")
            print(self.players)

        # yo ho ho!
        for ith, player in enumerate(self.players):
            self.yohoho[ith] = player.yohoho()

        # operate games
        for _ in range(self.round_count):
            self.goes_first = self.operate_game()
            wins_count[self.goes_first] += 1

        # update score
        for ith, tup in enumerate(zip(self.yohoho, wins_count)):
            if tup[0] == tup[1]:
                self.players[ith].score += 10 * self.round_count if tup[0] == 0 else 20 * tup[0]
            else:
                self.players[ith].score -= 10 * abs(tup[0] - tup[1])

        for ith, player in enumerate(self.players):
            print(f"Player {ith}\t{player.score}")

        self.round_count += 1

    def operate_game(self):
        """
        Operate a single game

        params:
            there are no parameters
        returns:
            the id of the winner
        """
        choices = []

        player_idx = 0
        # take turns choosing a card
        while player_idx < len(self.players):
            who_goes_idx = (self.goes_first + player_idx) % len(self.players)
            chosen = self.players[who_goes_idx].choose() # choose() returns a card object

            if self.debug:
                print(f"Player {who_goes_idx} chose {chosen}")

            choices.append(chosen)
            player_idx += 1

        # evaluate winner of this game
        self.goes_first = ( self.evaluate_winner(choices) + len(self.players) - self.goes_first ) % len(self.players)
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

        rgb_tuple = ( SkullEnum.RED, SkullEnum.GREEN, SkullEnum.BLUE )
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
            return False if TYPE2 in ( SkullEnum.PIRATE, SkullEnum.GREENPIRATE ) else True

        elif TYPE1 == SkullEnum.PIRATE or TYPE1 == SkullEnum.GREENPIRATE:
            # 18 combinations
            return False if TYPE2 == SkullEnum.SKULLKING else True

        elif TYPE1 in rgb_tuple: # 9
            if TYPE2 in rgb_tuple:
                return card1.number > card2.number if TYPE1 == TYPE2 else True
            elif TYPE2 in (
                SkullEnum.BLACK,
                SkullEnum.MERMAID,
                SkullEnum.PIRATE,
                SkullEnum.GREENPIRATE,
                SkullEnum.SKULLKING
            ):
                return False

            return True # white

        elif TYPE1 == SkullEnum.BLACK: # 9
            if TYPE2 == SkullEnum.WHITE or TYPE2 in rgb_tuple:
                return True

            elif TYPE2 == SkullEnum.BLACK:
                return card1.number > card2.number

            return False

    def evaluate_winner(self, choices):
        """
        Evaluate the winner among the list of SkullCard objects

        params:
            choices: list of SkullCard objects

        returns:
            the index of the winner
        """
        theme = None
        winning = -1
        theme_tuple = ( SkullEnum.RED, SkullEnum.GREEN, SkullEnum.BLUE, SkullEnum.BLACK )

        for idx, choice in enumerate( choices ):
            if self.debug:
                print(f"Player {idx}'s turn")

            if theme == None and choice.CARDTYPE in theme_tuple:
                theme = choice.CARDTYPE
                if self.debug:
                    print(f"The turn's theme became {theme}")

            if winning == -1:
                if choice.CARDTYPE != SkullEnum.WHITE:
                    winning = idx
                    if self.debug:
                        print(f"Player {idx} is the leader of this turn")
                continue

            if not self.evaluate_two(choices[winning], choices[idx]):
                if self.debug:
                    print(f"Player {idx} {choices[idx]} & Player {winning} {choices[winning]} Evaluation -> Winner is Player {choices[idx]}")
                winning = idx


        if self.debug:
            print(f"Winner of this turn is Player {winning}, with {choices[winning]}")

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
        max_idx = 0
        max_score = self.players[0].score
        winners = []
        for idx, player in enumerate(self.players):
            if max_score == player.score:
                winners.append(player)
            elif max_score > player.score:
                winners = [player]

        return tuple(winners)

