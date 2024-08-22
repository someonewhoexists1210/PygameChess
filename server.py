import socket
from _thread import *
import pickle
from game import Game


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()
del s


server = ip
port = 1000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId, addr):
    global idCount
    conn.send(str.encode(str(p)))
    ended = False

    while True:
        try:
            data = conn.recv(4096).decode()


            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                if game.ended():
                    conn.sendall(pickle.dumps(game))
                    ended = True
                    break
                else:
                    if data == 'get':
                        conn.sendall(pickle.dumps(game))
                    elif 'p-' in data:
                        game.players[p] = data.split('p-')[1]
                        conn.sendall(pickle.dumps(game))
                    elif '1/2-1/2' in data or  '1-0' in data or '0-1' in data:
                        data = data.split(',')
                        game.setResult(data[0], data[1])
                        conn.sendall(pickle.dumps(game))
                    elif 'draw' in data:
                        game.draw(data.split(',')[1])
                        conn.sendall(pickle.dumps(game))
                    elif 'resign' in data:
                        game.resign(data.split(',')[1])
                        conn.sendall(pickle.dumps(game))

                    elif data == 'abort':
                        game.abort()
                        conn.sendall(pickle.dumps(game))

                    else:
                        data = data.split(',')
                        game.play(data[0], data[1])
                        conn.sendall(pickle.dumps(game))
                        
            else:
                break
        except Exception as e:
            print(e)
            break
    if not ended:
        print("Lost connection to " + str(addr))
        try:
            del games[gameId]
            print("Closing Game", gameId)
        except:
            pass
    else:
        print(f'Game {gameId} ended ({str(game.endby).capitalize()}) ({game.result})')
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId, addr))