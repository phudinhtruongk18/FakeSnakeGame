import socket
from _thread import *
from snake import Snake
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


# players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]
# players = ["nguoichoi0","nguoichoi1","nguoichoi2","nguoichoi3","nguoichoi4","nguoichoi5"]
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
            # players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                # if player == 1:
                #     reply = players[0]
                # else:
                #     reply = players[1]
                if data == "ENDGAME":
                    conn.sendall(pickle.dumps("DIe"))
                    conn.sendall(pickle.dumps("StopConnection"))
                    break
            print(dataTongHop)
            listplayer[vitri] = dataTongHop
            conn.sendall(pickle.dumps(listplayer))
            print("Sending : ", listplayer)
        except:
            break

    print("Lost connection")

    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1