from typing import Tuple

import numpy as np


def signum(num: int) -> int:
    if num > 0:
        return 1
    elif num == 0:
        return 0
    else:
        return -1


class PathPredictor:
    def __init__(self, targets: list) -> None:
        self.square_start_x, self.square_end_x = sorted(targets[0])
        self.square_start_y, self.square_end_y = sorted(targets[1])

    def get_path(self, x_vel: int, y_vel: int) -> list:

        x = 0
        y = 0

        points = list()

        while y >= self.square_start_y or self.is_in_square(x, y):
            points.append((x, y))

            x += x_vel
            y += y_vel

            x_vel -= 1 if x > 0 else 0 if x == 0 else -1
            y_vel -= 1

        return points

    def is_in_square(self, x: int, y: int) -> bool:
        return self.square_start_x <= x <= self.square_end_x and self.square_start_y <= y <= self.square_end_y


    def find_highest_y_velocity(self) -> Tuple[int, int]:
        for y_vel in range(100):
            x_vel = 0
            path = self.get_path(x_vel, y_vel)

            while not self.has_path_overshot(path) or self.does_path_land_in_square(path):
                x_vel += 1
                path = self.get_path(x_vel, y_vel)

            

    def has_path_overshot(self, path: int) -> bool:
        return path[-1][0] > self.square_end_x

    
    def get_possible_x(self, x_vel: int) -> list:
        # x + x - 1 + x - 2 + ... =
        # nx - (1 + 2 + 3 + ... + n-1) = 

        # nx - (1 + n-1)(n-1)/2 =
        # nx - n(n-1)/2

        x_values = [0]

        x = None
        n = 1

        while x != 0:
            
            x = int(n*x_vel - n*(n-1)/2)
            x_values.append(x)

            n += 1

        return x_values

    def does_path_land_in_square(self, path: list) -> bool:
        return self.is_in_square(*path[-1])

    def print_path(self, path: list) -> None:

        x_min = min(path, key = lambda point: point[0])[0]
        y_min = min(path, key = lambda point: point[1])[1]
        
        x_max = max(path, key = lambda point: point[0])[0]
        y_max = max(path, key = lambda point: point[1])[1]

        height = y_max - y_min
        width = x_max - x_min

        board = np.zeros((height + 1, width + 1), dtype=np.int8)


        if signum(x_max) == signum(self.square_end_x) or signum(x_max) == signum(self.square_start_x):
            for y in range(self.square_start_y, self.square_end_y + 1):
                for x in range(self.square_start_x, self.square_end_x + 1):
                    try:
                        board[y_max - y][abs(x)] = 2
                    except IndexError:
                        pass
            

        # y_max, x_min -> 0, 0
        for x, y in path:
            board[y_max - y][abs(x)] = 1

        for row in board:
            line = ""
            for element in row:
                if element == 0:
                    line += "."

                elif element == 1:
                    line += "#"

                elif element == 2:
                    line += "T"

            print(line)


def task1(targets: list) -> None:
    predictor = PathPredictor(targets)
    path = predictor.get_path(20, 4)
    predictor.print_path(path)


def task2(targets: list) -> None:
    pass


def main() -> None:
    with open("sample_input.txt", "r") as f:
        targets = [[int(num) for num in segment.split("=")[1].split("..")] for segment in f.read()[13:].strip().split(", ")]

    task1(targets)
    task2(targets)


if __name__ == '__main__':
    main()
