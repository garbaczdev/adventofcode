from math import inf
from typing import Tuple

import numpy as np


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class PathFinder:
    def __init__(self, board: np.array) -> None:
        self.board: np.array = board

    def calculate_tables(self, start_x: int, start_y: int, end_x: int, end_y: int) -> Tuple[np.array, np.array]:
        costs = np.ndarray(self.board.shape)
        costs.fill(inf)
        costs[start_y][start_x] = 0
        
        _from = np.ndarray(self.board.shape, dtype=object)
        
        sorted_queue = [(start_x, start_y, 0)]

        while sorted_queue:

            current_x, current_y, current_cost = sorted_queue.pop(0)
            
            if current_cost > costs[current_y][current_x]:
                continue

            if current_x == end_x and current_y == end_y:
                break
            
            for x_d, y_d in DIRECTIONS:
                try:
                    new_x = x_d + current_x
                    new_y = y_d + current_y

                    if new_x < 0 or new_y < 0:
                        raise IndexError

                    new_cost = current_cost + self.board[new_y][new_x]
                    
                    if new_cost < costs[new_y][new_x]:

                        self.insert_into_sorted_queue(sorted_queue, (new_x, new_y, new_cost))
                        _from[new_y][new_x] = (current_x, current_y)
                        costs[new_y][new_x] = new_cost
                    
                except IndexError:
                    pass

        return costs, _from
        


    @staticmethod
    def insert_into_sorted_queue(sorted_queue: list, element_to_insert: tuple) -> None:
        
        if len(sorted_queue) == 0:
            sorted_queue.append(element_to_insert)
        else:
            index = 0
            while index < len(sorted_queue) and element_to_insert[2] > sorted_queue[index][2]:
                index += 1

            sorted_queue.insert(index, element_to_insert)
        
        


def task1(board: np.array) -> None:
    path_finder = PathFinder(board)

    end_x = len(board[0]) - 1
    end_y = len(board) - 1

    cost_table = path_finder.calculate_tables(0, 0, end_x, end_y)[0]
    print(cost_table[end_y][end_x])


def wrap_number(number: int, amount: int) -> int:
    new_number = (number - 1 + amount) % 9 + 1
    return new_number if new_number != 10 else 0


def calculate_extended_board(board: np.array) -> np.array:

    board_width = board.shape[0]
    board_height = board.shape[1]

    new_board = np.zeros((board_width*5, board_height*5))
    
    for y_seg_index in range(5):
        for x_seg_index in range(5):

            for y_d in range(board_height):
                for x_d in range(board_height):

                    y = y_seg_index*board_height + y_d
                    x = x_seg_index*board_width + x_d

                    new_board[y][x] = wrap_number(board[y_d][x_d], y_seg_index + x_seg_index)

    return new_board


def task2(board: np.array) -> None:

    board = calculate_extended_board(board)

    path_finder = PathFinder(board)

    end_x = len(board[0]) - 1
    end_y = len(board) - 1

    cost_table = path_finder.calculate_tables(0, 0, end_x, end_y)[0]
    print(cost_table[end_y][end_x])


def main() -> None:
    with open("input.txt", "r") as f:
        board = np.array([[int(char) for char in line] for line in f.read().split("\n") if line.strip()])

    # task1(board)
    task2(board)


if __name__ == '__main__':
    main()
