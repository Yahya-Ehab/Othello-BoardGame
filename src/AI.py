from src.Othello import Othello

othello = Othello()
class AI:
    def __init__(self) -> None:
        pass
    
    def computer_turn(self, grid, depth, alpha, beta, player):
        def max_value(grid, depth, alpha, beta):
            if depth == 0 or len(self.get_valid_moves(grid)) == 0:
                return othello.evaluate_board(grid)

            max_val = -64
            for move in self.get_valid_moves(grid):
                new_grid = self.simulate_move(grid, move[0], move[1], player)
                val = min_value(new_grid, depth - 1, alpha, beta)
                max_val = max(max_val, val)
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break  # Beta cut-off

            return max_val

        def min_value(grid, depth, alpha, beta):
            if depth == 0 or len(self.get_valid_moves(grid)) == 0:
                return othello.evaluate_board(grid)

            min_val = 64
            opponent = 1 if player == 2 else 2
            for move in self.get_valid_moves(grid):
                new_grid = self.simulate_move(grid, move[0], move[1], opponent)
                val = max_value(new_grid, depth - 1, alpha, beta)
                min_val = min(min_val, val)
                beta = min(beta, min_val)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_val

        best_move = None
        max_val = -64
        for move in self.get_valid_moves(grid):
            new_grid = self.simulate_move(grid, move[0], move[1], player)
            val = min_value(new_grid, depth - 1, alpha, beta)
            if val > max_val:
                max_val = val
                best_move = move
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break  # Beta cut-off
                
        return best_move, max_val

    def get_valid_moves(self, grid):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if grid[i][j] == 3:
                    valid_moves.append((i, j))
        return valid_moves

    def simulate_move(self, grid, x, y, player):
        new_grid = [row[:] for row in grid]
        new_grid[x][y] = player
        othello.update_pieces(new_grid, player, x, y, "", True)
        return new_grid

    