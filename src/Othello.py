class Othello:
    def __init__(self) -> None:
        pass

    # This is what actually detects the valid moves and assigns them (Must be in a straight line)
    def assign_open_moves(self, board, turn, x, y, found, direction, start):
        reverse_turn = 2 if turn == 1 else 1

        # Define the valid directions
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

        # If its an empty tile and the piece before it is not yours, then we can put our piece after it
        if board[x][y] == 0:
            if found:
                board[x][y] = 3
            else:
                return

        # If its not our piece, then we change found to true to indicate that if we find an empty tile next, we can put our piece on it
        if board[x][y] == reverse_turn:
            found = True

        # Otherwise if its an open tile, we return, because we can do nothing 
        if board[x][y] == 3 or (board[x][y] == turn and found):
            return

        # This goes through each direction if we're on the starting piece, otherwise it goes through the direction given to it
        for dir, (dx, dy) in directions.items():
            # Check if direction is valid and new tile is within boundaries
            if (dir == direction or start) and 0 <= dx + x <= 7 and 0 <= dy + y <= 7:
                self.assign_open_moves(board, turn, x + dx, y + dy, found, dir, start=False)

    # This clears the board and checks which pieces it should check its open moves
    def check_open_moves(self, board, turn):

        # This clears all the previously assigned valid moves so we can detect new ones
        for i in range(8):
            for j in range(8):
                if board[i][j] == 3:
                    board[i][j] = 0

        # This goes through the entire board and when it detects your piece, it calls the assign function
        for i in range(8):
            for j in range(8):
                if board[i][j] == turn:
                    self.assign_open_moves(board, turn, i, j, False, "", True)

    # This is to update the board pieces when making a move, it works by iterating over the dictionary of moves and trying each one if we're still at the start.
    # Otherwise it just uses the direction given to it, it uses recursion to call itself, and iteration to go through the directions, this makes the code much shorter than what we had
    def update_pieces(self, board, turn, x, y, direction, start):

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
                if self.update_pieces(board, turn, x + dx, y + dy, dir, start=False):
                    board[x][y] = turn

                    # If we're not at the start, we return true, otherwise we return nothing to allow it to check other directions
                    if not start:
                        return True

                # Else if we get false, we check if we're not at the start before returning it, to allow it to also check other directions
                elif not start:
                    return False

        # If we're out of the boundaries, we return false                    
        return False

    # Updating scoreboard by counting pieces
    def update_score(self, grid):
        white_score = sum(row.count(1) for row in grid)
        black_score = sum(row.count(2) for row in grid)
        return white_score, black_score

    def evaluateBoard(self, grid, player):
        # Simple evaluation function, just returns the difference between black and white scores
        white_score, black_score = self.update_score(grid)
        return black_score - white_score

    def computer_turn(self, grid, depth, alpha, beta, player):
        def max_value(grid, depth, alpha, beta):
            if depth == 0:
                return self.evaluateBoard(grid, player)

            max_val = -float('inf')
            for move in self.get_valid_moves(grid, player):
                new_grid = self.simulate_move(grid, move[0], move[1], player)
                val = min_value(new_grid, depth - 1, alpha, beta)
                max_val = max(max_val, val)
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break  # Beta cut-off

            return max_val

        def min_value(grid, depth, alpha, beta):
            if depth == 0:
                return self.evaluateBoard(grid, player)

            min_val = float('inf')
            opponent = 1 if player == 2 else 2
            for move in self.get_valid_moves(grid, opponent):
                new_grid = self.simulate_move(grid, move[0], move[1], opponent)
                val = max_value(new_grid, depth - 1, alpha, beta)
                min_val = min(min_val, val)
                beta = min(beta, min_val)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_val

        best_move = None
        max_val = -float('inf')
        for move in self.get_valid_moves(grid, player):
            new_grid = self.simulate_move(grid, move[0], move[1], player)
            val = min_value(new_grid, depth - 1, alpha, beta)
            if val > max_val:
                max_val = val
                best_move = move
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break  # Beta cut-off
        return best_move, max_val

    def get_valid_moves(self, grid, player):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if grid[i][j] == 3:
                    valid_moves.append((i, j))
        return valid_moves

    def simulate_move(self, grid, x, y, player):
        new_grid = [row[:] for row in grid]
        new_grid[x][y] = player
        self.update_pieces(new_grid, player, x, y, "", True)
        return new_grid
