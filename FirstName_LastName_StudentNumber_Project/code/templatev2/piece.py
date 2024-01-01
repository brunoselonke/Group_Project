# TODO: Add more functions as needed for your Pieces
class Piece(object):
    NoPiece = 0  # Constant representing an empty intersection on the board
    White = 1  # Constant representing a white stone on the board
    Black = 2  # Constant representing a black stone on the board
    WhiteCaptured = 3  # Constant representing a captured white stone
    BlackCaptured = 4  # Constant representing a captured black stone
    Status = 0  # Default status, initialized to NoPiece
    liberties = 0  # Default liberties, initialized to zero
    x = -1  # Default x-coordinate, initialized to -1
    y = -1  # Default y-coordinate, initialized to -1

    def __init__(self, Piece, x, y):  # Constructor method for initializing a Piece object
        self.Status = Piece  # Set the status of the piece
        self.liberties = 0  # Initialize liberties to zero
        self.x = x  # Set the x-coordinate
        self.y = y  # Set the y-coordinate

    def getPiece(self):  # Getter method to retrieve the status of the piece (PieceType)
        return self.Status

    def getLiberties(self):  # Getter method to retrieve the number of liberties
        return self.liberties

    def setLiberties(self, liberties):  # Setter method to set the number of liberties
        self.liberties = liberties  # Update the liberties value
