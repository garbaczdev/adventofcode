
from typing import Tuple
import numpy as np


OPENINGS = ["(", "[", "{", "<"]
CLOSINGS = [")", "]", "}", ">"]
EXPECTED_CLOSINGS = {opening: closing for opening, closing in zip(OPENINGS, CLOSINGS)}
TASK1_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
TASK2_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}




def is_corrupted(line: str) -> Tuple[bool, str]:

    line_mask = np.zeros(len(line))
    error = ""
    
    def dfs(current_index: int = 0) -> bool:

        nonlocal error

        line_mask[current_index] = 1

        current_opening = line[current_index]
        expected_closing = EXPECTED_CLOSINGS[current_opening]

        while current_index < len(line) - 1:

            if not line_mask[current_index + 1]:

                if line[current_index + 1] in OPENINGS:
                    if dfs(current_index + 1):
                        return True

                elif line[current_index + 1] == expected_closing:
                    line_mask[current_index + 1] = 1
                    return False

                else:
                    error = line[current_index + 1]
                    return True

            current_index += 1

        return False

    return dfs(), error

def calculate_finish(line: str) -> str:

    line = "<" + line

    line_mask = np.zeros(len(line))
    finish = ""
    
    def dfs(current_index: int = 0) -> None:

        nonlocal finish

        line_mask[current_index] = 1

        current_opening = line[current_index]
        expected_closing = EXPECTED_CLOSINGS[current_opening]

        while current_index < len(line) - 1:

            if not line_mask[current_index + 1]:

                if line[current_index + 1] in OPENINGS:
                    dfs(current_index + 1)

                elif line[current_index + 1] == expected_closing:
                    line_mask[current_index + 1] = 1
                    return

            current_index += 1

        finish += expected_closing

    dfs()

    return finish[:-1]

def calculate_score(finish: str) -> int:
    score = 0

    for char in finish:
        score *= 5
        score += TASK2_SCORES[char]

    return score

def task1(lines: list) -> None:
    corrupted_chars = list()

    for line in lines:
        corrupted, corrupted_char = is_corrupted(line)
        if corrupted:
            corrupted_chars.append(corrupted_char)

    print(sum(TASK1_SCORES[corrupted_char] for corrupted_char in corrupted_chars))

def task2(lines: list) -> None:
    
    unfinished_lines = [line for line in lines if not is_corrupted(line)[0]]

    finishes = [calculate_finish(unfinished_line) for unfinished_line in unfinished_lines]
    scores = [calculate_score(finish) for finish in finishes]
    scores.sort()
    print(scores[int(len(scores)/2)])

def main() -> None:
    with open("input.txt", "r") as f:
        lines = [line for line in f.read().split("\n") if line.strip()]

    # task1(lines)
    task2(lines)


if __name__ == '__main__':
    main()
