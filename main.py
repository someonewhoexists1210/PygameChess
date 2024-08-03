import pygame
import os, sys
import time

#Pygame Intialization
pygame.font.init()
WID,HEI = 400,400
WIN = pygame.display.set_mode((WID,HEI))
pygame.display.set_caption('Chess')


abcs = 'abcdefgh'

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


edit = lambda sq : [sq[0],int(sq[1])]
join = lambda a : a[0] + str(a[1])


#Board Initialization
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

               


#Current pieces on board
pieces = []


def square_occupied(sq):
    for l in pieces:
        if l.square == sq:
            return True
        else:
            return False

class piece:
    def __init__(self, square, color, img, worth):
        self.square = square
        self.x, self.y = boardpositions[square]
        self.moves = []
        self.color = color
        self.img = img
        self.worth = worth
        

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def draw_moves(self, win):
        for x in self.moves:
            pygame.draw.circle(win, (125,125,125), (boardpositions[x][0] + 50, boardpositions[x][1] - 50), 30)
        pygame.display.update()

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + 50 and self.y <= y1 < self.y + 50:
            return True
        else:
            return False


for m in range(0, 8):
    pieces.append(piece(abcs[m]+'7', 'black', BPAWN, 1))
    pieces.append(piece(abcs[m]+'2', 'white', WPAWN, 1))
pieces.append(piece('a8', 'black', BROOK, 5))
pieces.append(piece('h8', 'black', BROOK, 5))
pieces.append(piece('b8', 'black', BKNIGHT, 3))
pieces.append(piece('g8', 'black', BKNIGHT, 3))
pieces.append(piece('c8', 'black', BBISHOP, 3))
pieces.append(piece('f8', 'black', BBISHOP, 3))
pieces.append(piece('d8', 'black', BQUEEN, 9))
pieces.append(piece('e8', 'black', BKING, 100))

pieces.append(piece('a1', 'white', WROOK, 5))
pieces.append(piece('h1', 'white', WROOK, 5))
pieces.append(piece('b1', 'white', WKNIGHT, 3))
pieces.append(piece('g1', 'white', WKNIGHT, 3))
pieces.append(piece('c1', 'white', WBISHOP, 3))
pieces.append(piece('f1', 'white', WBISHOP, 3))
pieces.append(piece('d1', 'white', WQUEEN, 9))
pieces.append(piece('e1', 'white', WKING, 100))

    
while True:

    for p in pieces:
        p.draw(WIN)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i in pieces:
                    if i.click(pos):
                        i.draw_moves(WIN)
    pygame.display.update()
