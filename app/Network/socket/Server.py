import select
import socket
import struct
import numpy as np
from _pickle import dumps, loads
import threading

# ref : https://medium.com/@fromtheast/fast-camera-live-streaming-with-udp-opencv-de2f84c73562


class Server:
    def __init__(self, port):

        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        self.port = port
        print("{0}:{1}".format(self.ip,self.port))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.inputs = [self.sock]
        self.log = "Server Listen on {0}:{1}".format(
            self.ip, self.port)

        self.buffer = {}
        self.notUsedData = {}
        self.running = True
        self.waitDataThread = threading.Thread(target=self.waitClientDatas)
        self.waitDataThread.start()

    def getLatestBytes(self):
        data = []
        for keys in self.notUsedData:
            dataBytes = self.notUsedData[keys]
            if(dataBytes != None):
                data.append(dataBytes)
            self.notUsedData[keys] = None

        return data

    def waitClientDatas(self):
        headerSize = 4
        while self.running:
            data, client_address = self.sock.recvfrom(64*1024)
            if(client_address not in self.buffer):
                self.buffer[client_address] = b""

            if struct.unpack("I", data[0:headerSize])[0] > 1:
                self.buffer[client_address] += data[headerSize:]
            else:
                self.buffer[client_address] += data[headerSize:]
                self.notUsedData[client_address] = self.buffer[client_address]
                self.buffer[client_address] = b""

    def stop(self):
        self.sock.close()
        self.running = False
        self.waitDataThread.join()
