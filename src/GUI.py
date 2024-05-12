# Implement the pygame GUI for the application
import pygame
from Board import Board
from pygame.locals import *

pygame.init()

# Set up the window
WINDOW_SIZE = 800
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Othello")


# Set up the tiles
empty_tile_unscaled = pygame.image.load("./Images/Empty Tile.bmp")
black_tile_unscaled = pygame.image.load("./Images/Black Tile.bmp")
white_tile_unscaled = pygame.image.load("./Images/White Tile.bmp")
open_tile_unscaled = pygame.image.load("./Images/Open Tile.bmp")
hover_tile_unscaled = pygame.image.load("./Images/Hover Tile.bmp")
hover_white_tile_unscaled = pygame.image.load("./Images/Hover White Tile.bmp")
hover_black_tile_unscaled = pygame.image.load("./Images/Hover Black Tile.bmp")

tile_size = int(WINDOW_SIZE / 8)
empty_tile = pygame.transform.scale(empty_tile_unscaled, (tile_size, tile_size))
black_tile = pygame.transform.scale(black_tile_unscaled, (tile_size, tile_size))
white_tile = pygame.transform.scale(white_tile_unscaled, (tile_size, tile_size))
open_tile = pygame.transform.scale(open_tile_unscaled, (tile_size, tile_size))
hover_tile = pygame.transform.scale(hover_tile_unscaled, (tile_size, tile_size))
hover_white_tile = pygame.transform.scale(hover_white_tile_unscaled, (tile_size, tile_size))
hover_black_tile = pygame.transform.scale(hover_black_tile_unscaled, (tile_size, tile_size))
board = Board()


# For updating the board sprites
def draw_board(boardc):
    board = boardc.board
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                screen.blit(empty_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 1:
                screen.blit(white_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 2:
                screen.blit(black_tile, (i * tile_size, j * tile_size))
    pygame.display.flip()

screen.fill((255, 255, 255))
running = True


# Main loop
while running:
    for event in pygame.event.get():
        draw_board(board)
        pos = pygame.mouse.get_pos()
        x = pos[0] // tile_size
        y = pos[1] // tile_size
        
        # To use the hover sprite 
        if board.board[x][y] == 0:
            screen.blit(hover_tile, (x * tile_size, y * tile_size))
        if board.board[x][y] == 1:
            screen.blit(hover_white_tile, (x * tile_size, y * tile_size))
        if board.board[x][y] == 2:
            screen.blit(hover_black_tile, (x * tile_size, y * tile_size))
        
        # Closing the game
        if event.type == pygame.QUIT:
            running = False
        
        # Printing current tile location
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(x, y)
            
    pygame.display.flip()