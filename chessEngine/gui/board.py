from turtle import position
import pygame as pg
import sys
from dataclasses import dataclass


BACKGROUND = 247, 199, 171
WHITE= 255, 255, 255
BLACK = 0, 0, 0

SQUARE_HEIGHT = 100
SQUARE_WIDTH = 100

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024

STARTING_X = (SCREEN_WIDTH - 8*SQUARE_WIDTH)/2
STARTING_Y = (SCREEN_HEIGHT - 8*SQUARE_HEIGHT)/2

def squares():
    squareList = []
    for file in range(8):
        for rank in range(8):
            isLightSquare = (file + rank) % 2 != 0
            squareColor = WHITE if isLightSquare else BLACK
            position = (STARTING_X + file*SQUARE_WIDTH, STARTING_Y + rank*SQUARE_HEIGHT)
            
            rect = pg.Rect(position[0],position[1],SQUARE_WIDTH,SQUARE_HEIGHT)
            squareList.append((rect,squareColor))
            
    return squareList            
            
            
def drawBoard(screen, squareList):
    for rect, color in squareList:
        pg.draw.rect(screen,color,rect)
    
def boardGui():
    pg.init()

    size = width, height = 1024, 1024
    speed = [2, 2]
    

    screen = pg.display.set_mode(size)

    # ball = pg.image.load("./chessEngine/gui/chesspieces.png")
    # ballrect = ball.get_rect()
    squareList = squares()
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()
            
        
        screen.fill(BACKGROUND)
        drawBoard(screen,squareList)
        # screen.blit(ball, ballrect)
        pg.display.flip()
        
        
if(__name__=='__main__'):
    boardGui()
    



