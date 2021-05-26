import random
import socket
from _thread import *
import pickle
from DauTayServer import StrawberryServer

server = "139.162.49.190"
port = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

listplayer = []

dautay = StrawberryServer(26)


def is_va_cham_le(x1, y1, x2, y2):
        if x2 <= x1 < x2 + 26:
            if y2 <= y1 < y2 + 26:
                return True
        return False

namesIDs = []
with open("C:\\Users\\Administrator\\pygame\\data\\users.txt", "r", encoding="utf8") as f:
    x = f.read()
    z = x.rstrip().split("\n")
    for nameWithID in z:
        nameID = nameWithID.split("\t")
        namesIDs.append(nameID)


def random_color2():
    color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color


def findNameByID(ID):
    print(ID,"<- i nhan vao")
    print(namesIDs)
    try:
        for tenMasv in namesIDs:
            if tenMasv[1] == ID:
                color2 = random_color2()
                return tenMasv[0],color2
        return ID,"#ffb6c1"
    except Exception as aaaa:
        print("loi encode",aaaa)
        return ID,"#ffb6c1"


def guitraThongTin(conn):
    ID = pickle.loads(conn.recv(2048))
    du_lieu_gui_di_nek = (findNameByID(ID))
    conn.sendall(pickle.dumps(du_lieu_gui_di_nek))
    print("Sending Infor : ", du_lieu_gui_di_nek)


def threaded_client(conn, addr):
    vitri = len(listplayer)
    conn.send(str.encode(addr[0]))
    print("ip la ",addr[0])
    guitraThongTin(conn)
    listplayer.append([])
    data = None
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print("Received: ", data)
            ip_tang_diem = None
            if not data:
                print("Disconnected")
                break
            headXY = data[1][0]
            if is_va_cham_le(headXY[0],headXY[1],dautay.x,dautay.y):
                dautay.move()
                ip_tang_diem = addr

            du_lieu_rieng = data[:]
            du_lieu_rieng.append((dautay.x,dautay.y))
            listplayer[vitri] = du_lieu_rieng
            du_lieu_gui_di = (ip_tang_diem,(dautay.x,dautay.y),listplayer)
            conn.sendall(pickle.dumps(du_lieu_gui_di))
            print("Sending : ", du_lieu_gui_di)
        except:
            break
    print("Lost connection")
    conn.close()
    if "ENDGAME" in data:
        data_player = str(data).split("ENDGAME")
        f = open("data/playerData.txt", "a", encoding="utf8")
        f.write(str(data_player)+"\n")


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, addr))
