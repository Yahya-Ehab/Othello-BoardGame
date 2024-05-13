class Othello:
    def __init__(self) -> None:
        pass
    
    # This detects all the valid moves you can make based on your turn
    def detect_valid_moves(self, board, turn):
        # This clears all the previously assigned valid moves so we can detect new ones
        for i in range(8):
            for j in range(8):
                if board[i][j] == 3:
                        board[i][j] = 0
        
        # This detects the valid moves and assigns them (Must be in a straight line)
        reverse_turn = 2 if turn == 1 else 1
        for i in range(8):
            for j in range(8):
                if board[i][j] == reverse_turn:
                #    (In boundary)   (Block is empty)    (Opposite block is opposite color)
                    if i < 7 and board[i + 1][j] == 0 and board[i - 1][j] == turn: # Check right
                        board[i + 1][j] = 3
                    if j < 7 and board[i][j + 1] == 0 and board[i][j - 1] == turn: # Check down
                        board[i][j + 1] = 3
                    if i > 0 and board[i - 1][j] == 0 and board[i + 1][j] == turn: # Check left
                        board[i - 1][j] = 3
                    if j > 0 and board[i][j - 1] == 0 and board[i][j + 1] == turn: # Check up
                        board[i][j - 1] = 3
    
    
    
    # This is to update the board pieces when making a move
    # It keeps recursively calling the pieces around us to check if they lead to a piece of the same color
    # If not it returns false, this also happens when first calling it only
    # On any sequential calls, one direction is only chosen for the call after to prevent unnecessary loops and incorrect piece changing
    # FIXME: Unfortunately, this updates till it sees the first piece with the same color, meaning if we have (O X O X O) its gonna be only be (O O O X O) meaning one piece wont be changed
    def change_pieces(self, board, turn, x, y, direction, start):
 
        # It works first by making sure we're not checking the start piece
        # After that it checks if the piece we're on is the same color as our piece
        if board[x][y] == turn and not start:
            return True
        
        # This checks if the piece we're on is either empty or open
        if board[x][y] in [0, 3]:
            return False

        # This is to check the piece on our right
        if x < 7 and (direction == "right" or start):
            if(self.change_pieces(board, turn, x + 1, y, "right", start = False)):
                board[x][y] = turn
                
                # This stupid part is to allow it to check all directions on start and stop it from return and not checking the other directions
                # TODO: Optimize this crap
                if not start:
                    return True
                else:
                    pass
            else:
                if not start:
                    return False
                else:
                    pass
        
        # This is to check the piece below us
        if y < 7 and (direction == "down" or start):
            if(self.change_pieces(board, turn, x, y + 1, "down", start = False)):
                board[x][y] = turn
                if not start:
                    return True
                else:
                    pass
            else:
                if not start:
                    return False
                else:
                    pass
        
        # This is to check the piece above us
        if y > 0 and (direction == "up" or start):
            if(self.change_pieces(board, turn, x, y - 1, "up", start = False)):
                board[x][y] = turn
                if not start:
                    return True
                else:
                    pass
            else:
                if not start:
                    return False
                else:
                    pass
        
        # This is to check the piece on our left
        if x > 0 and (direction == "left" or start):
            if(self.change_pieces(board, turn, x - 1, y, "left", start = False)):
                board[x][y] = turn
                if not start:
                    return True
                else:
                    pass
            else:
                if not start:
                    return False
                else:
                    pass
