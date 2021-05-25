import socket
from _thread import *
import pickle
from DauTayServer import StrawberryServer

server = "172.105.226.101"
port = 6969

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
#
# def xu_ly_va_cham(listplayer):
#     if listplayer is not None:
#         print(len(listplayer), "cchieu dai")
#         for player in listplayer:
#             if is_va_cham_le(player.x,player.x):
#                 player.increase_length()
#                 return True
#         return False


def threaded_client(conn, addr):
    vitri = len(listplayer)
    conn.send(str.encode(addr[0]))
    print("ip la ",addr[0])
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
        f = open("data/playerData.txt", "a")
        f.write(str(data_player)+"\n")


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, addr))
