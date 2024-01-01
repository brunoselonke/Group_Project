from PyQt6.QtGui import QAction  # Importing QAction class from PyQt6.QtGui module
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog, QVBoxLayout, QLabel, QPushButton  # Importing necessary classes from PyQt6.QtWidgets module
from PyQt6.QtCore import Qt  # Importing Qt class from PyQt6.QtCore module
from board import Board  # Importing Board class from the board module
from score_board import ScoreBoard  # Importing ScoreBoard class from the score_board module

class Go(QMainWindow):
    def __init__(self):
        super().__init__()  # Calling the constructor of the parent class (QMainWindow)
        self.initUI()  # Calling the initUI method to initialize the user interface

    def getBoard(self):
        return self.board  # Getter method to retrieve the current game board

    def initUI(self):
        '''Initializes the application UI'''
        self.setFixedSize(700, 700)  # Set a fixed size for the window
        self.board = Board(self)  # Create an instance of the Board class
        self.setCentralWidget(self.board)  # Set the central widget of the QMainWindow to the game board

        self.center()  # Call the center method to center the window
        self.setWindowTitle('Go')  # Set the window title to 'Go'
        self.show()  # Display the window

    def center(self):
        '''Centers the window on the screen'''
        gr = self.frameGeometry()  # Get the geometry of the window
        screen = self.screen().availableGeometry().center()  # Get the center of the screen

        gr.moveCenter(screen)  # Move the window to the center of the screen
        self.move(gr.topLeft())  # Set the top-left corner of the window

        # Set up menus
        mainMenu = self.menuBar()  # Get the menu bar of the main window
        mainMenu.setNativeMenuBar(False)  # Set native menu bar to False
        gameMenu = mainMenu.addMenu("Game Menu")  # Add 'Game Menu' to the menu bar
        helpMenu = mainMenu.addMenu(" Help")  # Add 'Help' to the menu bar

        # Stats action setup
        statsAction = QAction("Stats  ", self)  # Create an action for displaying stats
        statsAction.setShortcut("Ctrl+S")  # Set a shortcut for the action
        gameMenu.addAction(statsAction)  # Add the action to the 'Game Menu'
        statsAction.triggered.connect(self.board.openScoreBoard)  # Connect action to openScoreBoard method

        # Quit Game action setup
        quitGameAction = QAction("Quit Game  ", self)  # Create an action for quitting the game
        quitGameAction.setShortcut("Ctrl+Q")  # Set a shortcut for the action
        gameMenu.addAction(quitGameAction)  # Add the action to the 'Game Menu'
        quitGameAction.triggered.connect(self.quitGame)  # Connect action to quitGame method

        # Game Instructions action setup
        gameInstructions = QAction("Instructions  ", self)  # Create an action for displaying game instructions
        gameInstructions.setShortcut("Ctrl+I")  # Set a shortcut for the action
        helpMenu.addAction(gameInstructions)  # Add the action to 'Help'
        gameInstructions.triggered.connect(self.openInstructionsDialog)  # Connect action to openInstructionsDialog method

    def quitGame(self):
        # Prompt to confirm if the player wants to quit
        user_response = QMessageBox.question(self, "Confirm quit", "Are you sure you want to quit?")

        # If yes, execute the quit
        if user_response == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def openInstructionsDialog(self):
        instructions_dialog = QDialog()  # Create a dialog for displaying game instructions
        instructions_dialog.setWindowTitle("Go Game Instructions")  # Set the dialog title

        layout = QVBoxLayout()  # Create a vertical layout for the dialog

        instructions_text = (
            "Instructions:<br><br>"
            "Go is a two-player board game that originated in China. The game is played on a grid where players take turns placing their stones.<br><br>"
            "The goal is to control more territory than your opponent by surrounding empty areas and capturing opponent stones.<br><br>"
            "Stones are captured by surrounding them entirely. However, suicide moves (which result in an immediate loss of liberties) are not allowed.<br><br>"
            "The player with the most controlled territory at the end wins."
        )

        instructions_label = QLabel(instructions_text)  # Create a label with the instructions text
        instructions_label.setWordWrap(True)  # Set word wrap for the label
        layout.addWidget(instructions_label)  # Add the label to the layout

        close_button = QPushButton("Close")  # Create a 'Close' button
        close_button.clicked.connect(instructions_dialog.close)  # Connect button to close the dialog
        layout.addWidget(close_button)  # Add the button to the layout

        instructions_dialog.setLayout(layout)  # Set the layout for the dialog
        instructions_dialog.exec()  # Execute the dialog
