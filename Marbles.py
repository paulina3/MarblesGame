import sys
from random import randint

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from win32api import GetSystemMetrics

# Number of fields in board
board_size = 9

# Store board information
board = []

# Balls information
balls_number = 5  # total number of used balls colors (5 - 9)
next_balls_number = 3  # increase each turn
next_colors = []  # random next balls colors
chosen_ball = None  # ball chosen to move
chosen_destination = None  # destination of chosen ball

# Colors definitions (images)
white = "images/white.png"     # blank
blue = "images/blue.png"       # number 0
green = "images/green.png"     # number 1
red = "images/red.png"         # number 2
yellow = "images/yellow.png"   # number 3
purple = "images/purple.png"   # number 4
colors_definition = [blue, green, red, yellow, purple, white]

# User's total score
total_score = 0


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
        self.move(int(window_width / 4 + button_size * pos_x), int(button_size + button_size * pos_y))
        self.setText(str(self.value))
        self.setStyleSheet("border-image : url({})".format(colors_definition[-1]))
        self.show()
        self.clicked.connect(lambda: self.move_balls())

    def change_value(self, color_number):
        self.value = color_number
        if color_number is not None:
            self.setStyleSheet("border-image : url({})".format(colors_definition[color_number]))
        else:
            self.setStyleSheet("border-image : url({})".format(colors_definition[-1]))
        self.setText(str(self.value))

    def move_balls(self):
        global chosen_ball
        global chosen_destination
        if self.value is not None:
            chosen_ball = board[self.pos_x][self.pos_y]
            print("Chosen ball position: {}, {}".format(self.pos_x, self.pos_y))
        elif chosen_ball is not None:
            if ball_can_be_moved(chosen_ball.pos_x, chosen_ball.pos_y, self.pos_x, self.pos_y):
                chosen_destination = board[self.pos_x][self.pos_y]
                print("Chosen destination position: {}, {}".format(self.pos_x, self.pos_y))
            # else do nothing
        # else do nothing

        if chosen_ball is not None and chosen_destination is not None:
            print("Moving color number {}".format(chosen_ball.value))
            chosen_destination.change_value(chosen_ball.value)
            chosen_ball.change_value(None)

            # Check for 4 or more in the row
            check_for_complete()

            # Add new balls to board
            next_rand_balls()


# Checks if ball can be moved to chosen destination
def ball_can_be_moved(pos_x, pos_y, dest_x, dest_y):
    can_be_moved = True
    return can_be_moved


# Returns 3 random ball numbers and its positions
# returns: [[pos_x, pos_y, color],[], ...]
def next_rand_colors():
    global next_colors
    next_colors = []

    # Random colors of next balls
    for i in range(next_balls_number):
        next_colors.append(randint(0, balls_number - 1))


# Returns 3 random ball numbers and its positions
# returns: [[pos_x, pos_y, color],[], ...]
def next_rand_balls():
    print("Random next balls")
    global chosen_ball
    global chosen_destination

    # Reset saved positions
    chosen_destination = None
    chosen_ball = None
    next_balls = []

    # Random balls position
    for i in range(next_balls_number):
        pos_x = randint(0, board_size - 1)
        pos_y = randint(0, board_size - 1)
        # If field not empty, try next one
        while board[pos_x][pos_y].value is not None:
            pos_x = (pos_x + 1) % board_size
            while board[pos_x][pos_y].value is not None:
                pos_y = (pos_y + 1) % board_size

        next_balls.append([pos_x, pos_y, next_colors[i]])

    # Update board
    for i in range(next_balls_number):
        pos_x = next_balls[i][0]
        pos_y = next_balls[i][1]
        color = next_balls[i][2]
        board[pos_x][pos_y].change_value(color)

    # Random colors of next balls
    next_rand_colors()
    return next_balls


# Loads initial board state
def init_board():
    # Define fields
    for i in range(board_size):
        board_row = []
        for j in range(board_size):
            board_row.append(Button(i, j, None, window))
        board.append(board_row)
    next_rand_colors()
    init_balls = next_rand_balls()
    for i in range(next_balls_number):
        pos_x = init_balls[i][0]
        pos_y = init_balls[i][1]
        color = init_balls[i][2]
        board[pos_x][pos_y].change_value(color)


# Define menu items
def init_menu(main_window):
    # Score label
    label = QLabel()
    label.setText("Twój wynik:")
    label.setFixedSize(int(20), int(20))
    label.move(int(0), int(0))
    label.show()
    # window.addDockWidget(label)


# Checks if balls can be removed
def check_for_complete():
    return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    init_board()
    init_menu(window)

    window.show()
    app.exec()
