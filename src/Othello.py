import copy


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

    def update_score(self, grid):
        white_score = sum(row.count(1) for row in grid)
        black_score = sum(row.count(2) for row in grid)
        return white_score, black_score

    def evaluateBoard(self, grid, player):
        # Simple evaluation function, just returns the difference between black and white scores
        white_score, black_score = self.update_score(grid)
        return black_score - white_score

    def computer_turn(self, grid, depth, alpha, beta, player):
        new_board = copy.deepcopy(grid)
        available_moves = self.find_available_moves(new_board, player)

        if depth == 0 or len(available_moves) == 0:
            score = self.evaluateBoard(grid, player)
            return None, score  # Return score without a move

        best_move = None
        best_score = float('-inf') if player > 0 else float('inf')

        for move in available_moves:
            x, y = move
            swappable_tiles = self.swap_tiles(x, y, new_board, player)
            new_board[x][y] = player
            for tile in swappable_tiles:
                new_board[tile[0]][tile[1]] = player

            if player == 1:
                next_player = 2
            else:
                next_player = 1

            _, value = self.computer_turn(new_board, depth - 1, alpha, beta, next_player)

            if player > 0:
                if value > best_score:
                    best_score = value
                    best_move = move
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            else:
                if value < best_score:
                    best_score = value
                    best_move = move
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break

            new_board = copy.deepcopy(grid)  # Reset the board

        return best_move, best_score

    def swap_tiles(self, x, y, grid, player):
        surround_cells = directions(x, y)
        if len(surround_cells) == 0:
            return []

        swappable_tiles = []
        for checkCell in surround_cells:
            c_x, c_y = checkCell
            difX, difY = c_x - x, c_y - y
            currentLine = []

            flag = True
            while flag:
                if grid[c_x][c_y] == player * -1:
                    currentLine.append((c_x, c_y))
                elif grid[c_x][c_y] == player:
                    flag = False
                    break
                elif grid[c_x][c_y] == 0:
                    currentLine.clear()
                    flag = False
                c_x += difX
                c_y += difY

                if c_x < 0 or c_x > 7 or c_y < 0 or c_y > 7:
                    currentLine.clear()
                    flag = False

            if len(currentLine) > 0:
                swappable_tiles.extend(currentLine)

        return swappable_tiles

    def find_available_moves(self, grid, player):
        """Takes the list of validCells and checks each to see if playable"""
        valid = self.find_valid_cells(grid, player)
        playable = []

        for cell in valid:
            x, y = cell
            if cell in playable:
                continue
            s_tiles = self.swap_tiles(x, y, grid, player)

            #if len(swapTiles) > 0 and cell not in playableCells:
            if len(s_tiles) > 0:
                playable.append(cell)

        return playable

    def find_valid_cells(self, grid, playrer):
        """Performs a check to find all empty cells that are adjacent to opposing player"""
        valid = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                dir = directions(gridX, gridY)

                for direction in dir:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == playrer:
                        continue

                    if (gridX, gridY) in valid:
                        continue

                    valid.append((gridX, gridY))
        return valid

def directions(x, y, mini_x=0, mini_y=0, maxi_x=7, maxi_y=7):
    valid_directions = []
    if x != mini_x: valid_directions.append((x - 1, y))
    if x != mini_x and y != mini_y: valid_directions.append((x - 1, y - 1))
    if x != mini_x and y != maxi_y: valid_directions.append((x - 1, y + 1))

    if x != maxi_x: valid_directions.append((x + 1, y))
    if x != maxi_x and y != mini_y: valid_directions.append((x + 1, y - 1))
    if x != maxi_x and y != maxi_y: valid_directions.append((x + 1, y + 1))

    if y != mini_y: valid_directions.append((x, y - 1))
    if y != maxi_y: valid_directions.append((x, y + 1))

    return valid_directions


