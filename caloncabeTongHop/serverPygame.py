import socket
from _thread import *
import pickle

server = "172.105.226.101"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

listplayer = []

def threaded_client(conn, player):
    vitri = len(listplayer)
    conn.send(pickle.dumps(listplayer))
    listplayer.append([])
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print("Received: ", data)
            dataTongHop = data[:]

            if not data:
                print("Disconnected")
                break
            else:
                if data == "ENDGAME":
                    conn.sendall(pickle.dumps("DIe"))
                    conn.sendall(pickle.dumps("StopConnection"))
                    break
            listplayer[vitri] = dataTongHop
            conn.sendall(pickle.dumps(listplayer))
            print("Sending : ", listplayer)
        except:
            break

    print("Lost connection")

    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, 0))
