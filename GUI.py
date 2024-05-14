# Implement the pygame GUI for the application
import pygame
from src.Board import Board
from src.Othello import Othello
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Set up the window
WINDOW_SIZE = 800
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Othello")

# Load tile sprites
empty_tile_unscaled = pygame.image.load("Images/Tile (Empty).png")
black_tile_unscaled = pygame.image.load("Images/Black Tile.png")
white_tile_unscaled = pygame.image.load("Images/White Tile.png")
open_tile_unscaled = pygame.image.load("Images/Open Tile.png")
hover_tile_unscaled = pygame.image.load("Images/Tile (Hover).png")
hover_black_tile_unscaled = pygame.image.load("Images/Black Tile (Hover).png")
hover_white_tile_unscaled = pygame.image.load("Images/White Tile (Hover).png")
hover_open_tile_unscaled = pygame.image.load("Images/Open Tile (Hover).png")
paused_black_tile_unscaled = pygame.image.load("Images/Black Tile (Paused).png")
paused_white_tile_unscaled = pygame.image.load("Images/White Tile (Paused).png")
current_black_unscaled = pygame.image.load("Images/Current Black Tile.png")
current_white_tile_unscaled = pygame.image.load("Images/Current White Tile.png")
hover_current_black_unscaled = pygame.image.load("Images/Current Black Tile (Hover).png")
hover_current_white_unscaled = pygame.image.load("Images/Current White Tile (Hover).png")


# Setup tiles
tile_size = int(WINDOW_SIZE / 8)
empty_tile = pygame.transform.scale(empty_tile_unscaled, (tile_size, tile_size))
black_tile = pygame.transform.scale(black_tile_unscaled, (tile_size, tile_size))
white_tile = pygame.transform.scale(white_tile_unscaled, (tile_size, tile_size))
open_tile = pygame.transform.scale(open_tile_unscaled, (tile_size, tile_size))
hover_tile = pygame.transform.scale(hover_tile_unscaled, (tile_size, tile_size))
hover_black_tile = pygame.transform.scale(hover_black_tile_unscaled, (tile_size, tile_size))
hover_white_tile = pygame.transform.scale(hover_white_tile_unscaled, (tile_size, tile_size))
hover_open_tile = pygame.transform.scale(hover_open_tile_unscaled, (tile_size, tile_size))
paused_black_tile = pygame.transform.scale(paused_black_tile_unscaled, (tile_size, tile_size))
paused_white_tile = pygame.transform.scale(paused_white_tile_unscaled, (tile_size, tile_size))
current_black_tile = pygame.transform.scale(current_black_unscaled, (tile_size, tile_size))
current_white_tile = pygame.transform.scale(current_white_tile_unscaled, (tile_size, tile_size))
hover_current_black_tile = pygame.transform.scale(hover_current_black_unscaled, (tile_size, tile_size))
hover_current_white_tile = pygame.transform.scale(hover_current_white_unscaled, (tile_size, tile_size))


board = Board().board
othello = Othello()

# Piece sound
move_sound = pygame.mixer.Sound("Sounds/Piece_Sound.wav")

lastX = -1
lastY = -1

# NOTE: the (x, y) points are reversed in pygame, where (x) is columns and (y) is rows
# x increases going right
# y increases going down
# For updating the board sprites
def draw_board(boardc):
    board = boardc
    pos = pygame.mouse.get_pos()
    x = pos[0] // tile_size
    y = pos[1] // tile_size

    for i in range(8):
        for j in range(8):
            # For hover
            if i == x and j == y and x == lastX and y == lastY and board[i][j] == 1:
                screen.blit(hover_current_black_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and x == lastX and y == lastY and board[i][j] == 2:
                screen.blit(hover_current_white_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 0:
                screen.blit(hover_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 1:
                screen.blit(hover_black_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 2:
                screen.blit(hover_white_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 3:
                screen.blit(hover_open_tile, (i * tile_size, j * tile_size))
            
            # For normal tiles
            elif i == lastX and j == lastY and board[i][j] == 1:
                screen.blit(current_black_tile, (i * tile_size, j * tile_size))
            elif i == lastX and j == lastY and board[i][j] == 2:
                screen.blit(current_white_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 0:
                screen.blit(empty_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 1:
                screen.blit(black_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 2:
                screen.blit(white_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 3:
                screen.blit(open_tile, (i * tile_size, j * tile_size))
    pygame.display.update()


# This checks if there are available moves for the current player, otherwise it skips their turn
# FIXME: this crashes the game at the end because there are no moves to be made, so we need an end screen
def skip_turn(board, x, y):
    
    for i in range(8):
        for j in range(8):
            if board[i][j] == 3:
                return False

    if board[x][y] == 1:
        screen.blit(paused_black_tile, (x * tile_size, y * tile_size))
        pygame.display.update()
        pygame.time.delay(2000)
        screen.blit(black_tile, (x * tile_size, y * tile_size))
        
    elif board[x][y] == 2:
        screen.blit(paused_white_tile, (x * tile_size, y * tile_size))
        pygame.display.update()
        pygame.time.delay(2000)
        screen.blit(white_tile, (x * tile_size, y * tile_size))
    
    return True

def game_over(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0 or board[i][j] == 3:
                return False
    
    game_over_font = pygame.font.SysFont("microsoftsansserif", 100)
    game_over_label = game_over_font.render("GAME OVER", 1, (255, 0, 0))
    screen.blit(game_over_label, (125, 325))
    
    over = True
    
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                                
        pygame.display.update()

screen.fill((255, 255, 255))
running = True
turn = 1

# Main loop
while running:
    for event in pygame.event.get():
        
        # Closing the game
        if event.type == pygame.QUIT:
            running = False
        
        othello.check_open_moves(board, turn)
        draw_board(board)
        
        if not game_over(board):
            if lastX != -1 and lastY != -1 and skip_turn(board, x, y):
                turn = 2 if turn == 1 else 1
                continue

        pos = pygame.mouse.get_pos()
        x = pos[0] // tile_size
        y = pos[1] // tile_size

        # If you press on an open tile
        if event.type == pygame.MOUSEBUTTONDOWN and board[x][y] == 3:
            
            # Update pieces on the grid
            if turn == 1:
                board[x][y] = 1
            elif turn == 2:
                board[x][y] = 2
            
            lastX = x
            lastY = y
            
            othello.update_pieces(board, turn, x, y, "", True)
            move_sound.play()
            
            # Changing turns
            turn = 2 if turn == 1 else 1
    
    # Changed from .flip because it flipped the board
    pygame.display.update()