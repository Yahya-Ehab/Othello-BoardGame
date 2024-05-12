# Board class for the Othello game
# 0 = empty, 1 = white, 2 = black
class Board:
    def __init__(self):
        self.board = [[0 for i in range(8)] for j in range(8)]
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[3][3] = 2
        self.board[4][4] = 2
        