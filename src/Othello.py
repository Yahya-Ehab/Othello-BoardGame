import copy


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
                    if i < 7 and board[i + 1][j] == 0 and board[i - 1][j] == turn:  # Check down
                        board[i + 1][j] = 3
                    if j < 7 and board[i][j + 1] == 0 and board[i][j - 1] == turn:  # Check right
                        board[i][j + 1] = 3
                    if i > 0 and board[i - 1][j] == 0 and board[i + 1][j] == turn:  # Check up
                        board[i - 1][j] = 3
                    if j > 0 and board[i][j - 1] == 0 and board[i][j + 1] == turn:  # Check left
                        board[i][j - 1] = 3


    def get_best_move(grid, depth, alpha, beta, player):
        pass


    def update_score(self, grid):
        white_score = sum(row.count(1) for row in grid)
        black_score = sum(row.count(2) for row in grid)
        return white_score, black_score

    def computerDifficulty(self, grid, depth, player):
        def minimax(grid, depth, alpha, beta, maximizing_player):
            if depth == 0:
                return None, self.evaluateBoard(grid, player)

            valid_moves = self.findAvailMoves(grid, player)
            if maximizing_player:
                max_score = float('-inf')
                best_move = None
                for move in valid_moves:
                    x, y = move
                    new_grid = copy.deepcopy(grid)
                    self.makeMove(new_grid, x, y, player)
                    _, score = minimax(new_grid, depth - 1, alpha, beta, False)
                    if score > max_score:
                        max_score = score
                        best_move = move
                    alpha = max(alpha, max_score)
                    if beta <= alpha:
                        break
                return best_move, max_score
            else:
                min_score = float('inf')
                best_move = None
                for move in valid_moves:
                    x, y = move
                    new_grid = copy.deepcopy(grid)
                    self.makeMove(new_grid, x, y, -player)
                    _, score = minimax(new_grid, depth - 1, alpha, beta, True)
                    if score < min_score:
                        min_score = score
                        best_move = move
                    beta = min(beta, min_score)
                    if beta <= alpha:
                        break
                return best_move, min_score

        return minimax(grid, depth, float('-inf'), float('inf'), True)

    def evaluateBoard(self, grid, player):
        # Simple evaluation function, just returns the difference between black and white scores
        white_score, black_score = self.update_score(grid)
        return black_score - white_score

    def findAvailMoves(self, grid, player):
        moves = []
        for i in range(8):
            for j in range(8):
                if grid[i][j] == 0:
                    if self.isValidMove(grid, i, j, player):
                        moves.append((i, j))
        return moves

    def isValidMove(self, grid, x, y, player):
        if grid[x][y] != 0:
            return False
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            tx, ty = x + dx, y + dy
            if 0 <= tx < 8 and 0 <= ty < 8 and grid[tx][ty] == -player:
                while 0 <= tx < 8 and 0 <= ty < 8:
                    if grid[tx][ty] == 0:
                        break
                    if grid[tx][ty] == player:
                        return True
                    tx += dx
                    ty += dy
        return False

    def makeMove(self, grid, x, y, player):
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            tx, ty = x + dx, y + dy
            if 0 <= tx < 8 and 0 <= ty < 8 and grid[tx][ty] == -player:
                to_flip = []
                while 0 <= tx < 8 and 0 <= ty < 8:
                    if grid[tx][ty] == 0:
                        break
                    if grid[tx][ty] == player:
                        for px, py in to_flip:
                            grid[px][py] = player
                        break
                    to_flip.append((tx, ty))
                    tx += dx
                    ty += dy
        grid[x][y] = player
