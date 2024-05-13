import pygame
from src.Board import Board
from src.Othello import Othello

pygame.init()
pygame.mixer.init()

# Set up the window
WINDOW_SIZE = 800
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Othello")

background_image = pygame.image.load("Images/bg.jpeg").convert()
# background_image = pygame.transform.scale(background_image, (800, 800))


# Load tile sprites
empty_tile_unscaled = pygame.image.load("Images/Empty Tile.png")
black_tile_unscaled = pygame.image.load("Images/Black Tile.png")
white_tile_unscaled = pygame.image.load("Images/White Tile.png")
open_tile_unscaled = pygame.image.load("Images/Open Tile.png")
hover_tile_unscaled = pygame.image.load("Images/Hover Tile.png")
hover_white_tile_unscaled = pygame.image.load("Images/Hover White Tile.png")
hover_black_tile_unscaled = pygame.image.load("Images/Hover Black Tile.png")
hover_open_tile_unscaled = pygame.image.load("Images/Hover Open Tile.png")

# Setup tiles
tile_size = int(WINDOW_SIZE / 8)
empty_tile = pygame.transform.scale(empty_tile_unscaled, (tile_size, tile_size))
black_tile = pygame.transform.scale(black_tile_unscaled, (tile_size, tile_size))
white_tile = pygame.transform.scale(white_tile_unscaled, (tile_size, tile_size))
open_tile = pygame.transform.scale(open_tile_unscaled, (tile_size, tile_size))
hover_tile = pygame.transform.scale(hover_tile_unscaled, (tile_size, tile_size))
hover_white_tile = pygame.transform.scale(hover_white_tile_unscaled, (tile_size, tile_size))
hover_black_tile = pygame.transform.scale(hover_black_tile_unscaled, (tile_size, tile_size))
hover_open_tile = pygame.transform.scale(hover_open_tile_unscaled, (tile_size, tile_size))
board = Board().board
othello = Othello()

# Piece sound
move_sound = pygame.mixer.Sound("Sounds/Piece_Sound.wav")


# NOTE: the (x, y) points are reversed in pygame, where (x) is columns and (y) is rows
# For updating the board sprites
def draw_board(grid):
    board = grid
    pos = pygame.mouse.get_pos()
    x = pos[0] // tile_size
    y = pos[1] // tile_size

    for i in range(8):
        for j in range(8):
            # For hover
            if i == x and j == y and board[i][j] == 0:
                screen.blit(hover_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 1:
                screen.blit(hover_black_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 2:
                screen.blit(hover_white_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 3:
                screen.blit(hover_open_tile, (i * tile_size, j * tile_size))

            # For normal tiles
            elif board[i][j] == 0:
                screen.blit(empty_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 1:
                screen.blit(black_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 2:
                screen.blit(white_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 3:
                screen.blit(open_tile, (i * tile_size, j * tile_size))
    pygame.display.flip()


# Function to draw the main menu
def draw_menu():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 38)
    pvp_text = font.render("Player vs Player", True, (255, 255, 255))
    pvc_text = font.render("Player vs Computer", True,(255, 255, 255))
    screen.blit(pvp_text, (400, 500))
    screen.blit(pvc_text, (400, 600))


# Function to draw the difficulty selection menu
def draw_difficulty_menu():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 36)
    easy_text = font.render("Easy", True, (255, 255, 255))
    medium_text = font.render("Medium", True, (255, 255, 255))
    hard_text = font.render("Hard", True, (255, 255, 255))
    screen.blit(easy_text, (400, 500))
    screen.blit(medium_text, (400, 600))
    screen.blit(hard_text, (400, 700))


def display_end_game_message(winner):
    font = pygame.font.Font(None, 64)
    if winner == 1:
        text = font.render("Black wins!", True, (255, 255, 255))
    elif winner == 2:
        text = font.render("White wins!", True, (255, 255, 255))
    else:
        text = font.render("It's a draw!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

# Main loop
running = True
current_mode = None
current_difficulty = None
turn = 1
depth = None
black_score = 2
white_score = 2
game_ended = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]

            if current_mode is None:
                # Check if the click was in the menu area
                if 400 < pos[0] < 600 and 500 < pos[1] < 550:
                    current_mode = "PvP"
                elif 400 < pos[0] < 600 < pos[1] < 650:
                    current_mode = "PvC"
            elif current_mode == "PvC" and current_difficulty is None:
                # Check if the click was in the difficulty menu area
                if 400 < pos[0] < 500 < pos[1] < 550:
                    current_difficulty = "Easy"
                    depth = 3
                elif 400 < pos[0] < 550 and 600 < pos[1] < 650:
                    current_difficulty = "Medium"
                    depth = 4
                elif 400 < pos[0] < 500 and 700 < pos[1] < 750:
                    current_difficulty = "Hard"
                    depth = 5

            if current_mode == "PvP" or (current_mode == "PvC" and current_difficulty):
                othello.detect_valid_moves(board, turn)
                draw_board(board)
                pos = pygame.mouse.get_pos()

                x = pos[0] // tile_size
                y = pos[1] // tile_size

                if board[x][y] == 3:
                    # Adding new pieces
                    if turn == 1:
                        board[x][y] = 1
                        turn = 2
                    elif turn == 2:
                        if current_mode == "PvC":
                            # If it's the computer's turn in PvC mode, let the computer make a move
                            best_move, _ = othello.computerDifficulty(board, depth, 2)
                            if best_move:
                                x, y = best_move
                                board[x][y] = 2
                        else:
                            board[x][y] = 2
                        turn = 1
                        # Update scores
                    white_score, black_score = othello.update_score(board)

                    if black_score + white_score == 64:
                        game_ended = True
                        if black_score > white_score:
                            display_end_game_message(1)
                        elif white_score > black_score:
                            display_end_game_message(2)
                        else:
                            display_end_game_message(0)

                    move_sound.play()
                    print(x, y)
                    print("score :", white_score, black_score)  # to test the score

    # Depending on the current mode, draw the appropriate menu or the game board
    if current_mode is None:
        draw_menu()
    elif current_mode == "PvC" and current_difficulty is None:
        draw_difficulty_menu()
    else:
        if not game_ended:  # Only draw the board if the game has not ended
            othello.detect_valid_moves(board, turn)
            draw_board(board)

    pygame.display.flip()

pygame.quit()
