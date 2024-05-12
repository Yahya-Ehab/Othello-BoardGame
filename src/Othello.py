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
                    if i < 7 and board[i + 1][j] == 0 and board[i - 1][j] == turn: # Check down
                        board[i + 1][j] = 3
                    if j < 7 and board[i][j + 1] == 0 and board[i][j - 1] == turn: # Check right
                        board[i][j + 1] = 3
                    if i > 0 and board[i - 1][j] == 0 and board[i + 1][j] == turn: # Check up
                        board[i - 1][j] = 3
                    if j > 0 and board[i][j - 1] == 0 and board[i][j + 1] == turn: # Check left
                        board[i][j - 1] = 3
