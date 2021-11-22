import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from win32api import GetSystemMetrics

# Global variables

# Number of fields in board
board_size = 9

# Store board information
board = []

# Colors definitions (RGB)
gray = "159, 159, 159"
white = "255, 255, 255"
blue = "133, 191, 244"
green = "132, 213, 136"

# User's total score
total_score = 0

# Variables used to move balls
chosen_ball = 0
chosen_destination = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)
        self.setWindowTitle("Marbles")
        self.setFixedSize(self.screen_width, self.screen_height)
        # self.showFullScreen()
        self.showMaximized()


class Button(QPushButton):
    def __init__(self, pos_x, pos_y, value, main_window):

        window_width = main_window.frameGeometry().width()
        window_height = main_window.frameGeometry().height()

        button_size = int(window_height / (board_size + 3))

        super().__init__(main_window)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value

        self.setFixedSize(button_size, button_size)
        # self.move(int(window_width / 3 + pos_x + button_size), int(button_size + pos_y + button_size))
        self.move(int(window_width / 4 + button_size * pos_x), int(button_size + button_size * pos_y))
        self.setText(str(self.value))
        self.setStyleSheet("background-color:rgb({})".format(gray))
        self.show()
        self.clicked.connect(lambda: self.change_value())

    def change_value(self):
        self.setStyleSheet("background-color:rgb({})".format(green))


# Loads initial board state
def init_board():
    # Define fields
    for i in range(board_size):
        board_row = []
        for j in range(board_size):
            board_row.append(Button(i, j, 0, window))
        board.append(board_row)


# Define menu items
def init_menu(main_window):
    # Score label
    label = QLabel()
    label.setText("Twój wynik:")
    label.setFixedSize(int(20), int(20))
    label.move(int(0), int(0))
    label.show()
    # window.addDockWidget(label)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()

    init_board()
    init_menu(window)

    window.show()
    app.exec()
