from piece import Piece

class GameLogic:
    def __init__(self):
        self.history = []  # Initialize the history attribute

    # Function to update liberties after placing a piece on the board
    def updateLibertiesOnPiecePlacement(self, board, row, col):
        placed_stone = board[row][col]

        # Save the original board state before the move
        original_board = self.copyBoard(board)

        # Update liberties for the neighboring stones
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Ensure the new position is within the board boundaries
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                neighboring_stone = board[new_row][new_col]

                # If the neighboring position contains a stone
                if neighboring_stone.getPiece() != 0:
                    # Recalculate liberties for the neighboring stone
                    self.calculateLiberties(board, new_row, new_col)

        # Check if placing the stone results in immediate loss of liberties
        if self.calculateLiberties(board, row, col) == 0:
            return False  # Placement results in suicide, disallow it

        # Update the liberties of the placed stone
        self.calculateLiberties(board, row, col)

        # Check for repeated position (Ko rule)
        if self.isRepeatedPosition(board):
            # Restore the original board state
            self.restoreOriginalBoard(board, original_board)
            return False  # Disallow move due to Ko rule

        # Update the history with the current board state
        self.history.append(self.copyBoard(board))

        return True  # Stone placement successful

    def restoreOriginalBoard(self, current_board, original_board):
        for i in range(len(current_board)):
            for j in range(len(current_board[0])):
                current_board[i][j].Status = original_board[i][j].Status
                current_board[i][j].liberties = original_board[i][j].liberties

    def isRepeatedPosition(self, current_board):
        current_state = self.copyBoardIgnoringLiberties(current_board)

        for past_board in self.history[:-1]:  # Exclude the initial state from comparison
            if self.areBoardsEqualIgnoringLiberties(current_state, past_board):
                return True
        return False

    def areBoardsEqualIgnoringLiberties(self, board1, board2):
        for i in range(len(board1)):
            for j in range(len(board1[0])):
                if board1[i][j].getPiece() != board2[i][j].getPiece():
                    return False
        return True

    def copyBoardIgnoringLiberties(self, board):
        return [[Piece(cell.getPiece(), cell.x, cell.y) for cell in row] for row in board]

    def copyBoard(self, board):
        return [[Piece(cell.getPiece(), cell.x, cell.y) for cell in row] for row in board]

    def areBoardsEqual(self, board1, board2):
        for i in range(len(board1)):
            for j in range(len(board1[0])):
                if (
                        board1[i][j].getPiece() != board2[i][j].getPiece()
                        or board1[i][j].getLiberties() != board2[i][j].getLiberties()
                ):
                    return False
        return True

    # Function to calculate liberties for a stone
    def calculateLiberties(self, board, row, col):
        stone = board[row][col]
        color = stone.getPiece()

        liberties = 0

        visited = set()
        stack = [(row, col)]

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue

            visited.add((r, c))
            for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_r, new_c = r + dr, c + dc

                if 0 <= new_r < len(board) and 0 <= new_c < len(board[0]):
                    neighbor = board[new_r][new_c]

                    if neighbor.getPiece() == 0 or neighbor.getPiece() == 3 or neighbor.getPiece() == 4:
                        liberties += 1
                    elif neighbor.getPiece() == color and (new_r, new_c) not in visited:
                        stack.append((new_r, new_c))

        stone.setLiberties(liberties)  # Set liberties count for the stone

        # Recursively update liberties for neighboring stones
        while stack:
            r, c = stack.pop()
            for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_r, new_c = r + dr, c + dc

                if 0 <= new_r < len(board) and 0 <= new_c < len(board[0]):
                    self.calculateLiberties(board, new_r, new_c)

        return liberties  # Return the calculated liberties count

    def captureStones(self, board):
        visited = set()

        for row in range(len(board)):
            for col in range(len(board[0])):
                current_stone = board[row][col]

                # Check if the stone has zero liberties and is not already captured
                if (
                        current_stone.getPiece() != Piece.NoPiece
                        and current_stone.getPiece() not in [Piece.WhiteCaptured, Piece.BlackCaptured]
                        and current_stone.getLiberties() == 0
                ):
                    color = current_stone.getPiece()

                    # Capture stones recursively for each stone with zero liberties
                    if (row, col) not in visited:
                        self.updateCapturedStones(board, row, col, color, visited)

    # Helper method to update captured stones recursively
    def updateCapturedStones(self, board, row, col, color, visited):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        visited.add((row, col))

        current_stone = board[row][col]
        current_stone.Status = Piece.WhiteCaptured if color == Piece.White else Piece.BlackCaptured

        # Update liberties for the current stone
        self.calculateLiberties(board, row, col)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                neighboring_stone = board[new_row][new_col]

                if neighboring_stone.getPiece() == color and (new_row, new_col) not in visited:
                    # Update liberties for the neighboring stone
                    self.updateCapturedStones(board, new_row, new_col, color, visited)

    def calculatePoints(self, board):
        # Initialize point counters for each player
        points_player_one = 0
        points_player_two = 0

        # Iterate through the board to count territory and captured stones
        for row in range(len(board)):
            for col in range(len(board[0])):
                current_stone = board[row][col]

                if current_stone.getPiece() == Piece.Black:
                    points_player_one += 1
                elif current_stone.getPiece() == Piece.White:
                    points_player_two += 1
                elif current_stone.getPiece() == Piece.WhiteCaptured:
                    points_player_one += 1
                    points_player_two -= 1
                elif current_stone.getPiece() == Piece.BlackCaptured:
                    points_player_two += 1
                    points_player_one -= 1
                else:
                    # Check if the empty intersection is surrounded by a single color
                    surrounding_colors = set()

                    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                        new_row, new_col = row + dr, col + dc

                        if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                            neighboring_stone = board[new_row][new_col]
                            surrounding_colors.add(neighboring_stone.getPiece())

                    # If the empty intersection is surrounded by a single color, add to territory
                    if len(surrounding_colors) == 1:
                        territory_color = surrounding_colors.pop()
                        if territory_color == Piece.White:
                            points_player_one += 1
                        elif territory_color == Piece.Black:
                            points_player_two += 1

        # Print or use the points for further processing
        print("Player One Points:", points_player_one)
        print("Player Two Points:", points_player_two)

        return points_player_one, points_player_two

    # Helper method to get the neighboring color of a position on the board
    def getNeighboringColor(self, board, row, col):
        # Define the directions to check: left, right, top, bottom
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        neighboring_colors = set()

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Ensure the new position is within the board boundaries
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                neighboring_stone = board[new_row][new_col]

                # If the neighboring position contains a stone
                if neighboring_stone.getPiece() != 0:
                    neighboring_colors.add(neighboring_stone.getPiece())

        if len(neighboring_colors) >= 1:
            return neighboring_colors.pop()
        else:
            return None  # Multiple neighboring colors or no neighboring colors

# End of the GameLogic class
