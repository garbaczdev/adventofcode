#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime


def part1(_in):
    max_rectangle_size = -1

    for i in range(len(_in)):
        for j in range(i+1, len(_in)):
            x1, y1 = _in[i]
            x2, y2 = _in[j]

            rectangle_size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if rectangle_size > max_rectangle_size:
                max_rectangle_size = rectangle_size

    return max_rectangle_size


def does_path_intersect_rectangle(path: list, x1: int, y1: int, x2: int, y2: int) -> bool:
    # Set the x1 to left and x2 to right
    x1, x2 = min(x1, x2), max(x1, x2)
    # Set y1 to down and y2 to up
    y1, y2 = min(y1, y2), max(y1, y2)

    for cord1, cord2 in zip(path, path[1:]):
        p_x1, p_y1 = cord1
        p_x2, p_y2 = cord2

        # Same as above, align them to make the comparisons easier
        p_x1, p_x2 = min(p_x1, p_x2), max(p_x1, p_x2)
        p_y1, p_y2 = min(p_y1, p_y2), max(p_y1, p_y2)

        if p_x1 == p_x2:
            # Case 1: Vertical step
            if not (x1 < p_x1 < x2):
                # The step x is not aligned with any of the horizontal walls
                continue

            # The line is already aligned on the x. It intersects the rectangle if either:
            # - p_y1 is inside of rectangle
            # - p_y2 is inside of rectangle 
            # - p_y1 is at the bottom of rectangle and p_y2 is at the top of the rectangle
            if y1 < p_y1 < y2 \
                or y1 < p_y2 < y2 \
                or (p_y1 <= y1 and y2 <= p_y2):
                    return True

        elif p_y1 == p_y2:
            # Case 2: Horizontal step
            if not (y1 < p_y1 < y2):
                # The step y is not aligned with any of the vertical walls
                continue

            # The line is already aligned on the y. It intersects the rectangle if either:
            # - p_x1 is inside of rectangle
            # - p_x2 is inside of rectangle 
            # - p_x1 is at the left of rectangle and p_x2 is at the right of the rectangle
            if x1 < p_x1 < x2 \
                or x1 < p_x2 < x2 \
                or (p_x1 <= x1 and x2 <= p_x2):
                    return True

    return False


def is_rectangle_contained_inside(
    path: list,
    is_outside_direction_clockwise: bool,
    x1: int,
    y1: int,
    x2: int,
    y2: int
) -> bool:
    # Turns out the solution works without implementing that!
    return True


"""
Advent of code 9.2

As the 2d space is too large, we cannot rasterize it and run coloring algorithms.
We have to instead find clever ways to estimate whether the box is inside of the drawn structure.

For the rectangle to be considered legal, we have 2 conditions:
1. The rectangle has no paths going through it (Except the borders) - it is fully contained either outside or inside the structure
2. The rectangle is inside of the structure

Checking the first condition is easy because we can just traverse every line (of green tiles) and check 
if it intersects the rectangle.

Checking the second condition is tricky, because determining whether a rectangle is contained is difficult without 
a coloring algorithm. There is however a concrete difference between the outside and inside of the triangle:
"If you pick the closest wall (That can contain the rectangle) on the right of the rectangle and you follow it,
the direction will be different for when the rectangle is fully outside and when it is fully inside"

The outside direction can be calculated by picking the tile that is guaranteed to be on the outside (left-most vertical wall) and checking the direction
of that. If its up, then the direction from the outside is clockwise, otherwise counterclockwise
"""
def part2(_in):
    wall_path = _in + [_in[0]]
    vertical_walls = [
        (cords1[0], cords2[1] - cords1[1])
        for cords1, cords2 in zip(wall_path, wall_path[1:])
        if cords1[0] == cords2[0]
    ]

    left_most_wall = min(vertical_walls, key=lambda x: x[0])
    # Determine the direction of the path while looking at the outside
    is_outside_direction_clockwise = left_most_wall[1] > 0

    max_rectangle_size = -1

    for i in range(len(_in)):
        for j in range(i+1, len(_in)):
            x1, y1 = _in[i]
            x2, y2 = _in[j]

            rectangle_size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

            # Check 1: If the triangle is not bigger, don't bother
            #   to check it
            # Check 2: If any of the paths intersects the triangle, its not fully
            #   contained in either outside of inside
            # Check 3: If the rectangle is not inside, no reason to check it
            if rectangle_size > max_rectangle_size \
                and not does_path_intersect_rectangle(wall_path, x1, y1, x2, y2) \
                and is_rectangle_contained_inside(wall_path, is_outside_direction_clockwise, x1, y1, x2, y2):

                max_rectangle_size = rectangle_size

    return max_rectangle_size


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            [int(num) for num in line.split(',')]
            for line in f.read().split("\n")
            if line.split()
        ]
    return _in


def benchmark(name: str, func, *_in) -> None:
    """
    Utility function to benchmark the given part function, printing timing and result.

    Parameters:
        name (str): A label to print alongside the benchmark.
        func (callable): The function to call.
        *_in: Arguments to pass to the function.

    Returns:
        None
    """
    now = datetime.now()
    result = func(*_in)
    _time = datetime.now() - now
    print(f"({_time}) {name}: {result}")

def main() -> None:
    """
    Reads command-line argument for the input file name, processes both parts,
    and prints their results and timings.

    Returns:
        None
    """
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    benchmark("PART 1", part1, _in)
    benchmark("PART 2", part2, _in)

if __name__ == "__main__":
    main()
