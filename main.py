from deck import Deck
from game import Game


def main():
    game = Game()
    game.operate_round()
    game.close()


if __name__ == "__main__":
    main()
