from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard

class Go(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates application UI'''
        self.setFixedSize(700, 700)  # Set a fixed size for the window
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.center()
        self.setWindowTitle('Go')
        self.show()

        # Create the scoreboard instance
        self.scoreBoard = ScoreBoard()

        # Access the Board instance and update stats on the scoreboard
        white_prisoners, black_prisoners = self.board.countPrisoners()
        current_player = self.board.current_player
        self.scoreBoard.updateStats(current_player, white_prisoners, black_prisoners)

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        gr.moveCenter(screen)
        self.move(gr.topLeft())

        # Set up menus
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        gameMenu = mainMenu.addMenu("Game Menu")
        helpMenu = mainMenu.addMenu(" Help")

        # Stats action setup
        statsAction = QAction("Stats", self)
        statsAction.setShortcut("Ctrl+S")
        gameMenu.addAction(statsAction)
        statsAction.triggered.connect(self.board.openScoreBoard)  # Connect clear action to the clear method

        # Quit Game action setup
        quitGameAction = QAction("Quit Game", self)
        quitGameAction.setShortcut("Ctrl+Q")
        gameMenu.addAction(quitGameAction)  # Quit Game Action
        #quitGameAction.triggered.connect(self.quitGame)  # Connect clear action to the clear method