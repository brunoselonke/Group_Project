from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class ScoreBoard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stats")

        self.current_turn_label = QLabel()
        self.white_prisoners_label = QLabel()
        self.black_prisoners_label = QLabel()

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.current_turn_label)
        layout.addWidget(self.white_prisoners_label)
        layout.addWidget(self.black_prisoners_label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def updateStats(self, current_player, white_prisoners, black_prisoners):
        self.current_turn_label.setText(f"Current's turn: {current_player}")
        self.white_prisoners_label.setText(f"White Prisoners: {white_prisoners}")
        self.black_prisoners_label.setText(f"Black Prisoners: {black_prisoners}")