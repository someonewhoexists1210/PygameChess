import socket
import pickle

class Network:
    def __init__(self, ty='game'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'pychess.someonewhoexists.hackclub.app' 
        self.port = 12145
        self.addr = (self.server, self.port)
        self.connect()
        self.client.send(str.encode(ty))
        if ty == 'db':
            self.client.recv(2048)
        else:
            self.p = self.client.recv(1024).decode()

    def getP(self):
        return self.p

    def getIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('209.58.169.47', 8080))
        ip = s.getsockname()[0]
        s.close()
        del s
        return ip

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
            
    def send(self, data):
        self.client.send(str.encode(data))
        return pickle.loads(self.client.recv(2048*2))

    def close(self):
        try:
            self.client.close()
            return 'Connection closed successfully'
        except:
            return "Error closing connection"
        
    def db(self, ty, table, cols=(), vals=()):
        self.client.send(f'{ty}| {table}| {cols}| {vals}'.encode())
        try:
            return self.client.recv(4096).decode()
        finally:
            self.client.close()

        
        