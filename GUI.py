# Implement the pygame GUI for the application
import pygame
from Board import Board
from pygame.locals import *

pygame.init()

# Set up the window
WIDTHHEIGHT = 600
screen = pygame.display.set_mode((WIDTHHEIGHT, WIDTHHEIGHT))
pygame.display.set_caption("Othello")
# Set up the tiles
empty_tile_unscaled = pygame.image.load("./Images/Tile.bmp")
black_tile_unscaled = pygame.image.load("./Images/Black Tile.bmp")
white_tile_unscaled = pygame.image.load("./Images/White Tile.bmp")
open_tile_unscaled = pygame.image.load("./Images/Open Tile.bmp")
# Scale tiles to be 50 x 50
tilesize = int(WIDTHHEIGHT / 8)
empty_tile = pygame.transform.scale(empty_tile_unscaled, (tilesize, tilesize))
black_tile = pygame.transform.scale(black_tile_unscaled, (tilesize, tilesize))
white_tile = pygame.transform.scale(white_tile_unscaled, (tilesize, tilesize))
open_tile = pygame.transform.scale(open_tile_unscaled, (tilesize, tilesize))
board = Board()


def draw_board(boardc):
    board = boardc.board
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                screen.blit(empty_tile, (i * tilesize, j * tilesize))
            elif board[i][j] == 1:
                screen.blit(white_tile, (i * tilesize, j * tilesize))
            elif board[i][j] == 2:
                screen.blit(black_tile, (i * tilesize, j * tilesize))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            x = pos[0] // tilesize

            y = pos[1] // tilesize

            print(x, y)
    
    screen.fill((255, 255, 255))
    draw_board(board)

    # Draw 8x8 grid of empty tiles that are properly sized
    
    pygame.display.flip()