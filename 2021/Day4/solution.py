import numpy as np

class BingoBoard:
    def __init__(self, lines: list):
        self.mask = np.zeros((5, 5), dtype=bool)
        self.content = np.array(lines, dtype=np.int16)

    def mark(self, number_to_mark: int) -> None:
        for y in range(len(self.content)):
            for x in range(len(self.content[y])):
                if self.content[y][x] == number_to_mark:
                    self.mask[y][x] = 1

    def has_won(self) -> bool:

        # Check each row
        for y in range(len(self.content)):
            if np.all(self.mask[y, :]):
                return True

        # Check each column
        for x in range(len(self.content[0])):
            if np.all(self.mask[:, x]):
                return True

        return False

    def get_unmarked_sum(self) -> int:

        _sum = 0

        for y in range(len(self.content)):
            for x in range(len(self.content[y])):
                if self.mask[y][x] == 0:
                    _sum += self.content[y][x]

        return _sum


def task1(boards: list, bingo_numbers: int) -> None:
    for bingo_number in bingo_numbers:
        for board in boards:
            board.mark(bingo_number)
            if board.has_won():
                print(board.get_unmarked_sum()*bingo_number)
                return

def task2(boards: list, bingo_numbers: int) -> None:

    board_set = set(boards)

    for bingo_number in bingo_numbers:
        for board in list(board_set):

            board.mark(bingo_number)

            if board.has_won():

                if len(board_set) == 1:
                    print(board.get_unmarked_sum()*bingo_number)
                    return
                
                else:
                    board_set.remove(board)



with open("input.txt", "r") as f:
    segments = [segment for segment in f.read().split("\n\n") if segment.strip()]

    bingo_numbers = [int(num) for num in segments[0].split(",")]

    boards = [BingoBoard([[int(num) for num in line.split()] for line in segment.split("\n")]) for segment in segments[1:]]


# task1(boards, bingo_numbers)
task2(boards, bingo_numbers)