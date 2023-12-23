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

        # Update the liberties of the placed stone
        self.calculateLiberties(board, row, col)

        # Check liberties of surrounding stones if the placed stone is black or white
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Check neighboring stones for potential color changes
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Ensure the new position is within the board boundaries
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                neighboring_stone = board[new_row][new_col]

                # If the neighboring position contains a stone of the opposite color
                if (placed_stone.getPiece() == Piece.Black and neighboring_stone.getPiece() == Piece.White) \
                        or (placed_stone.getPiece() == Piece.White and neighboring_stone.getPiece() == Piece.Black):

                    # Recalculate liberties for the neighboring stone
                    self.calculateLiberties(board, new_row, new_col)

                    # Check if liberties are zero and change the stone color to the placed stone's color
                    if neighboring_stone.getLiberties() == 0:
                        neighboring_stone.Status = placed_stone.getPiece()

                        # Propagate conquered pieces
                        self.propagateConquered(board, new_row, new_col, placed_stone.getPiece())

    # Function to recursively propagate conquered pieces
    def propagateConquered(self, board, row, col, color):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Check neighboring stones for color changes and update them
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Ensure the new position is within the board boundaries
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                neighboring_stone = board[new_row][new_col]

                # If the neighboring stone has the opposite color and is not yet conquered
                if neighboring_stone.getPiece() != 0 and neighboring_stone.getPiece() != color:
                    # Recalculate liberties for the neighboring stone
                    self.calculateLiberties(board, new_row, new_col)

                    # Check if liberties are zero and change the stone color to the placed stone's color
                    if neighboring_stone.getLiberties() == 0:
                        neighboring_stone.Status = color
                        # Recursively propagate conquered pieces
                        self.propagateConquered(board, new_row, new_col, color)

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
