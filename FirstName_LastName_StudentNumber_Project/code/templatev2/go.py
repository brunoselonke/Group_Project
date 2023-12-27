from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        # Set up menus
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        gameMenu = mainMenu.addMenu("Game Menu")
        helpMenu = mainMenu.addMenu(" Help")

        # Quit Game action setup
        quitGameAction = QAction("Quit Game", self)
        quitGameAction.setShortcut("Ctrl+Q")
        gameMenu.addAction(quitGameAction)  # Quit Game Action
        #quitGameAction.triggered.connect(self.quitGame)  # Connect clear action to the clear method


    def getBoard(self):
        return self.board

    # def getScoreBoard(self):
    #     return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.setFixedSize(700, 700)  # Set a fixed size for the window
        self.board = Board(self)
        self.setCentralWidget(self.board)
        # self.scoreBoard = ScoreBoard()
##      self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        # self.scoreBoard.make_connection(self.board)

        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        #size = self.geometry()
        #self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)
