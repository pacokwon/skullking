from functools import partial
from skullconstants import HEADER_SIZE, HOST, PORT
import pickle
import select
import socket
import sys


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    while True:
        readable, _, _ = select.select([client], [], [])

        if readable:
            message = receive_data(client)

            if message is False:
                print("Closing game...")
                sys.exit()

            operate_action(client, message)


def operate_action(client, data):
    if data["type"] == "in":
        is_valid = partial(data["validator"], data["payload"])
        while True:
            chosen = input(data["message"])
            if is_valid(chosen):
                break
        send_data(client, {"payload": int(chosen)})

    else:
        print(data["message"])


def receive_data(client):
    """
    Receive data from the server

    params:
        client: a client socket
    returns:
        a python dictionary that follows the rules of 'data'
        as described in the 'send' function of player.py
    """
    try:
        data_size = client.recv(HEADER_SIZE)
        if not len(data_size):
            return False

        data_size = int(data_size.decode("utf-8"))
        return pickle.loads(client.recv(data_size))

    except:
        return False


def send_data(client, data):
    """
    send data to client
    params:
        client: a client socket
        data: python dictionary
    """
    pickled = pickle.dumps(data)
    header = f"{len(pickled):<{HEADER_SIZE}}".encode("utf-8")
    client.send(header + pickled)


if __name__ == "__main__":
    main()
