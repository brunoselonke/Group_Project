from piece import Piece


class GameLogic:
    # Function to update liberties after placing a piece on the board
    def updateLibertiesOnPiecePlacement(self, board, row, col):
        # Get the stone that was just placed
        placed_stone = board[row][col]

        # Define the directions to check: left, right, top, bottom
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Update liberties for the neighboring stones
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

        return True  # Stone placement successful

    # Function to calculate liberties for a stone
    def calculateLiberties(self, board, row, col):
        stone = board[row][col]
        color = stone.getPiece()

        liberties = 0

        visited = set()
        stack = [(row, col)]

        # Explore neighbors to count liberties using a stack-based approach
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue

            visited.add((r, c))
            for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_r, new_c = r + dr, c + dc

                if 0 <= new_r < len(board) and 0 <= new_c < len(board[0]):
                    neighbor = board[new_r][new_c]

                    if neighbor.getPiece() == 0:
                        liberties += 1
                    elif neighbor.getPiece() == color and (new_r, new_c) not in visited:
                        stack.append((new_r, new_c))

        stone.setLiberties(liberties)  # Set liberties count for the stone
        return liberties  # Return the calculated liberties count

    def captureStones(self, board):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        visited = set()

        for row in range(len(board)):
            for col in range(len(board[0])):
                current_stone = board[row][col]

                # Check if the stone has zero liberties and is not already captured
                if current_stone.getPiece() != Piece.NoPiece and current_stone.getPiece() not in [Piece.WhiteCaptured, Piece.BlackCaptured] and current_stone.getLiberties() == 0:
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

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                neighboring_stone = board[new_row][new_col]

                if neighboring_stone.getPiece() == color and (new_row, new_col) not in visited:
                    self.updateCapturedStones(board, new_row, new_col, color, visited)