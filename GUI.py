import pygame
from src.Board import Board
from src.Othello import Othello
from src.AI import AI


# TODO:
# AI SOMETIMES CHECKS OUT OF BOUNDS (???)
# AI OVERWRITES PIECES SOMETIMES (FIXED)
# EACH PLAYER MUST HAVE 30 TURNS ONLY (DONE)
# WHITE OR BLACK MAY GET EATEN AND CRASH THE GAME (FIXED)

pygame.init()
pygame.mixer.init()

# Set up the window
WINDOW_SIZE = 800
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Othello")

background_image = pygame.image.load("Images/bg.jpeg").convert()
# background_image = pygame.transform.scale(background_image, (800, 800))


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
ai = AI()

# Piece sound
move_sound = pygame.mixer.Sound("Sounds/Piece_Sound.wav")

lastX = -1
lastY = -1

# NOTE: the (x, y) points are reversed in pygame, where (x) is columns and (y) is rows
# x increases going right
# y increases going down
# For updating the board sprites
def draw_board(grid):
    board = grid
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
def skip_turn(board, x, y):
    
    for i in range(8):
        for j in range(8):
            if board[i][j] == 3:
                return False

    # Black
    if board[x][y] == 1:
        screen.blit(paused_black_tile, (x * tile_size, y * tile_size))
        pygame.display.update()
        pygame.time.delay(2000)
        screen.blit(black_tile, (x * tile_size, y * tile_size))
    
    # White
    elif board[x][y] == 2:
        screen.blit(paused_white_tile, (x * tile_size, y * tile_size))
        pygame.display.update()
        pygame.time.delay(2000)
        screen.blit(white_tile, (x * tile_size, y * tile_size))
    
    return True


# This is to prevent the crashing of the program at the end, till we implement a proper menu and game over screen
def end_game(black_score, white_score, black_turns, white_turns):
    
    white = False 
    black = False
    
    # To check if no white or black pieces exist
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                white = True
            elif board[i][j] == 2:
                black = True

    
    # To check if we can't make anymore moves
    if black and white and black_turns < 31 and white_turns < 31 and black_score + white_score < 64:
        return False
    
    winner_font = pygame.font.SysFont("microsoftsansserif", 64)
    game_over_font = pygame.font.SysFont("microsoftsansserif", 100)
    game_over = game_over_font.render("Game Over", 1, (230, 211, 0))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(WINDOW_SIZE // 8, WINDOW_SIZE // 5, 600, 500))
    
    if black_score > white_score:
        winner = winner_font.render("Black wins!", True, (255, 255, 255))
    elif white_score > black_score:
        winner = winner_font.render("White wins!", True, (255, 255, 255))
    else:
        winner = winner_font.render("It's a draw!", True, (255, 255, 255))
    
    screen.blit(game_over, (WINDOW_SIZE // 5.5, WINDOW_SIZE // 3))
    screen.blit(winner, (WINDOW_SIZE // 3.3, WINDOW_SIZE // 1.8))
    
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()


# Draw the main menu
def main_menu():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 38)
    pvp_text = font.render("Player vs Player", True, (255, 255, 255))
    pvc_text = font.render("Player vs Computer", True,(255, 255, 255))
    screen.blit(pvp_text, (400, 500))
    screen.blit(pvc_text, (400, 600))


# Draw the difficulty selection menu
def difficulty_menu():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 36)
    easy_text = font.render("Easy", True, (255, 255, 255))
    medium_text = font.render("Medium", True, (255, 255, 255))
    hard_text = font.render("Hard", True, (255, 255, 255))
    screen.blit(easy_text, (400, 500))
    screen.blit(medium_text, (400, 600))
    screen.blit(hard_text, (400, 700))



# TODO: REMEMBER TO RESET THESE EVERY NEW GAME
turn = 1
depth = None
running = True
white_turns = 0
black_turns = 0
black_score = 0
white_score = 0
first_play = True
current_mode = None
current_difficulty = None

# Main loop
while running:
    for event in pygame.event.get():
        
        # Closing the game
        if event.type == pygame.QUIT:
            running = False
            
        # Depending on the current mode, draw the appropriate menu or the game board
        if current_mode is None:
            main_menu()
        elif current_mode == "PvC" and current_difficulty is None:
            difficulty_menu()
        
        # Main Menu
        if current_mode == None or current_mode == "PvC":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]

                # Select Game Mode
                if current_mode is None:                    
                    # Check if the click was in the menu area
                    if 400 < pos[0] < 600 and 500 < pos[1] < 550:
                        current_mode = "PvP"
                    elif 400 < pos[0] < 600 < pos[1] < 650:
                        current_mode = "PvC"
                        
                # Select AI Difficulty
                elif current_mode == "PvC" and current_difficulty is None:
                    # Check if the click was in the difficulty menu area
                    if 400 < pos[0] < 500 < pos[1] < 550:
                        current_difficulty = "Easy"
                        depth = 1
                    elif 400 < pos[0] < 550 and 600 < pos[1] < 650:
                        current_difficulty = "Medium"
                        depth = 3
                    elif 400 < pos[0] < 500 and 700 < pos[1] < 750:
                        current_difficulty = "Hard"
                        depth = 5

        # Player Vs Player
        if current_mode == "PvP":
            othello.check_open_moves(board, turn)
            draw_board(board)
            
            # Checking if game is over, or if turn needs skipping
            if not end_game(black_score, white_score, black_turns, white_turns):
                if lastX != -1 and lastY != -1 and skip_turn(board, x, y):
                    turn = 2 if turn == 1 else 1
                    continue
            
            # This is to prevent pressing on the button and putting a piece at the same time
            if first_play:
                first_play = False
                continue

            # Getting mouse coordinates
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size

            # If you press on an open tile
            if event.type == pygame.MOUSEBUTTONDOWN and board[x][y] == 3:
                
                # Update turn and register move
                if turn == 1:
                    board[x][y] = 1
                    black_turns += 1
                elif turn == 2:
                    board[x][y] = 2
                    white_turns += 1
                
                # Last piece's position
                lastX = x
                lastY = y
                
                # Piece movement sound
                move_sound.play()
                
                # Update pieces
                othello.update_pieces(board, turn, x, y, "", True)
                
                # Update scores 
                black_score, white_score = othello.update_score(board)
                
                # Changing turns
                turn = 2 if turn == 1 else 1
                
                # Scoreboard
                print(f'Score: Black -> {black_score}, White -> {white_score}')
                print(f'Black turn: {black_turns}, White turns: {white_turns}')


        # Player Vs AI
        if current_mode == "PvC" and current_difficulty:
            
            # Reset play condition
            played = False
            othello.check_open_moves(board, turn)
            draw_board(board)

            # Checking if game is over, or if turn needs skipping
            if not end_game(black_score, white_score, black_turns, white_turns):
                if lastX != -1 and lastY != -1 and skip_turn(board, x, y):
                    turn = 2 if turn == 1 else 1
                    continue

            # This is to prevent pressing on the button and putting a piece at the same time
            if first_play:
                first_play = False
                continue

            # Player's Turn
            if turn == 1:
                pos = pygame.mouse.get_pos()
                x = pos[0] // tile_size
                y = pos[1] // tile_size
                
                # Update pieces on the grid
                if event.type == pygame.MOUSEBUTTONDOWN and board[x][y] == 3:
                    board[x][y] = 1
                    black_turns += 1
                    played = True

            # AI's Turn
            elif turn == 2:
                pygame.time.delay(500)  # Delay to give time for the player to see the AI move
                best_move, _ = ai.computer_turn(board, depth, -64, 64, 2) # Getting the current best move
                
                # If it isn't none, then we register that move and change the play condition
                if best_move:
                    x, y = best_move
                    board[x][y] = 2
                    white_turns += 1
                    played = True
                else:
                    print("NO BEST MOVE\n\n\n")


            if played:
                
                # Last piece's position
                lastX = x
                lastY = y
                
                # Piece movement sound
                move_sound.play()
                
                # Update pieces
                othello.update_pieces(board, turn, x, y, "", True)
                
                # Update scores 
                black_score, white_score = othello.update_score(board)
                
                # Changing turns
                turn = 2 if turn == 1 else 1

                # Scoreboard
                print(f'Score: Black -> {black_score}, White -> {white_score}')
                print(f'Black turn: {black_turns}, White turns: {white_turns}')
                
    # Changed from .flip because it flipped the board
    pygame.display.update()

pygame.quit()
