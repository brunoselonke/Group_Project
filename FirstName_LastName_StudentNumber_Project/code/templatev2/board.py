from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtTest import QTest
from piece import Piece
from PyQt6.QtGui import QPainter, QBrush

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location
    boardSize = 7
    # TODO set the board width and height to be square
    # TODO this needs updating
    boardWidth  = boardSize     # board is 0 squares wide
    boardHeight = boardSize
    timerSpeed  = 1000     # the timer updates every 1 millisecond
    counter     = 10    # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # game is not currently started
        self.start()                # start the game which will start the timer
        self.boardArray = []         # TODO - create a 2d int/Piece array to store the state of the game
        self.boardArray = [[Piece(self,x,y) for x in range(self.boardHeight)] for y in range(self.boardWidth)]
        self.printBoardArray()      # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True                       # set the boolean which determines if the game has started to TRUE
        self.resetGame()                            # reset the game
        self.timer.start(self.timerSpeed, self)     # start the timer with the correct speed
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
            super(Board, self).timerEvent(event)      # if we do not handle an event we should pass it to the super
                                                        # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location ["+str(event.position().x())+","+str(event.position().y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # TODO set the default colour of the brush
        self.brush = QBrush(Qt.BrushStyle.SolidPattern)
        self.brush.setColor(Qt.GlobalColor.lightGray)
        painter.setBrush(self.brush)
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col  # TODO set this value equal the transformation in the column direction
                rowTransformation = self.squareHeight() * row  # TODO set this value equal the transformation in the row direction
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(col, row, int(self.squareWidth()), int(self.squareHeight()),self.brush)  # TODO provide the required arguments
                painter.restore()
                if self.brush.color() == Qt.GlobalColor.lightGray:
                    self.brush.setColor(Qt.GlobalColor.darkGray)
                else:
                    self.brush.setColor(Qt.GlobalColor.lightGray)
                # TODO change the colour of the brush so that a checkered board is drawn

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                if col == 0 or row == 0:
                    continue
                painter.save()
                # Determine the color of the piece based on self.boardArray[row][col]
                # piece_color = self.determinePieceColor(self.boardArray[row][col])
                piece_color = QColor(Qt.GlobalColor.white)
                painter.setBrush(piece_color)
                painter.setPen(piece_color)
                # Calculate the position of the piece based on row and column
                x = col * self.squareWidth()
                y = row * self.squareHeight()
                center = QPointF(x, y)
                # Draw the piece as an ellipse
                radius = self.squareWidth()/2
                painter.drawEllipse(center, radius, radius)
                painter.restore()

    def determinePieceColor(self, piece_value):
        '''Determine the color of the piece based on its value'''
        # Example: If piece_value == 'W', return 'white'
        #          If piece_value == 'B', return 'black'
        #          If it's empty, return 'transparent' for empty squares
        if piece_value.getPiece() == 1:
            return 'white'
        elif piece_value.getPiece() == 2:
            return 'black'
        else:
            return 'transparent'  # Adjust this based on your needs
