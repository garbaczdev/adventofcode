import numpy as np


def get_input() -> list:
    with open("input.txt", "r") as f:
        _in = [[int(tree) for tree in line] for line in f.read().split("\n") if line.split()]

    return _in


def is_visible(grid: np.array, x: int, y: int) -> bool:
    tested_tree = grid[y][x]
    rows = len(grid)
    cols = len(grid[0])

    if x == 0 or y == 0 or x == cols - 1 or y == rows - 1:
        return True

    return all(grid[y][xi] < tested_tree for xi in range(0, x)) \
        or all(grid[y][xi] < tested_tree for xi in range(x + 1, cols)) \
        or all(grid[yi][x] < tested_tree for yi in range(0, y)) \
        or all(grid[yi][x] < tested_tree for yi in range(y + 1, rows)) 


def get_score(grid: np.array, x: int, y: int) -> bool:
    tested_tree = grid[y][x]
    rows = len(grid)
    cols = len(grid[0])

    scores = [1, 1, 1, 1]

    for xi in range(x - 1, -1, -1):
        if grid[y][xi] >= tested_tree:
            break
        scores[0] += 1
    else:
        scores[0] -= 1
    

    for xi in range(x + 1, cols):
        if grid[y][xi] >= tested_tree:
            break
        scores[1] += 1
    else:
        scores[1] -= 1
    
    for yi in range(y - 1, -1, -1):
        if grid[yi][x] >= tested_tree:
            break
        scores[2] += 1
    else:
        scores[2] -= 1

    for yi in range(y + 1, rows):
        if grid[yi][x] >= tested_tree:
            break
        scores[3] += 1
    else:
        scores[3] -= 1

    product = 1
    for score in scores:
        product *= score

    return product

def part1(_in: list) -> None:
    grid = np.array(_in)
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if is_visible(grid, x, y):
                count += 1

    print("PART 1:", count)


def part2(_in: list) -> None:
    grid = np.array(_in)
    scores = list()
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            scores.append(get_score(grid, x, y))

    print("PART 2:", max(scores))


def main() -> None:
    _in = get_input()
    # part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
