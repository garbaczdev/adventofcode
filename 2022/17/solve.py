#!/usr/bin/env python3
from sys import argv
from datetime import datetime

import numpy as np


class Point2D:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y

    def __sub__(self, point):
        return Point2D(self.x - point.x, self.y - point.y)

    def __add__(self, point):
        return Point2D(self.x + point.x, self.y + point.y)
        
    def __hash__(self):
        return hash((self.x, self.y))

    def dist_from(self, point) -> int:
        diff = point - self
        return abs(diff.x) + abs(diff.y)


class Shape:
    def __init__(self, points: list, base_point: Point2D = Point2D(0, 0)):
        self._points = points
        self.height = self.get_height()
        self.base_point = base_point
    
    def copy(self):
        return Shape(self._points, self.base_point)

    def get_points(self) -> list:
        return [point + self.base_point for point in self._points]

    def get_height(self) -> int:
        return max(map(lambda point: point.y, self._points)) - min(map(lambda point: point.y, self._points)) + 1


ROCK_SHAPES = [
    [
        Point2D(0, 0),
        Point2D(1, 0),
        Point2D(2, 0),
        Point2D(3, 0),
    ],
    [
        Point2D(1, 0),
        Point2D(0, 1),
        Point2D(1, 1),
        Point2D(1, 2),
        Point2D(2, 1),
    ],
    [
        Point2D(0, 0),
        Point2D(1, 0),
        Point2D(2, 0),
        Point2D(2, 1),
        Point2D(2, 2),
    ],
    [
        Point2D(0, 0),
        Point2D(0, 1),
        Point2D(0, 2),
        Point2D(0, 3),
    ],
    [
        Point2D(0, 0),
        Point2D(0, 1),
        Point2D(1, 0),
        Point2D(1, 1),
    ]
]


class Board:

    DEFAULT_HEIGHT = 100000
    REALLOC_THRESHOLD = 1000

    def __init__(self, width: int):
        self.width = width
        self.height = self.DEFAULT_HEIGHT
        self._board = np.zeros((self.height + 1, self.width), dtype=bool)

        self._current_rock = None
        self._is_rock_falling = False

    def run_simulation(self, instructions: str, rocks_number) -> int:
        instruction_index = 0

        for rock_index in range(rocks_number):
            self.spawn_rock(rock_index % 5)

            while self._is_rock_falling:
                self.move_rock(instructions[instruction_index])
                instruction_index += 1
                instruction_index %= len(instructions)

            for point in self._current_rock.get_points():
                self._board[point.y][point.x] = 1


            self._is_rock_falling = False


    def print(self, start_y: int = 0, end_y: int = None):

        
        if self._is_rock_falling:
            rock_points = self._current_rock.get_points()
        else:
            rock_points = []

        if end_y is None: 
            if self._is_rock_falling:
                end_y = max(point.y for point in rock_points) + 1
            else:
                end_y = self.max_height()
        
        for y in range(end_y, start_y - 1, -1):
            line = []
            for x in range(self.width):
                point = Point2D(x, y)
                line.append(
                    "#" if self._board[point.y][point.x] 
                    else "@" if point in rock_points 
                    else "."
                )
                
            print("%-6d " % y + "|" + "".join(line) + "|")

        if start_y == 0:
            print(" "*len(str("%-6d " % y)) + "+" + "".join("-" for _ in range(self.width)) + "+")
        else:
            print()
        print()
        

    def optimize(self) -> None:
        rock_points = self._current_rock.get_points()
        max_rock_y = max(point.y for point in rock_points)
        if self.height - max_rock_y <= self.REALLOC_THRESHOLD:
            for y in range(max_rock_y, -1, -1):
                row = self._board[y]
                if not all(row):
                    new_board = np.zeros((self.height, self.width), dtype=bool)
                    new_board[0:self.height-y, :] = self._board[y:self.height, :]
                    self._board = new_board
                    return
                    

    def move_rock(self, instruction: str):

        if instruction == ">":
            diff = Point2D(1, 0)
        else:
            diff = Point2D(-1, 0)

        if self.can_rock_move(diff):
            self.move_rock_cord(diff)
    
        if self.can_rock_move(Point2D(0, -1)):
            self.move_rock_cord(Point2D(0, -1))
        else:
            self._is_rock_falling = False

    
    def spawn_rock(self, index: int) -> None:
        self._current_rock = Shape(ROCK_SHAPES[index])
        self._current_rock.base_point = Point2D(2, self.max_height() + 3)
        self._is_rock_falling = True
    
    def max_height(self) -> int:
        for y, row in enumerate(self._board):
            if any(row):
                continue
            return y

    def move_rock_cord(self, diff: Point2D):
        self._current_rock.base_point += diff

    def can_rock_move(self, diff: Point2D):
        new_rock = self._current_rock.copy()
        new_rock.base_point += diff
        new_points = new_rock.get_points()

        return all(
            (point.x >= 0 and point.x < self.width and point.y >= 0)
            and not self._board[point.y][point.x] 
            for point in new_points
        )


def get_input(filename: str) -> list:
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()][0]

    return _in


def part1(_in: list):
    board = Board(7)
    board.run_simulation(_in, 2022)
    board.print()
    print(board.max_height())


def part2(_in: list):
    board = Board(7)
    # board.run_simulation(_in, 1000000000000)
    print(board.max_height())


def benchmark(name: str, func, *_in) -> None:
    now = datetime.now()
    result = func(*_in)
    _time = datetime.now() - now
    print(f"({_time}) {name}: {result}")


def main() -> None:
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    benchmark("PART 1", part1, _in)
    benchmark("PART 2", part2, _in)


if __name__ == "__main__":
    main()
