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
    
    
    
    # This is to update the board pieces when making a move, it works by iterating over the dictionary of moves and trying each one if we're still at the start.
    # Otherwise it just uses the direction given to it, it uses recursion to call itself, and iteration to go through the directions, this makes the code much shorter than what we had
    def improved_update_pieces(self, board, turn, x, y, direction, start):
        
        # We define all the directions we can go and their dx, dy
        directions = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1),
            "up-left": (-1, -1),
            "up-right": (1, -1),
            "down-left": (-1, 1),
            "down-right": (1, 1)
        }
        
        # Making sure we're not checking the start piece then, checks if the piece we're on is the same color as our piece
        if board[x][y] == turn and not start:
            return True
        
        # This checks if the piece we're on is either empty or open
        if board[x][y] in [0, 3]:
            return False

        # If we find a piece with similar color on any direction, we return true and change its color
        # Otherwise we try another direction
        for dir, (dx, dy) in directions.items():
            if (dir == direction or start) and 0 <= x + dx < 8 and 0 <= y + dy < 8:
                if self.improved_update_pieces(board, turn, x + dx, y + dy, dir, start = False):
                    board[x][y] = turn
                    
                    # If we're not at the start, we return true, otherwise we return nothing to allow it to check other directions
                    if not start:
                        return True
                
                # Else if we get false, we check if we're not at the start before returning it, to allow it to also check other directions
                elif not start:
                        return False
        
        # If we're out of the boundaries, we return false                    
        return False