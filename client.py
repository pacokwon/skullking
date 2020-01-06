from skullconstants import HEADER_SIZE, HOST, PORT
import pickle
import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    while True:
        pass


def receive_message(client):
    try:
        message_size = client.recv(HEADER_SIZE)
        if not len(message_size):
            return False

        message_size = int(message_size.decode("utf-8"))
        return pickle.loads(client.recv(message_size))

    except:
        return False


def send_message(client, data):
    """
    send message to client
    params:
        client: client socket
        data: python dictionary
    """
    pickled = pickle.dumps(data)
    encoded_data = pickled.encode("utf-8")
    header = f"{len(encoded_data):<{HEADER_SIZE}}".encode("utf-8")
    client.send(header + encoded_data)


if __name__ == "__main__":
    main()
