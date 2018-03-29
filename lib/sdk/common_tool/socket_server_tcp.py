import sys
from socket import *


class SocketServerTCP:

    def __init__(self, bind_port):
        self.port = int(bind_port)
        self.host = ''
        self.buff_size = 1024
        self.server_socket = socket(AF_INET, SOCK_STREAM)

    def create_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(0)
        while True:
            self.server_socket.accept()

    def __del__(self):
        self.server_socket.close()


if __name__ == '__main__':
    port = sys.argv[1]
    eg = SocketServerTCP(port)
    eg.create_server()
    pass
