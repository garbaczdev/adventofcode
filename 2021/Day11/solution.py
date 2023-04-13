import numpy as np


class FlashEmulator:
    def __init__(self, board: np.array) -> None:
        self.board = board
        self.currently_flashing = np.zeros(np.shape(board), dtype=np.bool)
        self.has_flashed = np.zeros(np.shape(board), dtype=np.bool)
        self.flash_count = 0

    def perform_step(self) -> None:
        self.increase_board()
        self.update_currently_flashing()

        while self.is_flashing():
            self.flash_board()
            self.update_currently_flashing()

        self.clear_flashed()

    def increase_board(self) -> None:
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                self.board[y][x] += 1

    def update_currently_flashing(self) -> None:
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] > 9:
                    self.currently_flashing[y][x] = 1
                else:
                    self.currently_flashing[y][x] = 0

    def is_flashing(self) -> None:
        return np.any(self.currently_flashing)

    def flash_board(self) -> None:
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.currently_flashing[y][x]:

                    self.flash(x, y)

                    self.has_flashed[y][x] = 1

    def flash(self, x: int, y: int) -> None:

        self.board[y][x] = 0
        
        for y_d in range(-1, 2):
            for x_d in range(-1, 2):

                if y_d == 0 and x_d == 0:
                    continue

                try:

                    y_cord = y + y_d
                    x_cord = x + x_d

                    if x_cord < 0 or y_cord < 0:
                        raise IndexError

                    if not self.has_flashed[y_cord][x_cord]:
                        self.board[y_cord][x_cord] += 1

                except IndexError:
                    pass

        self.flash_count += 1

    def clear_flashed(self) -> None:
        self.has_flashed.fill(0)

    def is_synchronizing(self) -> bool:
        return not np.any(self.board)



def task1(board: np.array) -> None:
    flash_emulator = FlashEmulator(board)

    for step in range(100):
        flash_emulator.perform_step()
    
    print(flash_emulator.flash_count)


def task2(board: np.array) -> None:
    flash_emulator = FlashEmulator(board)

    count = 0

    while not flash_emulator.is_synchronizing():
        flash_emulator.perform_step()
        count += 1

    print(count)


def main() -> None:
    with open("input.txt", "r") as f:
        board = np.array([[int(char) for char in line] for line in f.read().split("\n") if line.strip()])

    # task1(board)
    task2(board)


if __name__ == '__main__':
    main()
