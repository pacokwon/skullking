from skullconstants import DEBUG, HEADER_SIZE, SkullEnum
from validators import choose_validator, yohoho_validator
import pickle
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
        self.send(msg_type="out", msg_data=f"{Player.ID} Users connected")

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
        message += "---------------------------"

        self.send("out", message)

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
        self.send(
            msg_type="in",
            msg_data=f"Player {self.id + 1} - Choose Card: ( 1 ~ {len(self.cards)} ): ",
            msg_validator=choose_validator,
            payload={"theme": theme_of_table, "cards": self.cards},
        )

        try:
            reply = self.receive()
            chosen = int(reply["payload"])
        except ValueError:
            print("ValueError! Received non-integer data from client")
            return None

        return self.cards.pop(chosen - 1)

    def yohoho(self):
        """
        Yohoho!
        The user guesses how many 'games' ze thinks ze will win in the current round
        """
        self.show_cards()
        self.send(
            msg_type="in",
            msg_data=f"Player {self.id + 1} - Yo ho ho!: ",
            msg_validator=yohoho_validator,
        )

    def send(self, msg_type, msg_data, msg_validator=None, payload=None):
        """
        send data to client
        params:
            msg_type: type of message
            msg_data: actual data meant to be sent to the client
            msg_validator: name of validator function
            payload: additional payload

        the three parameters form a dictionary called 'data'.
        'data' has three keys:
            1) type: str
                the value corresponding to this key is either 'in' or 'out'
            2) message: str
                If the 'type' attribute is 'in', then the message acts as a
                prompt before receiving input
                If the 'type' attribute is 'out', then the message is printed
                to stdout(the console)
            3) validator: object
                The validator function. None if validation is
                not necessary.
            4) payload: object
                Additional payload to be used freely
        """
        pickled = pickle.dumps(
            {
                "type": msg_type,
                "message": msg_data,
                "validator": msg_validator,
                "payload": payload,
            }
        )

        if DEBUG:
            if len(pickled) > HEADER_SIZE:
                print(f"Pickled length {len(pickled)} exceeds HEADER_SIZE")

        header = f"{len(pickled):<{HEADER_SIZE}}".encode("utf-8")
        self.sock.send(header + pickled)

    def receive(self):
        """
        Receive data from client socket

        returns:
            unpickled python object from client socket
        """
        try:
            data_size = self.sock.recv(HEADER_SIZE)
            if not len(data_size):
                return False

            data_size = int(data_size.decode("utf-8"))
            return pickle.loads(self.sock.recv(data_size))
        except:
            return False

    def __repr__(self):
        """
        repr function of Player class
        """
        rpr = f"\nPlayer {self.id}:\n"
        for card in self.cards:
            rpr += f"\t{card},\n"

        return rpr
