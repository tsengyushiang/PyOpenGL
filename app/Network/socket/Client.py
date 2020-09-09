import socket
import struct
import math


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffsize = self.sock.getsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF)
        print(self.buffsize)
        self.tryAgainTime = 100
        self.waitTime = 0

    def send(self, data):

        dataByte = data.toBytes()

        MAX_IMAGE_DGRAM = self.buffsize-64
        size = len(dataByte)
        num_of_segments = int(math.ceil(size/(MAX_IMAGE_DGRAM)))
        array_pos_start = 0
        print(size)
        while num_of_segments:
            array_pos_end = min(size, array_pos_start + MAX_IMAGE_DGRAM)
            self.sock.sendto(
                struct.pack("I", num_of_segments) +
                dataByte[array_pos_start:array_pos_end],
                (self.ip, self.port)
            )
            array_pos_start = array_pos_end
            num_of_segments -= 1

    def stop(self):
        self.sock.close()
