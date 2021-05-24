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


def threaded_client(conn, player):
    vitri = len(listplayer)
    conn.send(pickle.dumps(listplayer))
    listplayer.append([])
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print("Received: ", data)

            if not data:
                print("Disconnected")
                break
            else:
                if data == "ENDGAME":
                    conn.sendall(pickle.dumps("DIe"))
                    conn.sendall(pickle.dumps("StopConnection"))
                    break
            # headX,headY = data[1]          [0] van de la so sanh voi cai cua no chu khong phai vi tri dau tien
            headXY = data[1][0]
            if is_va_cham_le(headXY[0],headXY[1],dautay.x,dautay.y):
                dautay.move()
            data.append((dautay.x,dautay.y))
            listplayer[vitri] = data
            du_lieu_gui_di = ((dautay.x,dautay.y),listplayer)
            conn.sendall(pickle.dumps(du_lieu_gui_di))
            print("Sending : ", du_lieu_gui_di)
        except:
            break
    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, 0))
