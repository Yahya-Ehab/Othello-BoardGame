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

        # Otherwise if its an open tile, we return, because we can do nothing or if we find our tile again after find the opposite
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
        black_score = sum(row.count(1) for row in grid)
        white_score = sum(row.count(2) for row in grid)
        return black_score, white_score


    # Simple evaluation function, just returns the difference between black and white scores
    def evaluate_board(self, grid):
        black_score, white_score = self.update_score(grid)
        return black_score - white_score
    