from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class ScoreBoard(QDialog):
    def __init__(self, parent=None):
        # Initialize the ScoreBoard dialog with a parent (default is None)
        super().__init__(parent)
        self.setWindowTitle("Stats")  # Set the title of the dialog

        # Create QLabel instances for displaying turn and prisoners information
        self.current_turn_label = QLabel()
        self.white_prisoners_label = QLabel()
        self.black_prisoners_label = QLabel()

        # Create a QPushButton for closing the dialog
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.close)  # Connect the button click event to the close method

        # Create a QVBoxLayout for arranging widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.current_turn_label)  # Add turn label to the layout
        layout.addWidget(self.white_prisoners_label)  # Add white prisoners label to the layout
        layout.addWidget(self.black_prisoners_label)  # Add black prisoners label to the layout
        layout.addWidget(self.ok_button)  # Add OK button to the layout

        self.setLayout(layout)  # Set the layout for the ScoreBoard dialog

    def updateStats(self, current_player, white_prisoners, black_prisoners):
        # Update the turn and prisoners information based on the provided values
        self.current_turn_label.setText(f"Current's turn: {current_player}")  # Set the text for turn label
        self.white_prisoners_label.setText(f"White Prisoners: {white_prisoners}")  # Set the text for white prisoners label
        self.black_prisoners_label.setText(f"Black Prisoners: {black_prisoners}")  # Set the text for black prisoners label
