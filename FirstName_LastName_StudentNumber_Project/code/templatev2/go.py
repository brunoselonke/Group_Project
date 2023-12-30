from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        return self.board

    def initUI(self):
        '''initiates application UI'''
        self.setFixedSize(700, 700)  # Set a fixed size for the window
        self.board = Board(self)
        self.setCentralWidget(self.board)

        self.center()
        self.setWindowTitle('Go')
        self.show()

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
        statsAction = QAction("Stats  ", self)
        statsAction.setShortcut("Ctrl+S")
        gameMenu.addAction(statsAction)
        statsAction.triggered.connect(self.board.openScoreBoard)  # Connect clear action to the clear method

        # Quit Game action setup
        quitGameAction = QAction("Quit Game  ", self)
        quitGameAction.setShortcut("Ctrl+Q")
        gameMenu.addAction(quitGameAction)  # Quit Game Action
        quitGameAction.triggered.connect(self.quitGame)  # Connect clear action to the clear method

        # Game Instructions action setup
        gameInstructions = QAction("Instructions  ", self)
        gameInstructions.setShortcut("Ctrl+I")
        helpMenu.addAction(gameInstructions)  # Game Instructions
        gameInstructions.triggered.connect(self.openInstructionsDialog)  # Connect clear action to the clear method

    def quitGame(self):
        # Prompt to confirm if the player wants to skip
        user_response = QMessageBox.question(self, "Confirm quit", "Are you sure you want to quit?")

        # If yes, execute the skip_turn
        if user_response == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def openInstructionsDialog(self):
        instructions_dialog = QDialog()
        instructions_dialog.setWindowTitle("Go Game Instructions")

        layout = QVBoxLayout()

        instructions_text = (
            "Instructions:<br><br>"
            "Go is a two-player board game that originated in China. The game is played on a grid where players take turns placing their stones.<br><br>"
            "The goal is to control more territory than your opponent by surrounding empty areas and capturing opponent stones.<br><br>"
            "Stones are captured by surrounding them entirely. However, suicide moves (which result in immediate loss of liberties) are not allowed.<br><br>"
            "The player with the most controlled territory at the end wins."
        )

        instructions_label = QLabel(instructions_text)
        instructions_label.setWordWrap(True)
        layout.addWidget(instructions_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(instructions_dialog.close)
        layout.addWidget(close_button)

        instructions_dialog.setLayout(layout)
        instructions_dialog.exec()
