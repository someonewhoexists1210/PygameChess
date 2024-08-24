from _thread import *
import pickle, os, socket
from mys import PostgreSQL
from game import Game

server = ''
port = 12145

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

print(s.getsockname())

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId, addr):
    global idCount
    conn.send(str.encode(str(p)))

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
                        game.abort(p)
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
    if not game.ended():
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
    idCount += 1
    conn.send('Connected'.encode())
    ty = conn.recv(2048).decode()
    print("Connected to:", addr, f'({ty})')
    if ty == 'db':
        conn.send(str.encode(' '))
        db = PostgreSQL('someonewhoexists_pygamechess')
        while True:
            try:
                data = conn.recv(4096).decode()

                data = list(map(str, data.split('| ')))
                ind=0
                for _ in data:
                    if '(' in _:
                        data[ind] = eval(_)
                    ind += 1
                '''
                Data = [Type, Table, Conditions, Values]
                '''

                if data[0] == 'select':
                    if len(data[2]) == 1:
                        res = db.select(data[1], data[2][0], data[3][0])
                    else:
                        res = db.select(data[1], data[2][0], data[3][0], data[2][1], data[3][1], 'AND')
                
                elif data[0] == 'insert':
                    res = db.insert(data[1], data[2], data[3])
                elif data[0] == 'update':
                    res = db.update(data[1], data[2], data[3])
                else:
                    conn.send('Incorrect data'.encode())
                    break

                conn.send(str(res).encode())
                break

            except:
                break
        idCount -= 1
        conn.close()
    else:
        p = 0
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
        else:
            games[gameId].ready = True
            p = 1

        start_new_thread(threaded_client, (conn, p, gameId, addr))
