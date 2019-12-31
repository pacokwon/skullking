from Deck import Deck
from Game import Game

def main():
    """
    main function of program
    """
    game = Game(3)
    for _ in range(10):
        game.operate_round()

if __name__ == "__main__":
    # deck = Deck()
    # game = Game(3)
    # game.operate_round()
    # print(game.winners())
    main()
