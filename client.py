from skullconstants import HOST, PORT
import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))


if __name__ == "__main__":
    main()
