import select
import socket
import struct
import numpy as np
from _pickle import dumps, loads

# ref : https://swf.com.tw/?p=1201


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


class Server:
    def __init__(self, port):

        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        self.port = port

        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64*1024)

        self.sock.bind((self.ip, self.port))
        self.sock.setblocking(0)  # socket設成「非阻塞」模式
        self.sock.listen(5)
        self.inputs = [self.sock]
        self.log = "Server Listen on {0}:{1}".format(
            self.ip, self.port)

    def recv(self, sock):
        dataSizeByte = recvall(sock, struct.calcsize('i'))
        dataSize = struct.unpack('i', dataSizeByte)[0]

        dataByte = recvall(sock, dataSize)

        data = loads(dataByte)
        return data

    def update(self):
        readable, _, _ = select.select(self.inputs, [], [], 0.001)

        data = None
        for sck in readable:
            if sck is self.sock:
                client, addr = sck.accept()
                client.setblocking(0)
                self.inputs.append(client)
            else:
                try:
                    data = self.recv(sck)
                except:
                    pass

        return data

    def stop(self):
        self.sock.close()
