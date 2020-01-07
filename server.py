from skullconstants import ACCEPT_TIMEOUT_SECONDS, HOST, MAX_USERS, PORT
import select
import socket
import time


class Server:
    def __init__(self):
        """
        Server class constructor
        Initialize sockets, configure socket settings and
        accept clients for ACCEPT_TIMEOUT_SECONDS
        """
        self.client_sockets = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen()
        end_time = time.time() + ACCEPT_TIMEOUT_SECONDS
        print("Accepting Connections...")
        while time.time() < end_time:
            read_sockets, _, _ = select.select([self.server], [], [], 0)  # non-blocking
            if read_sockets:
                client, _ = self.server.accept()
                self.client_sockets[client] = len(self.client_sockets)

                if len(self.client_sockets) == MAX_USERS:
                    break

        print(f"{len(self.client_sockets)} users connected")

    def close(self):
        for sock in self.client_sockets:
            sock.close()

