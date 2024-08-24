import pygame
import sys, math, os
from assets.features import Button, InputBox, Timer
from assets.network import Network

#Pygame Intialization
pygame.font.init()
WID,HEI = 700,400
WIN = pygame.display.set_mode((WID,HEI))
pygame.display.set_caption('Chess')
main_font = pygame.font.SysFont("comicsans", 30)
message_font = pygame.font.Font('assets/PlaypenSans.ttf', 20)


resultss = {
    'w': '1-0',
    'b': '0-1',
    'd': '1/2-1/2'
}

boardpositions = {
'a1': (0,350),
'a2': (0,300),
'a3': (0,250),
'a4': (0,200),
'a5': (0,150),
'a6': (0,100),
'a7': (0,50),
'a8': (0,0),

'b1': (50,350),
'b2': (50,300),
'b3': (50,250),
'b4': (50,200),
'b5': (50,150),
'b6': (50,100),
'b7': (50,50),
'b8': (50,0),

'c1': (100,350),
'c2': (100,300),
'c3': (100,250),
'c4': (100,200),
'c5': (100,150),
'c6': (100,100),
'c7': (100,50),
'c8': (100,0),

'd1': (150,350),
'd2': (150,300),
'd3': (150,250),
'd4': (150,200),
'd5': (150,150),
'd6': (150,100),
'd7': (150,50),
'd8': (150,0),

'e1': (200,350),
'e2': (200,300),
'e3': (200,250),
'e4': (200,200),
'e5': (200,150),
'e6': (200,100),
'e7': (200,50),
'e8': (200,0),

'f1': (250,350),
'f2': (250,300),
'f3': (250,250),
'f4': (250,200),
'f5': (250,150),
'f6': (250,100),
'f7': (250,50),
'f8': (250,0),

'g1': (300,350),
'g2': (300,300),
'g3': (300,250),
'g4': (300,200),
'g5': (300,150),
'g6': (300,100),
'g7': (300,50),
'g8': (300,0),

'h1': (350,350),
'h2': (350,300),
'h3': (350,250),
'h4': (350,200),
'h5': (350,150),
'h6': (350,100),
'h7': (350,50),
'h8': (350,0)
}

# Background
BG = pygame.image.load('assets/imgs/bg.png')
#Background for side
BG2 = pygame.image.load('assets/imgs/bg2.png')

IMGS = {
        'pawn': (pygame.transform.scale(pygame.image.load('assets/imgs/wpawn.png'), (50,50)), pygame.transform.scale(pygame.image.load('assets/imgs/blpawn.png'), (50,50))),
        'knight': (pygame.transform.scale(pygame.image.load('assets/imgs/wknight.png'), (50,50)), pygame.transform.scale(pygame.image.load('assets/imgs/blknight.png'), (50,50))),
        'bishop': (pygame.transform.scale(pygame.image.load('assets/imgs/wbishop.png'), (50,50)), pygame.transform.scale(pygame.image.load('assets/imgs/blbishop.png'), (50,50))),
        'rook': (pygame.transform.scale(pygame.image.load('assets/imgs/wrook.png'), (50,50)), pygame.transform.scale(pygame.image.load('assets/imgs/blrook.png'), (50,50))),
        'queen': (pygame.transform.scale(pygame.image.load('assets/imgs/wqueen.png'), (50,50)), pygame.transform.scale(pygame.image.load('assets/imgs/blqueen.png'), (50,50))),
        'king': (pygame.transform.scale(pygame.image.load('assets/imgs/wking.png'), (50,50)), pygame.transform.scale(pygame.image.load('assets/imgs/blking.png'), (50,50))),
    }

#Current pieces on board
pieces = []
wpieces = []
bpieces = []
bking = None
wking = None

#Misc Variables
abcs = '123abcdefghij'
nm = "Anonymous"
rating = 1200
clicked_on_piece = None
pawnpushed = 0
piece_taken = 0
whites_turn = True
movesdone = 0
positions = []
file = []
loggedin = False

#Useful lambdas
right = lambda x: abcs[abcs.index(x[0]) + 1] + x[1]
left = lambda x: abcs[abcs.index(x[0]) - 1] + x[1]
up = lambda x: x[0] + str(int(x[1])+1)
down = lambda x: x[0] + str(int(x[1])-1)
tomins = lambda x: f"{math.floor(x/60)}:{(f'0{x%60}' if x%60 < 10 else x%60) if x % 60 != 0 else '00'}" if x/3600 < 1 else f"{math.floor(x/3600)}:{math.floor(x/60) - 60 if math.floor(x/60) - 60 >= 10 else f'0{math.floor(x/60)-60}'}:{(f'0{x%60}' if x%60 < 10 else x%60) if x % 60 != 0 else '00'}"
getword = lambda st, ind: st.split(' ')[ind]

#Board Init
def board():
    WIN.blit(BG, (0, 0))
    for i in range(0,8):
            for n in range(8):
                if i%2==0:
                    if n%2==1:
                        pygame.draw.rect(WIN, (0,153,51), (n*50,i*50,50,50))
                    else:
                        pygame.draw.rect(WIN, (255,255,255), (n*50,i*50,50,50))
                else:
                    if n%2==0:
                        pygame.draw.rect(WIN, (0,153,51), (n*50,i*50,50,50))
                    else:
                        pygame.draw.rect(WIN, (255,255,255), (n*50,i*50,50,50))

#Flips board
def flip(whitedown = False):
    if whitedown:
        for x in boardpositions:
            pos = abcs.index(x[0]) * 50 - 150
            boardpositions[x] = (pos, boardpositions[x][1])
            
            if x[1] == '8':
                boardpositions[x] = (boardpositions[x][0], 0)
            elif x[1] == '7':
                boardpositions[x] = (boardpositions[x][0], 50)
            elif x[1] == '6':
                boardpositions[x] = (boardpositions[x][0], 100)
            elif x[1] == '5':
                boardpositions[x] = (boardpositions[x][0], 150)
            elif x[1] == '4':
                boardpositions[x] = (boardpositions[x][0], 200)
            elif x[1] == '3':
                boardpositions[x] = (boardpositions[x][0], 250)
            elif x[1] == '2':
                boardpositions[x] = (boardpositions[x][0], 300)
            else:
                boardpositions[x] = (boardpositions[x][0], 350)
    else:
        for x in boardpositions:
            if x[0] == 'h':
                boardpositions[x] = ( 0, boardpositions[x][1])
            elif x[0] == 'g':
                boardpositions[x] = (50, boardpositions[x][1])
            elif x[0] == 'f':
                boardpositions[x] = (100, boardpositions[x][1])
            elif x[0] == 'e':
                boardpositions[x] = (150, boardpositions[x][1])
            elif x[0] == 'd':
                boardpositions[x] = (200, boardpositions[x][1])
            elif x[0] == 'c':
                boardpositions[x] = (250, boardpositions[x][1])
            elif x[0] == 'b':
                boardpositions[x] = (300, boardpositions[x][1])
            else:
                boardpositions[x] = (350, boardpositions[x][1])
            
            posn = int(x[1]) * 50 - 50
            boardpositions[x] = (boardpositions[x][0], posn)


#Check if square clicked
def sqclick(sq, pos):
        x1, y1 = pos
        if boardpositions[sq][0] <= x1 <= boardpositions[sq][0] + 50 and boardpositions[sq][1] <= y1 < boardpositions[sq][1] + 50:
            return True
        else:
            return False
        
#Checks if any given square is occupied
def square_occupied(sq, isBlack =None, returnpiece=False):
    if isBlack == None:
        for l in pieces:
            if l.square == sq:
                if returnpiece:
                    return l
                return True
        if returnpiece:
            return None
        return False
    else:
        for l in pieces:
            if l.square == sq:
                if l.isBlack == isBlack:
                    if returnpiece:
                        return l
                    return True
        if returnpiece:
            return None
        return False
    
#Checks Diagonals
def diagonal(sq, piece=None):
    if piece.worth == 1:
        result = []
        if piece.isBlack:
            if sq[0] !='a':
                sq1 = abcs[abcs.index(sq[0]) - 1]+str(int(sq[1])-1)
                if square_occupied(sq1, False):
                    result.append('x' + sq1)

            if sq[0] != 'h':
                sq2 = abcs[abcs.index(sq[0]) + 1]+str(int(sq[1])-1)
                if square_occupied(sq2, False):
                    result.append('x' + sq2)
            return result
        
        else:
            if sq[0] !='a':
                sq1 = abcs[abcs.index(sq[0]) - 1]+str(int(sq[1])+1)
                if square_occupied(sq1, True):
                    result.append('x' + sq1)

            if sq[0] != 'h':
                sq2 = abcs[abcs.index(sq[0]) + 1]+str(int(sq[1])+1)
                if square_occupied(sq2, True):
                    result.append('x' + sq2)
            return result
            
    #Checks kings diagonal reaches
    elif piece.worth > 10:
        return [abcs[abcs.index(sq[0]) + 1]+str(int(sq[1])+1),
                abcs[abcs.index(sq[0]) + 1]+str(int(sq[1])-1),
                abcs[abcs.index(sq[0]) - 1]+str(int(sq[1])+1),
                abcs[abcs.index(sq[0]) - 1]+str(int(sq[1])-1)]
            

    tempsq = sq
    tr = []
    bl = []
    tl = []
    br = []
    
    # Check Top-Right Diagonal
    while tempsq[0] != 'h' and tempsq[1] != '8':
        tempsq = abcs[abcs.index(tempsq[0]) + 1]+str(int(tempsq[1])+1)
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != None:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                tr.append('x' + tempsq)
                break
        tr.append(tempsq)
            
    #Reset while loop
    tempsq = sq
    
    # Check Bottom-Left Diagonal
    while tempsq[0] != 'a' and tempsq[1] != '1':
        tempsq = abcs[abcs.index(tempsq[0]) - 1]+str(int(tempsq[1])-1)
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != None:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                bl.append('x' + tempsq)
                break
        bl.append(tempsq)


    tempsq = sq
    # Check Top-Left Diagonal
    while tempsq[0] != 'a' and tempsq[1] != '8':
        tempsq = abcs[abcs.index(tempsq[0]) - 1]+str(int(tempsq[1])+1)
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != None:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                tr.append('x' + tempsq)
                break
        tr.append(tempsq)

    tempsq = sq
    # Check Bottom-Right Diagonal
    while tempsq[0] != 'h' and tempsq[1] != '1':
        tempsq = abcs[abcs.index(tempsq[0]) + 1]+str(int(tempsq[1])-1)
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != None:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                tr.append('x' + tempsq)
                break
        tr.append(tempsq)

    return tr + tl + br +bl

#Checks rows and files
def straight(sq, piece):
    t = []
    b = []
    r = []
    l = []

    tempsq = sq
    #Check File Ahead
    while tempsq[1] != '8':
        tempsq = tempsq[0] + str((int(tempsq[1])+1))
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != None:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                t.append('x' + tempsq)
                break
        t.append(tempsq)
    
    tempsq = sq
    #Check File Below
    while tempsq[1] != '1':
        tempsq = tempsq[0] + str((int(tempsq[1])-1))
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != None:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                b.append('x' + tempsq)
                break
        b.append(tempsq)

    tempsq = sq
    #Check Row Right
    while tempsq[0] != 'h':
        tempsq = abcs[abcs.index(tempsq[0])+1] + tempsq[1]
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != None:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                r.append('x' + tempsq)
                break
        r.append(tempsq)

    tempsq = sq
    #Check Row Left
    while tempsq[0] != 'a':
        tempsq = abcs[abcs.index(tempsq[0])-1] + tempsq[1]
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != None:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                l.append('x' + tempsq)
                break
        l.append(tempsq)
    
    return t + b + r + l

#Piece classes
class piece:
    def __init__(self, square, isBlack, worth):
        self.square = square
        self.moves = set([])
        self.isBlack = isBlack
        self.img = IMGS[self.__class__.__name__][self.isBlack]
        self.worth = worth
        self.pieces = {
            1: bking,
            0: wking
        }

    def draw(self):
        WIN.blit(self.img, (boardpositions[self.square][0], boardpositions[self.square][1]))

    def draw_moves(self):
        for x in self.moves:
            #If its a capture draw something else
            if x[0] == 'x':
                pygame.draw.rect(WIN, (125,125,125), (boardpositions[x[1:3]][0] + 5, boardpositions[x[1:3]][1] + 5 , 40, 40))
                pygame.draw.rect(WIN, (255,255,255), (boardpositions[x[1:3]][0] + 10, boardpositions[x[1:3]][1] + 10 , 30, 30))

            else:
                #For castling moves
                if x[-1] == 'O':
                    x = ('g8' if self.isBlack else 'g1') if x == 'O-O' else ('c8' if self.isBlack else 'c1')
                elif '=' in x:
                    x = x.split('=')[0]
                pygame.draw.circle(WIN, (125,125,125), (boardpositions[x][0] + 25, boardpositions[x][1] + 25), 10)

    #Remove illegal moves
    def remove_moves(self):
        toremove = []
        for l in self.moves:
            if '=' in l:
                l = l.split("=")[0]
            if l[0] == 'x':
                if l[1:3] not in boardpositions:
                    toremove.append(l)

            elif l not in boardpositions:
                toremove.append(l)
            elif square_occupied(l, self.isBlack):
                toremove.append(l)

        for x in toremove:
            if x in self.moves:
                self.moves.remove(x)
    
    #Check if piece has been clicked
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if boardpositions[self.square][0] <= x1 <= boardpositions[self.square][0] + 50 and boardpositions[self.square][1] <= y1 < boardpositions[self.square][1] + 50:
            return True
        else:
            return False

    #Capture piece
    def capture(self, capturedpiece):
        pieces.remove(capturedpiece)
        self.square = capturedpiece.square
        
    #Move function
    def move(self, sq, cp=None):
        global last_move, piece_taken
        sq = str(sq)
        if sq in self.moves:
            if sq[0] == 'x':
                last_move = (self, sq, self.square)
                ptn = notationhelp()                 
                cp = square_occupied(sq[1:3],returnpiece=True)
                piece_taken = 0
                self.capture(cp)
                movechange(ptn)  
            else:
                last_move = (self, sq, self.square)
                ptn = notationhelp()
                self.square = sq  
                piece_taken += 0.5
                movechange(ptn)
        else:
            raise ValueError(f'{self.__class__.__name__.capitalize()} {"takes" if sq[0] == "x" else "to"} {sq[1:3] if sq[0] == "x" else sq}')

#Pawn Class
class pawn(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 1)
        
    def enpassant(self):
        mvs = set()
        if self.isBlack:
            if type(last_move[0]) is pawn and last_move[1][1] == '4' and last_move[2][1] == '2':
                if self.square[1] == '4':
                    if last_move[1][0] == abcs[abcs.index(self.square[0]) + 1]:
                        mvs.add('x' + abcs[abcs.index(self.square[0]) + 1] + str(int(self.square[1]) - 1))
                        
                    elif last_move[1][0] == abcs[abcs.index(self.square[0]) - 1]:
                        mvs.add('x' + abcs[abcs.index(self.square[0]) - 1] + str(int(self.square[1]) - 1))
        else:
            if type(last_move[0]) is pawn and last_move[1][1] == '5' and last_move[2][1] == '7':
                if self.square[1] == '5':
                    if last_move[1][0] == abcs[abcs.index(self.square[0]) + 1]:
                        mvs.add('x' + abcs[abcs.index(self.square[0]) + 1] + str(int(self.square[1]) + 1))
                    elif last_move[1][0] == abcs[abcs.index(self.square[0]) - 1]:
                        mvs.add('x' + abcs[abcs.index(self.square[0]) - 1] + str(int(self.square[1]) + 1))    

        return mvs
    
    #Checks where it can moves
    def check_moves(self): 
        mvs = set([])
        if self.square == 'c5' and square_occupied('g6'):
            pass
        if self.isBlack:
            sq_in_front = self.square[0] + str(int(self.square[1]) - 1)
            sq2_in_front = self.square[0] + str(int(self.square[1]) - 2)
            if not square_occupied(sq_in_front):
                mvs.add(sq_in_front)
                if self.square[1] == '7' and not square_occupied(sq2_in_front):
                    mvs.add(sq2_in_front)
        else:
            sq_in_front = self.square[0] + str(int(self.square[1]) + 1)
            sq2_in_front = self.square[0] + str(int(self.square[1]) + 2)
            if not square_occupied(sq_in_front):
                mvs.add(sq_in_front)
                if self.square[1] == '2' and not square_occupied(sq2_in_front):
                    mvs.add(sq2_in_front)
        
        
        diags = diagonal(self.square, self)
        if diags != None:
            for l in diags:
                mvs.add(l)
       
        if last_move != None:
            mvs |= self.enpassant()
        
        tor = [[], []]
        for m in mvs:
            if m[-1] == '8' or m[-1] == '1':
                tor[0].append(m)
                tor[1].append(m+'=Q')
                tor[1].append(m+'=R')
                tor[1].append(m+'=B')
                tor[1].append(m+'=N')
        for _ in tor[0]:
            mvs.remove(_)
        for _ in tor[1]:
            mvs.add(_)


        self.moves = mvs
        self.remove_moves()
        
    def promote(self, sq, definitepromote=False):
        global promoted
        sq = str(sq).removeprefix('x')
        
        if definitepromote:
            sq, p = sq.split('=')
            piec = {
                'Q': queen(sq, self.isBlack),
                'R': rook(sq, self.isBlack),
                'B': bishop(sq, self.isBlack),
                'N': knight(sq, self.isBlack)

            }
            pieces.append(piec[p])
            pieces.remove(self)
            if self.isBlack:
                bpieces.remove(self)
                bpieces.append(piec[p])
            else:
                wpieces.remove(self)
                wpieces.append(piec[p])
            promoted = (True, p)


            return
        
        sq = sq.split('=')[0]
        
        q = Button(WIN, 100, 190, "Queen", (255, 255, 255), autofit=False, fontsize= 15, screensize = (WID, HEI), size = (50, 20))
        r = Button(WIN, 150, 190, "Rook", (255, 255, 255), autofit=False, fontsize= 15, screensize = (WID, HEI), size = (50, 20))
        b = Button(WIN, 200, 190, "Bishop", (255, 255, 255), autofit=False, fontsize= 15, screensize = (WID, HEI), size = (50, 20))
        k = Button(WIN, 250, 190, "Knight", (255, 255, 255), autofit=False, fontsize= 15, screensize = (WID, HEI), size = (50, 20))
        

        x = True
        while x:
            q.draw()
            r.draw()
            b.draw()
            k.draw()

            if self.isBlack:
                ps = bpieces
            else:
                ps = wpieces

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if q.click(pygame.mouse.get_pos()):
                        pie = queen(sq, self.isBlack)
                        pieces.append(pie)
                        ps.append(pie)
                        to = 'Q'
                        x = False
                    if r.click(pygame.mouse.get_pos()):
                        pie = rook(sq, self.isBlack)
                        pieces.append(pie)
                        ps.append(pie)
                        to = 'R'
                        x = False
                    if b.click(pygame.mouse.get_pos()):
                        pie = bishop(sq, self.isBlack)
                        pieces.append(pie)
                        ps.append(pie)
                        to = 'B'
                        x = False
                    if k.click(pygame.mouse.get_pos()):
                        pie = knight(sq, self.isBlack)
                        pieces.append(pie)
                        ps.append(pie)
                        to = 'N'
                        x = False
        
            pygame.display.update()
        promoted = (True, to)
        pieces.remove(self)
        ps.remove(self)

    def move(self, sq, cp=None, definitepromote = False):
        global pawnpushed, last_move, piece_taken
        sq = str(sq)
        if sq in self.moves:
            if sq[0] == 'x':
                cp = square_occupied(sq[1:3],returnpiece=True)
                piece_taken = 0
                
                if type(self) == pawn and cp == None:
                    passant = True
                    cp = square_occupied(sq[1] + str(int(sq[2]) + 1), returnpiece=True) if self.isBlack else square_occupied(sq[1] + str(int(sq[2]) - 1), returnpiece=True)
                else:
                    passant = False

                if '1' in sq or '8' in sq:
                    self.promote(sq, definitepromote)
                    sq = sq.split('=')[0]
                
                last_move = (self, sq, self.square)
                self.capture(cp)
                if passant:
                    self.square = self.square[0] + str(int(self.square[1]) + (-1 if self.isBlack else 1))

                movechange()  

            else:
                if '1' in sq or '8' in sq:
                    org = self.square
                    self.promote(sq, definitepromote)
                    sq = sq.split('=')[0]
                    last_move = (self, sq, org)

                    
                else:
                    last_move = (self, sq, self.square)
                    self.square = sq 
                
                piece_taken += 0.5
                movechange()
        else:
            raise ValueError(f'Pawn {"takes" if sq[0] == "x" else "to"} {sq[1:3] if sq[0] == "x" else sq}')

        pawnpushed = 0

#Rook Class
class rook(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 5)
        self.moved = False

    def check_moves(self):
        self.moves = straight(self.square, self)

    def move(self, sq, cp=None):
        super().move(sq, cp)
        self.moved = True   

#Bishop Class
class bishop(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 3)

    def check_moves(self):
        self.moves = diagonal(self.square, self) 

#Queen Class       
class queen(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 9)

    def check_moves(self):
        self.moves = diagonal(self.square, self) + straight(self.square, self)     

#King Class  
class king(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 10000000000000000)
        self.in_check = False
        self.moved = False

    def check_moves(self):
        self.moves = set([
            up(self.square),
            down(self.square),
            left(self.square),
            right(self.square)
            ] + diagonal(self.square, self))
        
        for mv in self.moves:
            if square_occupied(mv, not self.isBlack):
                self.moves.remove(mv)
                self.moves.add('x' + mv)
        
        self.remove_moves()
        cas = checkcastle(self.isBlack)
        if cas['kingside']:
            self.moves.add('O-O')
        if cas['queenside']:
            self.moves.add('O-O-O')

    def move(self, sq, cp=None):
        if sq == 'O-O' or sq == 'O-O-O':
            castle(not self.isBlack, sq)
            return
        super().move(sq, cp)
        self.moved = True

#Knight Class
class knight(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 3)

    def check_moves(self):
        self.moves = [
            right(self.square)[0] + str(int(right(self.square)[1]) + 2),
            left(self.square)[0] + str(int(right(self.square)[1]) + 2),
            right(self.square)[0] + str(int(right(self.square)[1]) - 2),
            left(self.square)[0] + str(int(right(self.square)[1]) - 2),
            right(right(self.square))[0]+ up(self.square)[1],
            left(left(self.square))[0]+ up(self.square)[1],
            right(right(self.square))[0]+ down(self.square)[1],
            left(left(self.square))[0]+ down(self.square)[1]
        ]
        for mv in self.moves:
            if square_occupied(mv, not self.isBlack):
                self.moves[self.moves.index(mv)] = 'x' + mv

        self.remove_moves()

#Checks if there is sufficient material
def is_sufficient(color = None):
    pss = {
        'white': wpieces,
        'black': bpieces
    }
    if color != None:
        if len(pss[color]) < 2:
            return False
        for x in pss[color]:
            t = type(x)
            if t is queen or t is rook or t is pawn:
                return True
        if len(pss[color]) == 2:
            return False

#Checks for a draw
def checkdraw():
    if len(pieces) <= 4:
        if len(pieces) == 2: return True, 'Insufficient Material'

        for p in pieces:
            if type(p) is queen or type(p) is rook or type(p) is pawn:
                if min(pawnpushed, piece_taken) >= 50: return True, '50 move rule'    
                elif positions.count(fen()) >= 3: return True, 'Repetition'
                else: return False, 'Not a draw' 
                    
        else:
            if len(wpieces) <= 2 and len(bpieces) <= 2: return True, 'Insufficient Material'            
            elif positions.count(fen()) >= 3: return True, 'Repetition'
            else: return False, 'Not a draw'

            
    else:
        if min(pawnpushed, piece_taken) >= 50: return True, '50 Move Rule'
        elif positions.count(fen()) >= 3: 
            return True, 'Repetition'
        else: return False, 'Not a draw'
      
#Checks if in check
def checkforchecks():
    wking.in_check = False
    bking.in_check = False

    for x in pieces:
        if type(x) is rook and x.square == 'f8':
            x.check_moves()
            continue
        x.check_moves()

    if not whites_turn:
        for p in wpieces:
            for mv in p.moves:
                if mv[0] == 'x':
                    if mv[1:3] == bking.square:
                        bking.in_check = True
                        
    else:
        for p in bpieces:
            for mv in p.moves:
                if mv[0] == 'x':
                    if mv[1:3] == wking.square:
                        wking.in_check = True

#Removes illegal moves (Based on checks etc)
def setlegalmoves(sidechecked):
    ps = {
        'white': (wpieces, wking, 'black'),
        'black': (bpieces, bking, 'white')
    }
    global  run
    legalmoves = []
    checkedsidepieces, checkedking, otherside = ps[sidechecked]
    checkingsidepieces = ps[otherside][0]
    
    for x in checkedsidepieces: 
        for c in x.moves: 
            orisq = x.square

            if c[0] == 'x':
                takenp = square_occupied(c[1:3], returnpiece=True)
                if takenp == None and type(x) is pawn:
                    takenp = square_occupied(c[1] + str(int(c[2]) + 1), returnpiece=True) if x.isBlack else square_occupied(c[1] + str(int(c[2]) - 1), returnpiece=True)
                pieces.remove(takenp)
                checkingsidepieces.remove(takenp)
                x.square = c[1:3]

            else: x.square = c

            for piec in checkingsidepieces:
                piec.check_moves()
                for m in piec.moves:
                    if m[0] == 'x' and m[1:3] == checkedking.square:
                        break
                else:
                    continue
                break
            else:
                legalmoves.append((c, x))
                
            if c[0] == 'x':
                pieces.append(takenp)
                checkingsidepieces.append(takenp)
                    
            x.square = orisq
            
    if legalmoves == []:
        if not checkedking.in_check:
            menu('STALEMATE', send=True)
        else:
            menu(otherside.upper()+ ' WINS BY CHECKMATE', send=True)        
    for pi in checkedsidepieces:
        pi.moves = set([])
    for m in legalmoves:
        m[1].moves.add(m[0])

# Called after every move
def movechange(passtonotation = ''):
    global whites_turn, clicked_on_piece, pawnpushed, movesdone, promoted, movenota
    if whites_turn:
        wtimer.pause()
        btimer.resume()
    else:
        btimer.pause()
        wtimer.resume()
    whites_turn = not whites_turn
    clicked_on_piece = None
    pawnpushed += 0.5
    movesdone += 0.5
    for p in pieces:
        p.check_moves()
    positions.append(fen())
    movenota = notation(additional = passtonotation)
    promoted = (False, None)

#Checks if move has been made and moves the chosen piece
def checkmove(clicked_on_piece, pos):
    global game
    for mv in clicked_on_piece.moves:
        if mv == 'O-O':  
            if  sqclick('g1', pos) or sqclick('g8', pos):
                clicked_on_piece.move(mv)
                game = net.send(movenota + ',' + str(pl_color))
                return
        elif mv == 'O-O-O':
            if sqclick('c1', pos) or sqclick('c8', pos):
                clicked_on_piece.move(mv)
                game = net.send(movenota + ',' + str(pl_color))

                return
        elif sqclick(mv[1:3] if mv[0] == 'x' else mv[:2], pos):
            clicked_on_piece.move(mv)
            game = net.send(movenota + ',' + str(pl_color))

            return 

#Checks if either side can castle    
def checkcastle(color):
    castlesqs = {
        False: {
            'pieces': (wking, wqrook, wkrook, bpieces),
            'kside': ('f1', 'g1'),
            'qside': ('d1', 'c1', 'b1')
        },
        True: {
            'pieces': (bking, bqrook, bkrook, wpieces),
            'kside': ('f8', 'g8'),
            'qside': ('d8', 'c8', 'b8')
        }
    }

    selfking, qrook, krook, otherpieces = castlesqs[color]['pieces']
    result = [False, False]

    if not selfking.moved and not krook.moved and krook in pieces:
        for x in castlesqs[color]['kside']:
            if square_occupied(x):
                break
            continue
        else:
            for piece in otherpieces:
                for move in piece.moves:
                    if move in castlesqs[color]['kside']:
                        break
                else:
                    continue
                break
            else:
                result[0] = True
    
    if not selfking.moved and not qrook.moved and qrook in pieces:
        for x in castlesqs[color]['qside']:
            if square_occupied(x):
                break
            continue
        else:
            for piece in otherpieces:
                for move in piece.moves:
                    if move == 'b1':
                        continue
                    if move in castlesqs[color]['qside']:
                        break
                else:
                    continue
                break
            else:
                result[1] = True

    return ({'kingside': result[0], 'queenside': result[1]})

#Castles the person
def castle(wturn, mv):
    global last_move
    if mv == 'O-O':
        if wturn == True:
            wking.square = 'g1'
            wkrook.square = 'f1'
            wking.moved = True
            wkrook.moved = True
            last_move = (wking, 'O-O')
            movechange()
        else:
            bking.square = 'g8'
            bkrook.square = 'f8'
            bking.moved = True
            bkrook.moved = True
            last_move = (bking, 'O-O')
            movechange()
    elif mv == 'O-O-O':
        if wturn == True:
            wking.square = 'c1'
            wqrook.square = 'd1'
            wking.moved = True
            wqrook.moved = True
            last_move = (wking, 'O-O-O')
            movechange()
        else:
            bking.square = 'c8'
            bqrook.square = 'd8'
            bking.moved = True
            bqrook.moved = True
            last_move = (bking, 'O-O-O')
            movechange()

#Writes Notation
def notation(**kwargs):
    checkforchecks()
    if last_move == None: return

    x = last_move[1]

    if type(last_move[0]) is knight:
        x = 'N' + kwargs['additional'] + x
    elif type(last_move[0]) is pawn:
        if x[0] == 'x':
            x = last_move[2][0] + x
        if promoted[0]:
            x = x + '=' + promoted[1]
    else:
        if 'O' not in x:
            x = type(last_move[0]).__name__[0].upper() + kwargs['additional'] + x

    if bking.in_check or wking.in_check:
        x = x + '+'
    
    file.append(x)
    return x
    
#Checks if notation need to be like Nbd2
def notationhelp():
    x = []
    y = []
    locs = []
    
    for p in pieces:
        for mv in p.moves:
            x.append((mv, type(p), p.isBlack))
            y.append(p.square)
            
    if tuple([last_move[1], type(last_move[0]), last_move[0].isBlack]) in x:
        for _ in range(len(x)):
            if x[_] == tuple([last_move[1], type(last_move[0]), last_move[0].isBlack]):
                locs.append(y[_])
           
        if last_move[2] in locs:
            if len(locs) == 2:
                if locs[0][0] == locs[1][0]:
                    return last_move[2][1]
                else:
                    return last_move[2][0]
            if len(locs) >= 3:
                toreturn = '  '
                for _ in locs:
                    if _ == last_move[2]:
                        continue
                    if _[1] == last_move[2][1]:
                        toreturn = last_move[2][0] + toreturn if toreturn[0] != last_move[2][0] else toreturn
                    if _[0] == last_move[2][0]:
                        toreturn = toreturn + last_move[2][1] if toreturn[-1] != last_move[2][1] else toreturn
                return toreturn.replace(" ", '')
            
    return ''

#Turns notation to a move
def notationtomove(move):
    move = str(move)
    pis = {
        'K': king,
        'N': knight,
        'B': bishop,
        'R': rook,
        'Q': queen,
    }
    if whites_turn:
        selfpieces = wpieces.copy()
    else:
        selfpieces = bpieces.copy()

    move = move.removesuffix('+')
    move = move.removesuffix('#')

    length = len(move)
    #e4
    if length == 2:
        for x in selfpieces:
            if type(x) is pawn and move in x.moves:
                x.move(move)
                return

    # Nc3
    elif length == 3:
        if move == 'O-O':
            if whites_turn:
                wking.move(move)
                return
            else:
                bking.move(move)           
                return 
                
        pt = pis[move[0]]
        for x in selfpieces:
            if type(x) == pt and move[1:] in x.moves:
                x.move(move[1:])
                return

    #Nge2, Nxe3, exd5, e8=Q
    elif length == 4:
        if '=' in move:
            for x in selfpieces:
                if type(x) is pawn and move in x.moves:
                    x.move(move, definitepromote=True)
                    return

        elif move[0].islower():
            for x in selfpieces:
                if type(x) is pawn and x.square[0] == move[0] and move[1:] in x.moves:
                    x.move(move[1:])
                    return

        else:
            pt = pis[move[0]]
            if move[1] == 'x':
                for x in selfpieces:
                    if type(x) is pt and move[1:] in x.moves:
                        x.move(move[1:])
                        return
            else:
                for x in selfpieces:
                    if type(x) is pt and move[2:] in x.moves and move[1] in x.square:
                        x.move(move[2:])
                        return
    #Be2d3
    elif length == 5:
        if move == 'O-O-O':
            if whites_turn:
                wking.move(move)
                return
            else:
                bking.move(move)    
                return
        else:
            pt = pis[move[0]]
            for x in selfpieces:
                if type(x) is pt and move[3:] in x.moves and move[1:3] == x.square:
                    x.move(move[3:])
                    return
    elif length == 6:
        if '=' in move:
            for x in selfpieces:
                if type(x) is pawn and x.square[0] == move[0] and move[1:] in x.moves:
                    x.move(move[1:], definitepromote=True)
                    return
        else:
            pt = pis[move[0]]
            for x in selfpieces:
                if type(x) is pt and move[3:] in x.moves and move[1:3] == x.square:
                    x.move(move[3:])
                    return
    
    
    raise ValueError(move + " is an invalid/illegal move")                  

# Main game loop
def main():
    global wpieces, bpieces, pieces, bking, wking, wkrook, wqrook, bkrook, bqrook
    global clicked_on_piece, whites_turn, movesdone, last_move, promoted, game
    global file, positions, run, pawnpushed, piece_taken, net, pl_color, btimer, wtimer
    run = True
    clock = pygame.time.Clock()
    net = Network()
    pl_color = int(net.getP())
    game = net.send('p-' + nm)


    drawmes = message_font.render(f"{'White' if pl_color else 'Black'} wants a draw", 1, (0, 0, 0))
    resign = Button(WIN, 450, 250, "Resign", (0, 0, 0) if pl_color == 1 else (255, 255, 255),(255, 255, 255) if pl_color == 1 else (0, 0, 0), autofit= False, size = (100, 40))
    drawbut = Button(WIN, 575, 250, "Draw", (125, 125, 125), (255, 255, 255) if pl_color == 0 else (0, 0, 0), autofit= False, size = (100, 40))

    whites_turn = True
    last_move = None
    clicked_on_piece = None
    pawnpushed = 0
    piece_taken = 0
    whites_turn = True
    movesdone = 0
    promoted = (False, None)
    positions = []
    file = []

    flip(not pl_color)

    wstarttime = 300
    bstarttime = 300
    wtime = 300
    btime = 300
    wtimer = Timer()
    btimer = Timer()

    wking = king('e1', 0)
    bking = king('e8', 1)
    wkrook = rook('h1', 0)
    wqrook = rook('a1', 0)
    bkrook = rook('h8', 1)
    bqrook = rook('a8',1)

    pieces = [
    pawn('a7', 1),
    pawn('b7', 1),
    pawn('c7', 1),
    pawn('d7', 1),
    pawn('e7', 1),
    pawn('f7', 1),
    pawn('g7', 1),
    pawn('h7', 1),

    pawn('a2', 0),
    pawn('b2', 0),
    pawn('c2', 0),
    pawn('d2', 0),
    pawn('e2', 0),
    pawn('f2', 0),
    pawn('g2', 0),
    pawn('h2', 0),

    bqrook,
    bkrook,

    wqrook,
    wkrook,

    knight('b8', 1),
    knight('g8', 1),
    knight('b1', 0),
    knight('g1', 0),

    bishop('c8', 1),
    bishop('f8', 1),
    bishop('c1', 0),
    bishop('f1', 0),

    queen('d8',  1),
    queen('d1', 0),
    wking,
    bking,
    ]

    for p in pieces:
        p.check_moves()
    wpieces = [x for x in pieces if not x.isBlack]
    bpieces = [x for x in pieces if x.isBlack]
    def redraw():
        
        #Board Initialization
        board()

        #Draw Piece Selected
        if clicked_on_piece != None:
            clicked_on_piece.draw_moves()

        #Blit pieces
        for piec in pieces:
            piec.draw()
            piec.check_moves()

        drawbut.color = (125, 125, 125)
            
        wtimelabel = main_font.render(tomins(round(wtime)), 1, (255, 255, 255))
        btimelabel = main_font.render(tomins(round(btime)), 1, (255, 255, 255))
        WIN.blit(wtimelabel, (450, 300 if pl_color == 0 else 100))
        WIN.blit(btimelabel, (450, 100 if pl_color == 0 else 300))

        if pl_color == 0:
            if movesdone == 0:
                resign.text = 'Abort'
            else:
                resign.text = 'Resign'
        else:
            if movesdone <= 0.5:
                resign.text = 'Abort'
            else:
                resign.text = 'Resign'   
        
        if (game.whitewantsdraw and pl_color == 1) or (game.blackwantsdraw and pl_color == 0):
            WIN.blit(drawmes, (450, 150))
        elif (game.whitewantsdraw and pl_color == 0) or (game.blackwantsdraw and pl_color == 1):
            drawbut.color = (255, 255, 0)

        drawbut.draw()
        resign.draw()
        pygame.display.update()
    
    wtimer.start()
    wtimer.pause()
    btimer.start()
    btimer.pause()
    while run:
        clock.tick(60)
        try:
            if not game.ended():
                game = net.send('get')
                if game.connected() and whites_turn:
                    wtimer.resume()
        except EOFError:
            print(net.close())
            menu('Game Disconnected')
        except ConnectionResetError as e:
            print(e)
            menu('Error')
        except ConnectionAbortedError as e:
            print(e)
            menu('Error')
        
        
        if game.connected() and not game.ended():
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if resign.click(pos):
                        if resign.text == 'Resign':
                            game = net.send('resign,'+ ('black' if pl_color else 'white'))
                        else:
                            game = net.send('abort')
                    if drawbut.click(pos):
                        game = net.send('draw,'+ ('black' if pl_color else 'white'))


            wpieces = [x for x in pieces if not x.isBlack]
            bpieces = [x for x in pieces if x.isBlack]
            
            redraw()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_h]:
                print(fen())
                

            if whites_turn:
                wtime = wstarttime - wtimer.get().seconds
                if wtime <= 0:
                    if is_sufficient('black'):
                        menu('BLACK WINS ON TIME', send=True)
                    else:
                        draw = (True, "")
                        menu('TIMEOUT VS IN. MATERIAL', send=True)

            else:
                btime = bstarttime - btimer.get().seconds
                if btime <= 0:
                    if is_sufficient('white'):
                        menu('WHITE WINS ON TIME', send=True)
                    else:
                        draw = (True, "")
                        menu('IN. MATERIAL VS TIMEOUT', send=True)

            checkforchecks()
            draw = checkdraw()
            if draw[0]:
                menu('DRAW BY ' + draw[1].upper(), send=True)
            if whites_turn:
                setlegalmoves('white')
            else:
                setlegalmoves('black')

            if whites_turn == pl_color:
                lm = game.getLastMove()
                if lm[1] != pl_color:
                    notationtomove(lm[0])
                continue
                
            #Event Checking
            pos = pygame.mouse.get_pos()
            for event in events:
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for x in pieces:
                        if x.click(pos):
                            if whites_turn != x.isBlack and whites_turn != pl_color:
                                clicked_on_piece = x
                    if clicked_on_piece != None:
                        checkmove(clicked_on_piece, pos)

                    if resign.click(pos):
                        if resign.text == 'Resign':
                            game = net.send('resign,'+ ('black' if pl_color else 'white'))
                        else:
                            game = net.send('abort')
                    if drawbut.click(pos):
                        game = net.send('draw,'+ ('black' if pl_color else 'white'))
                    

        elif not game.connected():
            mes = Button(WIN, 1, 2, 'Waiting for player', (255, 255, 255), center=True, screensize = (WID, HEI))
            ex = Button(WIN, WID-30, HEI-30, 'X', (255, 0, 0), textcolor=(255, 255, 255), size =(30, 30), autofit=False)
            mes.draw()
            ex.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if ex.click(pos):
                        net.close()
                        return

        elif game.ended():
            if game.result == '0-1':
                color = 'BLACK WINS by '
            elif game.result == '1-0':
                color = 'WHITE WINS by '
            elif game.result == '1/2-1/2':
                color = 'DRAW by '
            elif game.result == '0-0':
                color = 'GAME '
            else:
                raise ValueError('Invalid result ' + game.result)
            
            menu(color  + game.endby)

#Menu screen
def menu(res, start=False, send=False):
    global run, file, nm, game
    run = False
    res = res.upper()
    result = ""
        
    message = Button(WIN,225, 20, res, fontsize=15)
    new = Button(WIN, 1, 100, "New Game", (249, 97, 103), (255, 255, 255 ))

    if not loggedin:
        logins = Button(WIN, 1, 200, "Login", (249, 97, 103), (255, 255, 255 ))
        logins.x = 550 - (logins.width/2)
    else:
        if not start:
            db = Network('db').db('update', 'users', ('rating', 'username'), (rating + 8, nm))
        label1 = pygame.font.SysFont("calibri", 20).render(nm + f'({rating})', 1, (0, 0, 0))


    message.x = 550 - (message.width/2)
    new.x = 550 - (new.width/2)
    
    if res.count('WHITE') == 1:
        result = resultss['w']
        if send:
            game = net.send(result + ','+getword(res, -1))

    elif res.count('BLACK') == 1:
        result = resultss['b']
        if send:
            game = net.send(result + ',' + getword(res, -1))

    elif res.count('DRAW') == 1:
        result = resultss['d']
        if send:
            game = net.send(result + ',' + (getword(res, -1).capitalize() if "INSUFFICIENT" not in res else "INSUFFICIENT MATERIAL"))

    if not start:
        g = fen()
        export = Button(WIN, 1, 2, "Export", (47, 60, 126), (251, 234, 235), autofit=True)
        export.x, export.y = WID - export.width - 2, HEI - export.height - 2
        net.client.close()
        
    if res.count('CHECKMATE') == 1:
        if file[-1][-1] != "+":
            file[-1] = file[-1] + "#"
        else:
            file[-1] = file[-1][:-1] + "#"
    
    l = 0
    for _ in file:
        if l % 2 == 0:
            file[l] = str(int(l/2) + 1) + '. ' + _
        l += 1

    while True:
        WIN.blit(BG2, (400, 0))
        if not start: 
            fentopos(g, True)
            export.draw()
        else:
            board()
        message.draw()
        new.draw()
        if not loggedin:
            logins.draw()
        else: 
            WIN.blit(label1, (420, HEI - 30))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit() 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not start:
                    if export.click(pygame.mouse.get_pos()):
                        path = os.path.join('C:\\Users\\darsh\\Downloads', 'game.pgn')

                        tags = [f'[Won By "{getword(res, -1).capitalize() if "INSUFFICIENT" not in res else "INSUFFICIENT MATERIAL"}"]\n',
                                f'[White {game.players[0]}]\n', 
                                f'[Black {game.players[1]}]\n', 
                                f'[Result "{result}"]\n']
                        
                        with open(path, 'w')as f:
                            f.writelines(tags)
                            for x in file:
                                f.write(x + ' ')
                            f.write('\n' + result)

                if new.click(pygame.mouse.get_pos()):
                    main()
                if not loggedin:
                    if logins.click(pygame.mouse.get_pos()):
                        login()
                
                        
        pygame.display.update()

#Login Screen
def login(createmenu = False):
    global nm, rating, loggedin
    drawmes = False
    user = InputBox(300, 125, 200, 30)
    password = InputBox(300, 225, 200, 30, True)
    if not createmenu:
        create = Button(WIN, WID - 150, 0, "Create Account", (44, 151, 75),autofit=False, size = (150, 35))

    mes = Button(WIN, 1, 2, '', (255, 127, 127), center=True, screensize = (WID, HEI), autofit=False, size = (500, 50))
    mes.y -= 10
    submit = Button(WIN, 300, 300, "Login", (255, 255, 0), autofit=False, size = (100, 30))
    back = Button(WIN, 0, HEI - 30, "<", (255, 255, 0), autofit=False, size = (30, 30))
    label1  = pygame.font.SysFont("gotham", 32).render("Username:", 1, (0, 0, 0))
    label2  = pygame.font.SysFont("gotham", 32).render("Password:", 1, (0, 0, 0))
    while True:
        WIN.blit(BG, (0, 0))
        WIN.blit(label1, (175, 130))
        WIN.blit(label2, (175, 230))

        if drawmes:
            mes.draw()
        submit.draw()
        user.update()
        user.draw(WIN)
        if not createmenu: create.draw()
        else: submit.text = "Create"
        password.update()
        password.draw(WIN)
        back.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit() 
            user.handle_event(event)
            password.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit.click(pygame.mouse.get_pos()):
                    if not createmenu:
                        db = Network('db')
                        res = eval(db.db('select', 'users', ('username', 'password'), (user.get(), password.get())))
                        if res[0] == 'No results':
                            mes.text = "Wrong Username or password"
                            drawmes = True
                        elif type(res) is list:
                            nm, rating = res[0][0], res[0][2]
                            loggedin = True
                            menu("", start = True)
                    else:
                        if user.get() != '' and password.get() != '':
                            if len(user.get()) <= 8:
                                db = Network('db')
                                res = db.db('insert', 'users', ('username', 'password'), (user.get(), password.get()))
                                if res != 'None':
                                    if "Duplicate" in res:
                                        mes.text = "Username already taken"
                                        drawmes = True
                                else:
                                    nm = user.get()
                                    rating = 1200
                                    loggedin = True
                                    menu('', start=True)

                            else:
                                mes.text = "Username must be at max 8 characters"
                                drawmes = True
                        else:
                            mes.text = "Enter username and password"
                            drawmes = True
                if not createmenu:
                    if create.click(pygame.mouse.get_pos()):
                        login(True)
                if back.click(pygame.mouse.get_pos()):
                    menu("", True)

def fen() -> str:
    '''Converts current position to fen string'''
    files = 'abcdefgh'
    ranks = '12345678'
    pos = {
        '8':'',
        '7':'',
        '6':'',
        '5':'',
        '4':'',
        '3':'',
        '2':'',
        '1':'',
    }
    piecs = {
        'pawn': 'p',
        'knight': 'n',
        'bishop': 'b',
        'rook': 'r',
        'queen': 'q',
        'king': 'k',
    }

    for r in ranks:
        count = 0
        for f in files:
            piece = square_occupied(f+r, returnpiece=True)
            if piece == None:
                count += 1
                continue
            else:
                n = piecs[piece.__class__.__name__]
                if not piece.isBlack: n = n.capitalize()
                if count > 0:
                    pos[r] += str(count)
                count = 0
                pos[r] += n
        if count > 0 :
            pos[r] += str(count)

    res = ''
    for x in pos:
        res += pos[x] + '/'
    res = res[:-1]

    res += ( f" {'w' if whites_turn else 'b'} ") 

    dash = True
    if checkcastle(0)['kingside']:
        res += 'K'
        dash = False
    if checkcastle(1)['kingside']:
        res += 'k'
        dash = False
    if checkcastle(0)['queenside']:
        res += 'Q'
        dash = False
    if checkcastle(1)['queenside']:
        res += 'q'
        dash = False

    if dash:
        res += '- '

    dash = True
    if last_move != None:
        if last_move[0].isBlack:
            pawns = list(filter(lambda x: type(x) is pawn, wpieces))
            s = 1
        else:
            pawns = list(filter(lambda x: type(x) is pawn, wpieces))
            s = -1

        for p in pawns:
            if p.enpassant() != set():
                res+= ' ' + last_move[2][0] + str(int(last_move[1][1]) + s)
                dash = False
                break
        
    if dash:
        res += '-'
    
    res += f' {int(min(pawnpushed*2, piece_taken*2))} '
    res += str(int(movesdone))

    return res



def fentopos(num, flipboard=False):
    global pieces, whites_turn
    pieces = []
    files = 'abcdefgh1'
    file = 'a'
    rank = 8

    num = str(num).split(' ')[0]

    for x in num:
        if x == '/':
            rank -= 1
            file = 'a'
            continue
        try:
            c = int(x)
        except:
            c = 0
            if str(x).lower() == 'p':
                pieces.append(pawn(file + str(rank), int(not x.isupper())))
            elif str(x).lower() == 'n':
                pieces.append(knight(file + str(rank), int(not x.isupper())))
            elif str(x).lower() == 'b':
                pieces.append(bishop(file + str(rank), int(not x.isupper())))
            elif str(x).lower() == 'r':
                pieces.append(rook(file + str(rank), int(not x.isupper())))
            elif str(x).lower() == 'q':
                pieces.append(queen(file + str(rank), int(not x.isupper())))
            elif str(x).lower() == 'k':
                pieces.append(king(file + str(rank), int(not x.isupper())))
                
        file = files[files.index(file) + (c if c else 1)]
    
    if flipboard:flip()
    board()
    for x in pieces:
        x.draw()


if __name__ == '__main__':
    fentopos('r7/ppp1k3/2n5/3q4/3P4/2Q2N1P/PPP2PP1/R4K1R w - - 0 21')
    menu("WELCOME", True)