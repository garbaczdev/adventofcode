import numpy as np

def count_ones(board: np.array) -> int:
    count = 0

    for row in board:
        for element in row:
            if element:
                count += 1
    
    return count

def calculate_fold(points: set, instruction: tuple) -> None:
    new_points = set()

    if instruction[0] == "x":

        for point in points:

            if point[0] < instruction[1]:
                new_points.add(point)

            elif point[0] > instruction[1]:
                new_points.add((2*instruction[1] - point[0], point[1]))
        # side1, side2 = board[:, :instruction[1]], board[:, instruction[1] + 1:]
        # board = np.logical_or(side1, np.fliplr(side2))

    if instruction[0] == "y":

        for point in points:

            if point[1] < instruction[1]:
                new_points.add(point)

            elif point[1] > instruction[1]:
                new_points.add((point[0], 2*instruction[1] - point[1]))
        # side1, side2 = board[:instruction[1], :], board[instruction[1] + 1:, :]
        # board = np.logical_or(side1, np.flipud(side2))

    return new_points

def points_to_board(points: set) -> np.array:
    max_x = max(points, key=lambda cords: cords[0])[0]
    max_y = max(points, key=lambda cords: cords[1])[1]
    
    board = np.zeros((max_y + 1, max_x + 1), dtype=np.bool)
    for x, y in points:
        board[y][x] = 1

    return board

def board_to_text(board: np.array) -> str:
    result = ""

    for row in board:
        for element in row:
            result += "#" if element else "."

        result += "\n"

    return result


def task1(points: set, instructions: list) -> None:
    
    instruction = instructions[0]

    points = calculate_fold(points, instruction)

    board = points_to_board(points)

    print(count_ones(board))
    

def task2(points: set, instructions: list) -> None:

    for instruction in instructions:
        points = calculate_fold(points, instruction)

    board = points_to_board(points)

    print(board_to_text(board))


def main() -> None:
    with open("input.txt", "r") as f:
        segments = [segment for segment in f.read().split("\n\n") if segment.strip()]

        points = set(tuple([int(cord) for cord in line.split(",")]) for line in segments[0].split("\n"))
        # max_x = max(points, key=lambda cords: cords[0])[0]
        # max_y = max(points, key=lambda cords: cords[1])[1]
        
        # board = np.zeros((max_y + 1, max_x + 1), dtype=np.bool)
        # for x, y in points:
        #     board[y][x] = 1

        instructions = [(instruction.split()[-1].split("=")[0], int(instruction.split()[-1].split("=")[1])) for instruction in segments[1].split("\n")]

    # task1(points, instructions)
    task2(points, instructions)

if __name__ == '__main__':
    main()
