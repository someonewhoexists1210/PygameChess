import pygame
import sys, math, os
from features import Button, InputBox, MYSQL
from dotenv import load_dotenv
load_dotenv()

#Pygame Intialization
pygame.font.init()
WID,HEI = 700,400
WIN = pygame.display.set_mode((WID,HEI))
pygame.display.set_caption('Chess')
pygame.font.init()
main_font = pygame.font.SysFont("comicsans", 30)

sys.dont_write_bytecode = True

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
BG = pygame.image.load('imgs/bg.png')
#Background for side panel
BG2 = pygame.image.load('imgs/bg2.png')

IMGS = {
        'pawn': (pygame.transform.scale(pygame.image.load('imgs/wpawn.png'), (50,50)), pygame.transform.scale(pygame.image.load('imgs/blpawn.png'), (50,50))),
        'knight': (pygame.transform.scale(pygame.image.load('imgs/wknight.png'), (50,50)), pygame.transform.scale(pygame.image.load('imgs/blknight.png'), (50,50))),
        'bishop': (pygame.transform.scale(pygame.image.load('imgs/wbishop.png'), (50,50)), pygame.transform.scale(pygame.image.load('imgs/blbishop.png'), (50,50))),
        'rook': (pygame.transform.scale(pygame.image.load('imgs/wrook.png'), (50,50)), pygame.transform.scale(pygame.image.load('imgs/blrook.png'), (50,50))),
        'queen': (pygame.transform.scale(pygame.image.load('imgs/wqueen.png'), (50,50)), pygame.transform.scale(pygame.image.load('imgs/blqueen.png'), (50,50))),
        'king': (pygame.transform.scale(pygame.image.load('imgs/wking.png'), (50,50)), pygame.transform.scale(pygame.image.load('imgs/blking.png'), (50,50))),
    }


#Current pieces on board
pieces = []
wpieces = []
bpieces = []
bking = None
wking = None

#Misc Variables
abcs = '123abcdefghij'
clicked_on_piece = None
pawnpushed = 0
piece_taken = 0
whites_turn = True
movesdone = 0
positions = []
file = []
DB_PATH = os.getenv('DB_PATH')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
executer = MYSQL(os.path.abspath(DB_PATH), 'localhost', DB_USER, DB_PASSWORD, DB_NAME)

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
        return False
    else:
        for l in pieces:
            if l.square == sq:
                if l.isBlack == isBlack:
                    if returnpiece:
                        return l
                    return True
        return False
    
#Checks Diagonals
def diagonal(sq, piece=None):
    if piece.worth == 1:
        result = []
        if piece.isBlack:
            if sq[0] !='a':
                sq1 = abcs[abcs.index(sq[0]) - 1]+str(int(sq[1])-1)
                if square_occupied(sq1, False):
                    result.append((sq1, ''))

            if sq[0] != 'h':
                sq2 = abcs[abcs.index(sq[0]) + 1]+str(int(sq[1])-1)
                if square_occupied(sq2, False):
                    result.append((sq2, ''))
            return result
        
        else:
            if sq[0] !='a':
                sq1 = abcs[abcs.index(sq[0]) - 1]+str(int(sq[1])+1)
                if square_occupied(sq1, True):
                    result.append((sq1, ''))

            if sq[0] != 'h':
                sq2 = abcs[abcs.index(sq[0]) + 1]+str(int(sq[1])+1)
                if square_occupied(sq2, True):
                    result.append((sq2, ''))
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
        if occupied != False:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                tr.append((tempsq, ''))
                break
        tr.append(tempsq)
            
    #Reset while loop
    tempsq = sq
    
    # Check Bottom-Left Diagonal
    while tempsq[0] != 'a' and tempsq[1] != '1':
        tempsq = abcs[abcs.index(tempsq[0]) - 1]+str(int(tempsq[1])-1)
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != False:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                bl.append((tempsq, ''))
                break
        bl.append(tempsq)


    tempsq = sq
    # Check Top-Left Diagonal
    while tempsq[0] != 'a' and tempsq[1] != '8':
        tempsq = abcs[abcs.index(tempsq[0]) - 1]+str(int(tempsq[1])+1)
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != False:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                tr.append((tempsq, ''))
                break
        tr.append(tempsq)

    tempsq = sq
    # Check Bottom-Right Diagonal
    while tempsq[0] != 'h' and tempsq[1] != '1':
        tempsq = abcs[abcs.index(tempsq[0]) + 1]+str(int(tempsq[1])-1)
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != False:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                tr.append((tempsq, ''))
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
        if occupied != False:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                t.append((tempsq, ''))
                break
        t.append(tempsq)
    
    tempsq = sq
    #Check File Below
    while tempsq[1] != '1':
        tempsq = tempsq[0] + str((int(tempsq[1])-1))
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != False:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                b.append((tempsq, ''))
                break
        b.append(tempsq)

    tempsq = sq
    #Check Row Right
    while tempsq[0] != 'h':
        tempsq = abcs[abcs.index(tempsq[0])+1] + tempsq[1]
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != False:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                r.append((tempsq, ''))

                break
        r.append(tempsq)

    tempsq = sq
    #Check File Ahead
    while tempsq[0] != 'a':
        tempsq = abcs[abcs.index(tempsq[0])-1] + tempsq[1]
        occupied = square_occupied(tempsq, returnpiece=True)
        if occupied != False:
            if piece.isBlack == occupied.isBlack:
                break
            else:
                l.append((tempsq, ''))
                break
        l.append(tempsq)
    
    return t + b + r + l

#Piece classes
class piece:
    def __init__(self, square, isBlack, worth):
        self.square = square
        self.x, self.y = boardpositions[self.square]
        self.moves = set([])
        self.isBlack = isBlack
        self.img = IMGS[self.__class__.__name__][self.isBlack]
        self.worth = worth
        self.pieces = {
            1: bking,
            0: wking
        }

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def draw_moves(self):
        for x in self.moves:
            #If its a capture draw something else
            if type(x) is tuple:
                pygame.draw.rect(WIN, (125,125,125), (boardpositions[x[0]][0] + 5, boardpositions[x[0]][1] + 5 , 40, 40))
                pygame.draw.rect(WIN, (255,255,255), (boardpositions[x[0]][0] + 10, boardpositions[x[0]][1] + 10 , 30, 30))

            else:
                #For castleing moves
                if x[-1] == 'p':
                    pygame.draw.circle(WIN, (125,125,125), (boardpositions[x[:-1]][0] + 25, boardpositions[x[:-1]][1] + 25), 10)
                else:
                    pygame.draw.circle(WIN, (125,125,125), (boardpositions[x][0] + 25, boardpositions[x][1] + 25), 10)

    #Remove illegal moves
    def remove_moves(self):
        toremove = []
        for l in self.moves:
            if type(l) is tuple:
                if l[0] not in boardpositions:
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
        if self.x <= x1 <= self.x + 50 and self.y <= y1 < self.y + 50:
            return True
        else:
            return False

    def check_moves(self):
        pass

    #Capture piece
    def capture(self, capturedpiece):
        pieces.remove(capturedpiece)
        self.move(capturedpiece.square)
        
    #Move function
    def move(self, sq, cp=None):
        if type(sq) == tuple:
            self.capture(cp)
            return
        self.square = sq
        self.x, self.y = boardpositions[self.square]    
        self.check_moves()
        
#Pawn Class
class pawn(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 1)
        
    #Checks where it can moves
    def check_moves(self): 
        mvs = set([])
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
            if self.isBlack:
                if type(last_move[0]) is pawn and last_move[1][1] == '4' and last_move[2][1] == '2':
                    if self.square[1] == '4':
                        if last_move[1][0] == abcs[abcs.index(self.square[0]) + 1]:
                            mvs.add((abcs[abcs.index(self.square[0]) + 1] + str(int(self.square[1]) - 1), last_move[0]))
                            
                        if last_move[1][0] == abcs[abcs.index(self.square[0]) - 1]:
                            mvs.add((abcs[abcs.index(self.square[0]) - 1] + str(int(self.square[1]) - 1), last_move[0]))
            else:
                if type(last_move[0]) is pawn and last_move[1][1] == '5' and last_move[2][1] == '7':
                    if self.square[1] == '5':
                        if last_move[1][0] == abcs[abcs.index(self.square[0]) + 1]:
                            mvs.add((abcs[abcs.index(self.square[0]) + 1] + str(int(self.square[1]) + 1), last_move[0]))
                        if last_move[1][0] == abcs[abcs.index(self.square[0]) - 1]:
                            mvs.add((abcs[abcs.index(self.square[0]) - 1] + str(int(self.square[1]) + 1), last_move[0]))
                            

        self.moves = mvs
        self.remove_moves()
        
    def capture(self, capturedpiece):
        super().capture(capturedpiece)
        global promoted
        if capturedpiece.square[1] == '8':
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


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if q.click(pygame.mouse.get_pos()):
                            pieces.append(queen(self.square, self.isBlack))
                            to = 'Q'
                            x = False
                        if r.click(pygame.mouse.get_pos()):
                            pieces.append(rook(self.square, self.isBlack))
                            to = 'R'
                            x = False
                        if b.click(pygame.mouse.get_pos()):
                            pieces.append(bishop(self.square, self.isBlack))
                            to = 'B'
                            x = False
                        if k.click(pygame.mouse.get_pos()):
                            pieces.append(knight(self.square, self.isBlack))
                            to = 'K'
                            x = False
            
                pygame.display.update()
            promoted = (True, to)
            pieces.remove(self)

    def move(self, sq, cp=None):
        global pawnpushed                
        super().move(sq, cp)
        if type(sq) is tuple:
            if sq[1] != '':
                if self.isBlack:
                    self.square = cp.square[0] + str(int(cp.square[1]) - 1)
                else:
                    self.square = cp.square[0] + str(int(cp.square[1]) + 1)
                self.x, self.y = boardpositions[self.square]   
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
                self.moves.add((mv, ''))
        
        self.remove_moves()
        castles(self.isBlack)

    def move(self, sq, cp=None):
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
                self.moves[self.moves.index(mv)] = (mv, '')

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

#Gets current position
def get_position():
    temp = []
    for p in pieces:
        temp.append(p.square)
    return temp

#Checks for a draw
def checkdraw():
    if whitewantsdraw and blackwantsdraw:
        return True, "Agreement"
    
    if len(pieces) <= 4:
        if len(pieces) == 2: return True, 'Insufficient Material'

        for p in pieces:
            if type(p) is queen or type(p) is rook or type(p) is pawn:
                if pawnpushed >= 50 and piece_taken >= 50: return True, '50 move rule'    
                elif positions.count(get_position()) >= 2: return True, 'Repetition'
                else: return False, 'Not a draw' 
                    
        else:
            if len(wpieces) <= 2 and len(bpieces) <= 2: return True, 'Insufficient Material'            
            elif positions.count(get_position()) >= 2: return True, 'Repetition'
            else: return False, 'Not a draw'

            
    else:
        if pawnpushed >= 50 and piece_taken >= 50: return True, '50 Move Rule'
        elif positions.count(get_position()) >= 2: return True, 'Repetition'
        else: return False, 'Not a draw'
      
#Checks if in check
def checkforchecks():
    wking.in_check = False
    bking.in_check = False

    if not whites_turn:
        for p in wpieces:
            for mv in p.moves:
                if type(mv) is tuple:
                    if mv[0] == bking.square:
                        bking.in_check = True
                        
    else:
        for p in bpieces:
            for mv in p.moves:
                if type(mv) is tuple:
                    if mv[0] == wking.square:
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

            if type(c) is tuple:
                    if c[1] == '':
                        takenp = square_occupied(c[0], returnpiece=True)
                    else:
                        takenp = c[1]
                    pieces.remove(takenp)
                    checkingsidepieces.remove(takenp)
                    x.square = c[0]

            else: x.square = c

            for piec in checkingsidepieces:
                piec.check_moves()
                for m in piec.moves:
                    if type(m) is tuple and m[0] == checkedking.square:
                        break
                else:
                    continue
                break
            else:
                legalmoves.append((c, x))
                
            if type(c) is tuple:
                pieces.append(takenp)
                checkingsidepieces.append(takenp)
                    
            x.square = orisq
            
    if legalmoves == []:
        if not checkedking.in_check:
            menu('STALEMATE')
        else:
            menu(otherside.upper()+ ' WINS BY CHECKMATE')        
    for pi in checkedsidepieces:
        pi.moves = set([])
    for m in legalmoves:
        m[1].moves.add(m[0])

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
    
#Checks if move has been made and moves the chosen piece
def checkmove(pos):
    global clicked_on_piece, whites_turn, piece_taken, pawnpushed, last_move, movesdone, promoted
    passtonotation = ''

    def movechange():
        global whites_turn, clicked_on_piece, pawnpushed, movesdone, whitewantsdraw, blackwantsdraw
        whites_turn = not whites_turn
        clicked_on_piece = None
        pawnpushed += 0.5
        movesdone += 0.5
        whitewantsdraw, blackwantsdraw = False, False
        for p in pieces:
            p.check_moves()
        positions.append(get_position())
        notation(additional = passtonotation)

    for mv in clicked_on_piece.moves:
        if clicked_on_piece == wking:
            if mv[-1] == 'p':
                if mv[0] == 'g':
                    if sqclick('g1', pos):
                        promoted = (False, None)
                        wking.move('g1')
                        wkrook.move('f1')
                        last_move = (wking, 'O-O')
                        movechange()
                        return
                    continue
                elif mv[0] == 'c':
                    if sqclick('c1', pos):
                        promoted = (False, None)
                        wking.move('c1')
                        wqrook.move('d1')
                        last_move = (wking, 'O-O-O')
                        movechange()
                        return
                    continue

        elif clicked_on_piece == bking:
            if mv[-1] == 'p':
                if mv[0] == 'g':
                    if sqclick('g8', pos):
                        promoted = (False, None)
                        bking.move('g8')
                        bkrook.move('f8')
                        last_move = (bking, 'O-O')
                        movechange()
                        return
                    continue
                elif mv[0] == 'c':
                    if sqclick('c8', pos):
                        promoted = (False, None)
                        bking.move('c8')
                        bqrook.move('d8')
                        last_move = (bking, 'O-O-O')
                        movechange()
                        return
                    continue

        if type(mv) is tuple:
            osq = clicked_on_piece.square
            if sqclick(mv[0], pos):
                last_move = (clicked_on_piece, mv, osq)
                passtonotation = notationhelp()
                if mv[1] == '':
                    promoted = (False, None)
                    clicked_on_piece.move(mv, square_occupied(mv[0],returnpiece=True))
                else:
                    promoted = (False, None)
                    clicked_on_piece.move(mv, mv[1])
                piece_taken = 0
                movechange()      
                return
        else:
            if sqclick(mv, pos):
                osq = clicked_on_piece.square
                promoted = (False, None)
                last_move = (clicked_on_piece, mv, osq)
                passtonotation = notationhelp()
                clicked_on_piece.move(mv)
                piece_taken += 0.5
                movechange()
                return

#Checks if either side can castle    
def castles(color):
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

    if not selfking.moved and not krook.moved:
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
    
    if not selfking.moved and not qrook.moved:
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

    if result[0]:
        selfking.moves.add(castlesqs[color]['kside'][1] + "p")
    if result[1]:
        selfking.moves.add(castlesqs[color]['qside'][1] + "p")
        
#Writes Notation
def notation(**kwargs):
    checkforchecks()
    if last_move == None: return

    x = last_move[1]
    
    if type(x) is tuple:
        x = "x" + x[0]
    


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
    
# Main game loop
def main():
    global wpieces, wtime, bpieces, wking, pieces,  movesdone, wpieces, bpieces
    global clicked_on_piece, whites_turn, draw, bking, run, wkrook, wqrook
    global blackwantsdraw, bkrook, bqrook, last_move, draw, blackwantsdraw, piece_taken
    global whitewantsdraw, whitewantsdraw, pawnpushed, file, promoted, positions
    run = True
    clock = pygame.time.Clock()
    resignblack = Button(WIN, 450, 50, "Resign", (0, 0, 0),(255, 255, 255), autofit= False, size = (100, 40))
    resignwhite = Button(WIN, 450, 250, "Resign", (255, 255, 255), autofit= False, size = (100, 40))
    drawwhite = Button(WIN, 575, 50, "Draw", (125, 125, 125), autofit=False, size = (100, 40))
    drawblack = Button(WIN, 575, 250, "Draw", (125, 125, 125), (255, 255, 255), autofit= False, size = (100, 40))

    whites_turn = True
    movesdone = 0
    last_move = None
    whitewantsdraw = False
    blackwantsdraw = False
    clicked_on_piece = None
    pawnpushed = 0
    piece_taken = 0
    whites_turn = True
    movesdone = 0
    promoted = (False, None)
    positions = []
    file = []


    wtime = 300
    btime = 300

    wpoints = 0
    bpoints = 0

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

    wpieces = [x for x in pieces if not x.isBlack]
    bpieces = [x for x in pieces if x.isBlack]
    for p in wpieces:
        if type(p) is king:
            continue
        wpoints += p.worth
    for p in bpieces:
        if type(p) is king:
            continue
        bpoints += p.worth


    def redraw():
        global clicked_on_piece, whites_turn, draw, whitewantsdraw, blackwantsdraw
        
        #Board Initialization
        board()

        #Draw Piece Selected
        if clicked_on_piece != None:
            clicked_on_piece.draw_moves()

        #Blit pieces
        for piec in pieces:
            piec.draw()
            piec.check_moves()
            

        drawblack.color = (125, 125, 125)
        drawwhite.color = (125, 125, 125)
        checkforchecks()
        draw = checkdraw()
        if draw[0]:
            menu('DRAW BY ' + draw[1].upper())
        if whites_turn:
            setlegalmoves('white')
        else:
            setlegalmoves('black')
        
            
        wtimelabel = main_font.render(tomins(round(wtime)), 1, (255, 255, 255))
        btimelabel = main_font.render(tomins(round(btime)), 1, (255, 255, 255))
        WIN.blit(wtimelabel, (450, 300))
        WIN.blit(btimelabel, (450, 100))

        if last_move == None:
            resignwhite.text = "Abort"
            resignblack.text = "Abort"

        else:
            if movesdone == 0.5:
                resignblack.text = "Abort"
                resignwhite.text = "Resign"
            else:
                resignblack.text = "Resign"
                resignwhite.text = "Resign"
        if whitewantsdraw:
            drawwhite.color = (255, 255, 0)
        if blackwantsdraw:
            drawblack.color = (255, 255, 0)

        resignblack.draw()
        resignwhite.draw()
        drawblack.draw()
        drawwhite.draw()
 
        #Event Checking
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for x in pieces:
                        if x.click(pos):
                            if whites_turn != x.isBlack:
                                clicked_on_piece = x
                    if clicked_on_piece != None:
                        checkmove(pos)
                    if resignblack.click(pos):
                        if resignblack.text == "Resign":
                            menu('White wins by resignation')
                        else:
                            menu('Game Aborted')
                    if resignwhite.click(pos):
                        if resignwhite.text == "Resign":
                            menu('Black wins by resignation')
                        else:
                            menu('Game Aborted')  
                    if drawwhite.click(pos):
                        whitewantsdraw = True
                    if drawblack.click(pos):
                        blackwantsdraw = True
                                      
    while run:
        clock.tick(60)
        if whites_turn:
            wtime -= 1/76
            if wtime <= 0:
                if is_sufficient('black'):
                    menu('BLACK WINS ON TIME')
                else:
                    draw = (True, "")
                    menu('TIMEOUT VS IN. MATERIAL')

        else:
            btime -= 1/76
            if btime <= 0:
                if is_sufficient('white'):
                    menu('WHITE WINS ON TIME')
                else:
                    draw = (True, "")
                    menu('IN. MATERIAL VS TIMEOUT')

        redraw()
        wpieces = [x for x in pieces if not x.isBlack]
        bpieces = [x for x in pieces if x.isBlack]
            
        pygame.display.update()

def menu(res, start=False, loggedin = False):
    global run, file

    run = False
    res = res.upper()
    result = ""
    if not start:
        export = Button(WIN, 1, 2, "Export", (47, 60, 126), (251, 234, 235), autofit=True)
        export.x, export.y = WID - export.width - 2, HEI - export.height - 2
    else:
        board()
        res = "WELCOME"
        
    message = Button(WIN,225, 20, res, fontsize=15)
    new = Button(WIN, 1, 100, "New Game", (249, 97, 103), (255, 255, 255 ))

    if not loggedin:
        logins = Button(WIN, 1, 200, "Login", (249, 97, 103), (255, 255, 255 ))
        logins.x = 550 - (logins.width/2)
    else:
        label1 = pygame.font.SysFont("calibri", 20).render(nm + f'({rating})', 1, (0, 0, 0))


    message.x = 550 - (message.width/2)
    new.x = 550 - (new.width/2)
    

    if res.count('WHITE') == 1:
        result = resultss['w']
    elif res.count('BLACK') == 1:
        result = resultss['b']
    elif res.count('DRAW') == 1:
        result = resultss['d']


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
        if not start: export.draw()
        message.draw()
        new.draw()
        if not loggedin: logins.draw()
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
                        with open('game.txt', 'w')as f:
                            f.writelines([f'[Won By "{getword(res, -1).capitalize()}"]\n', '[White ""]\n', '[Black ""]\n', f'[Result "{result}"]\n'])
                            for x in file:
                                f.write(x + ' ')
                            f.write('\n' + result)
                if new.click(pygame.mouse.get_pos()):
                    main()
                if not loggedin:
                    if logins.click(pygame.mouse.get_pos()):
                        login()
                
                        
        pygame.display.update()

def login(createmenu = False):
    global nm, rating
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
                        res = executer.select('users', 'username', user.get(), 'password',password.get(), 'AND')
                        if res[0] == 'No results':
                            mes.text = "Wrong Username or password"
                            drawmes = True
                        elif type(res) is list:
                            print(executer.selectall('users'))
                            nm, rating = res[0][0], res[0][2]
                            menu("", start = True,loggedin=True)
                    else:
                        if user.get() != '' and password.get() != '':
                            if len(user.get()) <= 8:
                                res = executer.insert('users', ('username', 'password'), (user.get(), password.get()))
                                if res != None:
                                    if "Duplicate" in res:
                                        mes.text = "Username already taken"
                                        drawmes = True
                                else:
                                    nm = user.get()
                                    rating = 1200
                                    menu('', start=True, loggedin=True)

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

menu("", True)