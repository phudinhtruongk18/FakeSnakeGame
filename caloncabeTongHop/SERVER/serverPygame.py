import random
import socket
from _thread import *
import pickle
from DauTayServer import StrawberryServer

server = "192.168.2.58"
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
    color = "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
    return color


def findNameByID(ID):
    print(ID, "<- i nhan vao")
    print(namesIDs)
    try:
        for tenMasv in namesIDs:
            if tenMasv[1] == ID:
                color2 = random_color2()
                return tenMasv[0], color2
        return ID, "#ffb6c1"
    except Exception as aaaa:
        print("loi encode", aaaa)
        return ID, "#ffb6c1"


def guitraThongTin(connTemp):
    ID = pickle.loads(connTemp.recv(2048))
    du_lieu_gui_di_nek = (findNameByID(ID))
    connTemp.sendall(pickle.dumps(du_lieu_gui_di_nek))
    print("Sending Infor : ", du_lieu_gui_di_nek)


def threaded_client(connTemp, addrTemp):
    vitri = len(listplayer)
    connTemp.send(str.encode(addrTemp[0]))
    print("ip la ", addrTemp[0])
    guitraThongTin(connTemp)
    listplayer.append([])
    data = None
    while True:
        try:
            data = pickle.loads(connTemp.recv(2048))
            print("Received: ", data)
            ip_tang_diem = None
            if not data:
                print("Disconnected")
                break
            headXY = data[1][0]
            if is_va_cham_le(headXY[0], headXY[1], dautay.x, dautay.y):
                dautay.move()
                ip_tang_diem = addrTemp

            du_lieu_rieng = data[:]
            du_lieu_rieng.append((dautay.x, dautay.y))
            listplayer[vitri] = du_lieu_rieng
            du_lieu_gui_di = (ip_tang_diem, (dautay.x, dautay.y), listplayer)
            connTemp.sendall(pickle.dumps(du_lieu_gui_di))
            print("Sending : ", du_lieu_gui_di)
        except Exception as ex:
            print(ex)
            break
    print("Lost connection")
    connTemp.close()
    if "ENDGAME" in data:
        data_player = str(data).split("ENDGAME")
        file = open("data/playerData.txt", "a", encoding="utf8")
        file.write(str(data_player) + "\n")


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, addr))