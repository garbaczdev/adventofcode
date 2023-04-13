#!/usr/bin/env python3
from sys import argv

from copy import deepcopy

import numpy as np


class SandBoard:

    SAND_DROP_POINT = (500, 0)
    CHAR_DECODING = {
        0: ".",
        1: "#",
        2: "o"
    }

    def __init__(self, lines: list):
        self.unparsed_lines = lines
        x_max, y_max = self.find_max(lines)
        self.content = np.zeros((y_max+1, x_max+1), dtype=np.uint8)
        self.draw_content(self.content, self.unparsed_lines)

    def __str__(self) -> str:
    
        content = self.content[:, 495:504]
        height, width = content.shape
        lines = list()
        for y in range(height):
            line = list()
            for x in range(width):
                char = self.CHAR_DECODING[content[y][x]]
                line.append(char)
            lines.append("".join(line))

        return "\n".join(lines)
                

    def drop_sand(self) -> bool:
        """
        Drops a piece of sand onto the board.
        Retuns True if it stopped.
        Returns False if it fell into the void.
        """

        sand_cord = self.SAND_DROP_POINT

        moved = True
        while moved:
            new_sand_cord = self.move(*sand_cord)

            if new_sand_cord == sand_cord:
                moved = False

            sand_cord = new_sand_cord


        x, y = sand_cord

        if self.is_out_of_bounds(x, y):
            return False

        self.content[y][x] = 2
        return True


    def move(self, x: int, y: int) -> tuple[int,int]:
        height, width = self.content.shape 
        
        if self.is_out_of_bounds(x, y):
            return (x, y)

        if not self.is_occupied(x, y + 1):
            return (x, y + 1)
        if not self.is_occupied(x - 1, y + 1):
            return (x - 1, y + 1)
        if not self.is_occupied(x + 1, y + 1):
            return (x + 1, y + 1)

        return (x, y)

    def is_occupied(self, x: int, y: int) -> bool:
        if self.is_out_of_bounds(x, y):
            return False

        return self.content[y][x] != 0

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        height, width = self.content.shape 
        return x < 0 or x >= width or y < 0 or y >= height


    @staticmethod
    def draw_content(content: np.array, unparsed_lines: list) -> None:
        lines = [[tuple(map(int, point.split(","))) for point in line.split("->")] for line in unparsed_lines]

        for line in lines:
            for p1, p2 in zip(line, line[1:]):
                p1x, p1y = p1
                p2x, p2y = p2

                if p1x == p2x:
                    y_diff = p2y - p1y
                    _range = range(p1y, p2y + 1) if y_diff > 0 else range(p1y, p2y - 1, -1)
                    for y in _range:
                        content[y][p1x] = 1
                elif p1y == p2y:
                    x_diff = p2x - p1x
                    _range = range(p1x, p2x + 1) if x_diff > 0 else range(p1x, p2x - 1, -1)
                    for x in _range:
                        content[p1y][x] = 1

    @staticmethod
    def find_max(lines: list) -> tuple[int, int]:
        x_cords = [int(point.split(",")[0]) for line in lines for point in line.split("->")]
        y_cords = [int(point.split(",")[1]) for line in lines for point in line.split("->")]
        return (max(x_cords), max(y_cords))


class AdvancedSandBoard(SandBoard):

    def __init__(self, lines: list):
        x_max, y_max = self.find_max(lines)
        lines.append(f"0,{y_max} -> {x_max},{y_max}")
        super().__init__(lines)

    def find_max(self,lines: list) -> tuple[int, int]:
        x_max, y_max = super().find_max(lines)
        return x_max*2, y_max+2


def get_input(filename: str) -> list:
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in: list) -> None:
    _in = deepcopy(_in)
    board = SandBoard(_in)
    i = 0
    while board.drop_sand():
        i += 1
        # print(board)
        # print(i)

    print(board)
    print("PART 1:", i)

def part2(_in: list) -> None:
    _in = deepcopy(_in)
    board = AdvancedSandBoard(_in)
    i = 0
    while board.content[0][500] != 2:
        board.drop_sand()
        i += 1
    print("PART 2:", i)


def main() -> None:
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
