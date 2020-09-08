import select
import socket
import struct
import numpy as np
from _pickle import dumps, loads

# ref : https://swf.com.tw/?p=1201


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


class Server:
    def __init__(self, port):

        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        self.port = port

        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 128*1024)

        self.sock.bind((self.ip, self.port))
        self.sock.setblocking(0)  # socket設成「非阻塞」模式
        self.sock.listen(5)
        self.inputs = [self.sock]
        self.log = "waiting clients on server {0}:{1}".format(
            self.ip, self.port)

    def recv(self, sock):
        dataSizeByte = recvall(sock, struct.calcsize('i'))
        dataSize = struct.unpack('i', dataSizeByte)[0]

        dataByte = recvall(sock, dataSize)

        data = loads(dataByte)
        return data

    def getInputs(self):
        readable, _, _ = select.select(self.inputs, [], [], 0.001)

        data = None
        for sck in readable:
            if sck is self.sock:
                client, addr = sck.accept()
                client.setblocking(0)
                print(addr)
                self.inputs.append(client)
            else:
                try:
                    data = self.recv(sck)
                except:
                    data = None

        return data

    def stop(self):
        self.sock.close()
