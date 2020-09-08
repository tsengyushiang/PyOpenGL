import socket
import struct

from _pickle import dumps, loads

# https://kuanyuchen.gitbooks.io/python3-tutorial/content/er_jin_zhi_chu_li_fang_shi.html


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket()

        self.tryAgainTime = 100
        self.waitTime = 0
        self.log = 'init...'

        self.connect()

    def connect(self):
        try:
            if(self.waitTime > 0):
                raise

            self.waitTime = self.tryAgainTime
            self.sock = socket.socket()
            self.sock.connect((self.ip, self.port))
            self.log = ("{0}:{1} connect successfully.".format(
                self.ip, self.port))
        except:
            self.log = "{0}:{1} server not found, try reconnect after {2} msec.".format(
                self.ip, self.port, self.waitTime)

        self.waitTime = self.waitTime-1

    def send(self, data):

        try:
            dataByte = dumps(data.toArr())
            dataLenByte = struct.pack('i', len(dataByte))

            self.sock.send(dataLenByte)
            self.sock.send(dataByte)
        except:
            self.connect()

    def stop(self):

        try:
            self.sock.close()
        except:
            pass
