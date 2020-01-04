from deck import Deck
from game import Game


def main():
    game = Game(3)
    for _ in range(10):
        game.operate_round()


if __name__ == "__main__":
    # deck = Deck()
    # game = Game(3)
    # game.operate_round()
    # print(game.winners())
    main()
