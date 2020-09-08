import socket
import struct

from _pickle import dumps, loads

# https://kuanyuchen.gitbooks.io/python3-tutorial/content/er_jin_zhi_chu_li_fang_shi.html


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket()

        try:
            self.sock.connect((ip, port))
            self.log = ("{0}:{1} connect successfully.".format(ip, port))
        except:
            self.sock = None
            self.log = ("{0}:{1} server not found.".format(ip, port))

    def send(self, data):

        if(self.sock == None):
            return

        dataByte = dumps(data.toArr())
        dataLenByte = struct.pack('i', len(dataByte))

        self.sock.send(dataLenByte)
        self.sock.send(dataByte)

    def stop(self):

        if(self.sock == None):
            return

        self.sock.close()
