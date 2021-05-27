import pickle
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.2.58"
        self.port = 65432
        # self.client.get
        self.mineIP = ""
        self.addr = ()
        self.p = ""

    def getPlayerInfor(self):
        print("toi ne ", self.port)
        self.addr = (self.server, self.port)
        self.p = self.connect()
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()
        except socket.error as e:
            print("Hok the ket noi ", e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            data = pickle.loads(self.client.recv(2048))
            return data
            # tuong ung voi dautayXY (mau sac, vi tri)
        except socket.error as e:
            print(e)
            print("soc")
        except EOFError as f:
            print(f)
            print("Connection Closed")


