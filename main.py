import pygame
import os, sys
import time

#Pygame Intialization
pygame.font.init()
WID,HEI = 400,400
WIN = pygame.display.set_mode((WID,HEI))
pygame.display.set_caption('Chess')

def board():
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


abcs = '123abcdefghij'

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

# Images
BPAWN = pygame.transform.scale(pygame.image.load('imgs/blpawn.png'), (50,50))
BROOK = pygame.transform.scale(pygame.image.load('imgs/blrook.png'), (50,50))
BKNIGHT = pygame.transform.scale(pygame.image.load('imgs/blknight.png'), (50,50))
BBISHOP = pygame.transform.scale(pygame.image.load('imgs/blbishop.png'), (50,50))
BQUEEN = pygame.transform.scale(pygame.image.load('imgs/blqueen.png'), (50,50))
BKING = pygame.transform.scale(pygame.image.load('imgs/blking.png'), (50,50))

WPAWN = pygame.transform.scale(pygame.image.load('imgs/wpawn.png'), (50,50))
WROOK = pygame.transform.scale(pygame.image.load('imgs/wrook.png'), (50,50))
WKNIGHT = pygame.transform.scale(pygame.image.load('imgs/wknight.png'), (50,50))
WBISHOP = pygame.transform.scale(pygame.image.load('imgs/wbishop.png'), (50,50))
WQUEEN = pygame.transform.scale(pygame.image.load('imgs/wqueen.png'), (50,50))
WKING = pygame.transform.scale(pygame.image.load('imgs/wking.png'), (50,50))

IMGS = {
        'pawn': (WPAWN, BPAWN),
        'knight': (WKNIGHT, BKNIGHT),
        'bishop': (WBISHOP, BBISHOP),
        'rook': (WROOK, BROOK),
        'queen': (WQUEEN, BQUEEN),
        'king': (WKING, BKING),
    }

right = lambda x: abcs[abcs.index(x[0]) + 1] + x[1]
left = lambda x: abcs[abcs.index(x[0]) - 1] + x[1]
up = lambda x: x[0] + str(int(x[1])+1)
down = lambda x: x[0] + str(int(x[1])-1)

def sqclick(sq, pos):
        x1, y1 = pos
        if boardpositions[sq][0] <= x1 <= boardpositions[sq][0] + 50 and boardpositions[sq][1] <= y1 < boardpositions[sq][1] + 50:
            return True
        else:
            return False

#Current pieces on board
pieces = []

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

class piece:
    def __init__(self, square, isBlack, worth):
        self.square = square
        self.x, self.y = boardpositions[self.square]
        self.moves = set([])
        self.isBlack = isBlack
        self.img = IMGS[self.__class__.__name__][self.isBlack]
        self.worth = worth
        

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def draw_moves(self):
        for x in self.moves:
            if type(x) is tuple:
                pygame.draw.rect(WIN, (125,125,125), (boardpositions[x[0]][0] + 5, boardpositions[x[0]][1] + 5 , 40, 40))
                pygame.draw.rect(WIN, (255,255,255), (boardpositions[x[0]][0] + 10, boardpositions[x[0]][1] + 10 , 30, 30))
            else:
                pygame.draw.circle(WIN, (125,125,125), (boardpositions[x][0] + 25, boardpositions[x][1] + 25), 10)

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
        
        

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + 50 and self.y <= y1 < self.y + 50:
            return True
        else:
            return False

    def capture(self, capturedpiece, player):
        pieces.remove(capturedpiece)
        self.move(capturedpiece.square)
        
    
    def move(self, sq):
        self.square = sq
        self.x, self.y = boardpositions[self.square]
        self.moves = set([])

class pawn(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 1)
        
    def check_moves(self): 
        if self.isBlack:
            sq_in_front = self.square[0] + str(int(self.square[1]) - 1)
            sq2_in_front = self.square[0] + str(int(self.square[1]) - 2)
            if not square_occupied(sq_in_front):
                self.moves.add(sq_in_front)
                if self.square[1] == '7' and not square_occupied(sq2_in_front):
                    self.moves.add(sq2_in_front)
        else:
            sq_in_front = self.square[0] + str(int(self.square[1]) + 1)
            sq2_in_front = self.square[0] + str(int(self.square[1]) + 2)
            if not square_occupied(sq_in_front):
                self.moves.add(sq_in_front)
                if self.square[1] == '2' and not square_occupied(sq2_in_front):
                    self.moves.add(sq2_in_front)
        
        diags = diagonal(self.square, self)
        if diags != None:
            for l in diags:
                self.moves.add(l)

        self.remove_moves()
        self.draw_moves()

    def promote(self):
        p = input('Promote to: ')
        if p == 'queen':
            pieces.append(queen(self.square, self.isBlack))
        elif p == 'rook':
            pieces.append(rook(self.square, self.isBlack))
        elif p == 'bishop':
            pieces.append(bishop(self.square, self.isBlack))
        elif p == 'knight':
            pieces.append(knight(self.square, self.isBlack))
        pieces.remove(self)

    def capture(self, capturedpiece, player):
        super().capture(capturedpiece, player)
        if capturedpiece.square[1] == '8':
            self.promote()
            
    
    def move(self, sq):
        super().move(sq)
        if self.square[1] == '8':
            self.promote()
            

class rook(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 5)

    def check_moves(self):
        self.moves = straight(self.square, self)
        self.draw_moves()

class bishop(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 3)

    def check_moves(self):
        self.moves = diagonal(self.square, self)
        self.draw_moves()

class queen(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 9)

    def check_moves(self):
        self.moves = diagonal(self.square, self) + straight(self.square, self)
        self.draw_moves()

class king(piece):
    def __init__(self, square, isBlack):
        super().__init__(square, isBlack, 10000000000000000)
        self.in_check = False

    def check_moves(self):
        self.moves = [
            up(self.square),
            down(self.square),
            left(self.square),
            right(self.square)
            ] + diagonal(self.square, self)
        
        for mv in self.moves:
            if square_occupied(mv, not self.isBlack):
                self.moves[self.moves.index(mv)] = (mv, '')
        
        self.remove_moves()
      
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

wking = king('e1', 0)
bking = king('e8', 1)

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

rook('a8', 1),
rook('h8', 1),

rook('a1', 0),
rook('h1', 0),

knight('b8', 1),
knight('g8', 1),
knight('b1', 0),
knight('g1', 0),

bishop('c8', 1),
bishop('f8', 1),
bishop('c1', 0),
bishop('f1', 0),

queen('d8',  1),
bking,
queen('d1', 0),
king('e1', 0),

]
def checkmove(pos):
    global clicked_on_piece, whites_turn, checkingpieces
    for mv in clicked_on_piece.moves:
        if type(mv) is tuple:
            if sqclick(mv[0], pos):
                clicked_on_piece.move(mv, square_occupied(mv[0],returnpiece=True))
                whites_turn = not whites_turn
                clicked_on_piece = None
        else:
            if sqclick(mv, pos):
                clicked_on_piece.move(mv)
                whites_turn = not whites_turn
                clicked_on_piece = None
                checkingpieces = None


def main():
    global wpieces, bpieces
    run = True
    clock = pygame.time.Clock()

    def redraw():
        global clicked_on_piece, whites_turn

        #Board Initialization
        board()

        #Draw Piece Selected
        if clicked_on_piece != None:
            clicked_on_piece.draw_moves()

        #Blit pieces
        for piec in pieces:
            piec.draw()
            
        #Event Checking
        pos = pygame.mouse.get_pos()
        pygame.display.update()
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
                        
                        
                    


    while run:
        clock.tick(60)
        redraw()
        wpieces = [x for x in pieces if not x.isBlack]
        bpieces = [x for x in pieces if x.isBlack]
        
    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit() 

main()