#!/usr/bin/env python3
from sys import argv

import numpy as np


class Board:

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, _input: str):
        self._original_board = _input
        self._lines = [list(line) for line in _input.split("\n") if line.split()]

        self.board = np.array(self._lines)

        self.start_cord = self.find_letter_cord('S')
        self.end_cord = self.find_letter_cord('E')

    
    def find_path(self) -> tuple[int, int]:
        
        queue = [self.start_cord]

        visited = np.zeros(self.board.shape, dtype=np.uint8)
        start_x, start_y = self.start_cord
        visited[start_y][start_x] = 1

        _from = dict()

        while queue:

            current = queue.pop(0)

            x, y = current
            current_value = self.get_value(x, y)

            if current == self.end_cord:
                break

            for x_diff, y_diff in self.DIRECTIONS:
                x_new = x + x_diff
                y_new = y + y_diff
                if not self.is_visited(visited, x_new, y_new):
                    new_value = self.get_value(x_new, y_new)
                    if new_value - current_value > 1:
                        continue

                    visited[y_new][x_new] = 1
                    queue.append((x_new, y_new))
                    _from[(x_new, y_new)] = current            
        else:
            return []
        
        path = list()
        while current != self.start_cord:
            path.append(current)
            current = _from[current]

        path.reverse()

        return path
        



    def find_letter_cord(self, letter: str) -> tuple[int, int]:
        height, width = self.board.shape
        for y in  range(height):
            for x in range(width):
                if self.board[y][x] == letter:
                    return x, y

        return -1, -1

    def get_value(self, x, y) -> int:
        return self.get_letter_value(self.board[y][x])

    def can_go(self, visited: np.array, x: int, y: int) -> bool:
        if is_visited(visited, x, y):
            return False

    def get_starting_points(self) -> list:

        starting_points = list()

        height, width = self.board.shape

        for y in  range(height):
            for x in range(width):
                if self.board[y][x] == "a" and self.has_surroundings(x, y):
                    starting_points.append((x, y))

        return starting_points


    def has_surroundings(self, x: int, y: int) -> bool:

        height, width = self.board.shape

        for x_diff, y_diff in self.DIRECTIONS:
            x_new = x + x_diff
            y_new = y + y_diff
            if x_new < 0 or y_new < 0 or x_new >= width or y_new >= height:
                continue

            if self.board[y_new][x_new] != 'a':
                return True

        return False

        

    @staticmethod
    def get_letter_value(letter: str) -> int:

        if letter == 'S':
            return 1
        if letter == 'E':
            return 26

        return ord(letter) - 96


    @staticmethod
    def is_visited(visited: np.array, x: int, y: int) -> bool:
        height, width = visited.shape

        if x < 0 or x >= width or y < 0 or y >= height:
            return True

    
        return visited[y][x]
        


def get_input(filename: str) -> str:
    with open(filename, "r") as f:
        _in = f.read()

    return _in


def part1(_in: str) -> None:
    board = Board(_in)

    path = board.find_path()
    print("PART 1:", len(path))


def part2(_in: str) -> None:
    board = Board(_in)
    starting_points = board.get_starting_points()
    starting_points.append(board.start_cord)

    print(f"EXAMINING {len(starting_points)} PATHS")

    path_lengths = list()
    for i, starting_point in enumerate(starting_points):
        board.start_cord = starting_point
        path = board.find_path()
        if path:
            path_lengths.append(len(path))
        print("EXAMINED:", i)

    min_path = min(path_lengths)
    print("PART 2:", min_path)


def main() -> None:
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
