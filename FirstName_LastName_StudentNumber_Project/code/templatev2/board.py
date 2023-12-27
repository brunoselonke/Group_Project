from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QUrl
from PyQt6.QtGui import QPainter, QColor, QImage, QPen
from PyQt6.QtTest import QTest
from piece import Piece
from game_logic import GameLogic
from PyQt6.QtGui import QPainter, QBrush
from PyQt6.QtMultimedia import QSoundEffect


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    boardSize = 6
    updateBoardStateSignal = pyqtSignal(list)  # Define the signal for updating the board state

    # TODO set the board width and height to be square
    # TODO this needs updating
    boardWidth = boardSize  # board is 0 squares wide
    boardHeight = boardSize
    timerSpeed = 1000  # the timer updates every 1 millisecond
    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        self.current_player = "Player One"
        self.game_logic = GameLogic()
        self.updateBoardStateSignal.connect(self.handleBoardStateUpdate)

    def handleBoardStateUpdate(self, updated_board_array):
        '''Handle the updated board state'''

        # You can perform any actions here based on the updated board state
        # For example, print the updated board array
        print("Updated Board State:")
        self.printBoardArray()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer
        self.boardArray = []  # TODO - create a 2d int/Piece array to store the state of the game
        self.boardArray = [[Piece(0, x, y) for x in range(self.boardHeight + 1)] for y in range(self.boardWidth + 1)]
        # +1 makes the pieces been drawn in the last column and line
        self.printBoardArray()  # TODO - uncomment this method after creating the array above
        self.margin = 100  # controls the margin between the board and the window
        self.piecesSize = 2.5  # controls pieces sizes, the smaller the number the bigger the piece

    def printBoardArray(self):
        '''prints the boardArray with black and white pieces'''
        print("boardArray:")
        for row in self.boardArray:
            row_str = ""
            for cell in row:
                if cell.getPiece() == Piece.Black:
                    row_str += "B "
                elif cell.getPiece() == Piece.White:
                    row_str += "W "
                else:
                    row_str += "- "
            print(row_str)

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return (self.contentsRect().width() - 2 * self.margin) / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return (self.contentsRect().height() - 2 * self.margin) / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        painter.translate(self.margin, self.margin)
        board_image = QImage(
            "./assets/light-wooden-background.png")  # Replace "path_to_your_board_image" with the image file path
        boardRect = self.contentsRect().adjusted(-self.margin, -self.margin, self.margin, self.margin)
        painter.drawImage(boardRect, board_image)
        self.drawPieces(painter)  # Draw pieces on top of the background
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''This event is automatically called when the mouse is pressed'''

        # Initializing sound effect
        self.piece_sound = QSoundEffect()
        self.piece_sound.setSource(QUrl.fromLocalFile("./assets/piecemove.wav"))
        self.invalid_sound = QSoundEffect()
        self.invalid_sound.setSource(QUrl.fromLocalFile("./assets/invalid.wav"))

        # Convert mouse click event to row and column
        col = int(event.position().x() // self.squareWidth()) - 1
        row = int(event.position().y() // self.squareHeight()) - 1

        # Ensure the click is within the board bounds
        if 0 <= row < Board.boardHeight + 1 and 0 <= col < Board.boardWidth + 1:
            # Get the Piece instance at the clicked position
            clicked_piece = self.boardArray[row][col]

            # Check if the clicked piece is not empty
            if clicked_piece.getPiece() == 0:
                # Check whose turn it is and update the piece accordingly
                if self.current_player == "Player One":
                    clicked_piece.Status = Piece.Black  # Update the color of the clicked piece to black for Player One
                    self.current_player = "Player Two"  # Change the turn to Player Two
                else:
                    clicked_piece.Status = Piece.White  # Update the color of the clicked piece to white for Player Two
                    self.current_player = "Player One"  # Change the turn back to Player One

                # Check if the move is valid to prevent suicide
                if self.game_logic.updateLibertiesOnPiecePlacement(self.boardArray, row, col):
                    # Play sound when placing a piece
                    self.piece_sound.play()

                    # Emit the signal with the updated board state
                    self.updateBoardStateSignal.emit(self.boardArray)

                    # Capture stones after placement
                    self.game_logic.captureStones(self.boardArray)

                    # Redraw the board
                    self.update()
                else:
                    # Play a sound indicating an invalid move (suicide prevention)
                    self.invalid_sound.play()
                    # Reset the turn back to the current player after an invalid move
                    if self.current_player == "Player One":
                        self.current_player = "Player Two"
                    else:
                        self.current_player = "Player One"

        # Emit the signal with the click location
        click_loc = "Click location [" + str(event.position().x()) + "," + str(event.position().y()) + "]"
        self.clickLocationSignal.emit(click_loc)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        self.brush = QBrush(Qt.BrushStyle.SolidPattern)
        self.brush.setColor(Qt.GlobalColor.transparent)
        border_width = 3  # Adjust this value to make the pen ticker or thicker
        border_color = Qt.GlobalColor.black  # Adjust the color as needed

        pen = QPen(border_color)
        pen.setWidth(border_width)
        painter.setPen(pen)

        painter.setBrush(self.brush)

        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                # Fill the squares with transparent color and black borders
                painter.fillRect(col, row, int(self.squareWidth()), int(self.squareHeight()), self.brush)
                painter.drawRect(col, row, int(self.squareWidth()),
                                 int(self.squareHeight()))  # Draw borders with the specified pen
                painter.restore()

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                # Determine the color of the piece based on self.boardArray[row][col]
                piece_color = self.determinePieceColor(self.boardArray[row][col])
                painter.setBrush(piece_color)
                painter.setPen(piece_color)
                # Calculate the position of the piece based on row and column
                x = col * self.squareWidth()
                y = row * self.squareHeight()
                center = QPointF(x, y)
                # Draw the piece as an ellipse
                radius = self.squareWidth() / self.piecesSize
                painter.drawEllipse(center, radius, radius)
                painter.restore()

    def determinePieceColor(self, piece_value):
        '''Determine the color of the piece based on its value'''
        # Example: If piece_value == 'W', return 'white'
        #          If piece_value == 'B', return 'black'
        #          If it's empty, return 'transparent' for empty squares
        if piece_value.getPiece() == 1:
            return QColor(Qt.GlobalColor.white)
        elif piece_value.getPiece() == 2:
            return QColor(Qt.GlobalColor.black)
        elif piece_value.getPiece() == 3:
            return QColor(Qt.GlobalColor.transparent)
        elif piece_value.getPiece() == 4:
            return QColor(Qt.GlobalColor.transparent)
        else:
            return QColor(Qt.GlobalColor.transparent)  # Adjust this based on your needs
