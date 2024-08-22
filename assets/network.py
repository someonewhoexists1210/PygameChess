import socket
import pickle

class Network:
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = self.getIp()
        self.port = 1000
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p
    
    def getIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
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
        
        
        