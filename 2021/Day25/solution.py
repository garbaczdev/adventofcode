import numpy as np


def calculate_step(board: np.array) -> np.array:
    new_board = np.zeros(board.shape, dtype=np.int8)

    board_height = board.shape[0]
    board_width = board.shape[1]

    for y, row in enumerate(board):
        for x, element in enumerate(row):
            if element == 1:
                
                new_x = x + 1

                if new_x == board_width:
                    new_x = 0

                if board[y][new_x] == 0:
                    new_board[y][new_x] = 1
                else:
                    new_board[y][x] = 1

    for y, row in enumerate(board):
        for x, element in enumerate(row):
            if element == 2:
                
                new_y = y + 1

                if new_y == board_height:
                    new_y = 0

                if new_board[new_y][x] == 0 and board[new_y][x] != 2:
                    new_board[new_y][x] = 2
                else:
                    new_board[y][x] = 2

    return new_board
                
                




def task1(board: np.array) -> None:
    last_board = np.zeros(board.shape)
    
    step = 0

    while not np.all(board == last_board):

        last_board = board
        board = calculate_step(board)

        step += 1

    print(step)

def task2(board: np.array) -> None:
    pass


def main() -> None:
    with open("input.txt", "r") as f:
        # "." -> 0
        # ">" -> 1
        # "v" -> 2
        board = np.array([[1 if char == ">" else 2 if char == "v" else 0 for char in line] for line in f.read().split("\n") if line.strip()], dtype=np.int8)

    task1(board)
    task2(board)


if __name__ == '__main__':
    main()
