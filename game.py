class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.whites_turn = True
        self.last_move = ['', 1]
        self.whitewantsdraw = False
        self.blackwantsdraw = False
        self.result = None
        self.moves = []
        self.aborted = False
        self.players = ['', '']
        self.endby = ''

    def connected(self):
        return self.ready

    def getLastMove(self):
        return self.last_move
    
    def play(self, mv, pl):
        self.last_move = [mv, int(pl)]
        self.whitewantsdraw = False
        self.blackwantsdraw = False
        self.moves.append(mv)
    
    def draw(self, color):
        if color == 'white':
            self.whitewantsdraw = True
        elif color == 'black':
            self.blackwantsdraw = True
        if self.whitewantsdraw and self.blackwantsdraw:
            self.setResult('1/2-1/2', 'agreement')

    def abort(self):
        self.aborted = True
        self.setResult('0-0', 'Aborted')

    def setResult(self, res, by):
        self.result = res
        self.endby = by
    
    def resign(self, color):
        self.setResult('1-0' if color == 'black' else '0-1', 'resignation')
        
    def ended(self) -> bool:
        return self.result != None or self.aborted  
    
    
