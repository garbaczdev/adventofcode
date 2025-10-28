#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

# =======================================================
# Advent of Code 2016, Day 2 solution
#
# This script provides solutions for both Part 1 and Part 2 
# of Advent of Code 2016 Day 2, the "Bathroom Security" challenge. 
#
# The code processes input files detailing sequences of movement 
# instructions, simulates movement across two different keypads, 
# and generates the resulting bathroom code combinations.
#
# Input: Text file, each line consists of a sequence of 'U', 'D', 'L', 'R'
# Output: Sequence of keypad values (the bathroom code) for both keypad layouts
#
# Assumptions:
#    - The input file exists and is readable
#    - Each line consists of valid movement instructions only
#    - For Part 2, the keypad layout matches the sample given
#    - No input sanitation is done on the instruction strings
#    - Input lines are not empty (empty lines are ignored)
# =======================================================

from sys import argv
from datetime import datetime

# Keypad configuration for part 1 (standard 3x3 keypad)
KEYPAD = [
    [1, 2, 3],    # Row 0 (top)
    [4, 5, 6],    # Row 1 (middle)
    [7, 8, 9],    # Row 2 (bottom)
]


# Keypad configuration for part 2 (diamond shaped, allows spaces for empty positions).
# Lines are aligned as lists of characters for indexed access.
KEYPAD_PART2 = """
  1  
 234 
56789
 ABC 
  D  
""".strip("\n").split("\n")
# Assumption: Each row of KEYPAD_PART2 contains an equal number of characters.
# Spaces represent invalid/non-existent keys.

def part1(_in):
    """
    Simulates movement instructions on a standard 3x3 keypad to determine the bathroom code.

    Parameters:
        _in (list of str): List of strings, 
        each representing one line of movement instructions (U/D/L/R).

    Returns:
        str: The final code, combined from results after each instruction line.

    Implementation details:
    - Starts at '5' (coordinates x=1, y=1)
    - Ensures that movement outside the keypad boundaries does not occur
    """
    x = 1  # Start at column 1 (center), which is '5'
    y = 1  # Start at row 1 (center)
    code = []  # Will store each digit after completing a line

    for line in _in:
        for instruction in line:
            # Move left but do not leave left edge
            if instruction == "L":
                x = max(0, x - 1)
            # Move right but do not leave right edge
            elif instruction == "R":
                x = min(len(KEYPAD[0]) - 1, x + 1)
            # Move up but do not leave top edge
            elif instruction == "U":
                y = max(0, y - 1)
            # Move down but do not leave bottom edge
            elif instruction == "D":
                y = min(len(KEYPAD) - 1, y + 1)
        # After one line, add the current keypad digit to the code
        code.append(KEYPAD[y][x])

    # Convert all code elements to str and return the joined result
    return "".join(str(x) for x in code)


def part2(_in):
    """
    Simulates movement on a non-standard, diamond-shaped keypad 
    (with potential blank keys) to determine the bathroom code.

    Parameters:
        _in (list of str): List of strings, 
        each representing one line of movement instructions (U/D/L/R).

    Returns:
        str: The final code, combined from results after each instruction line.

    Implementation details:
    - Starts at '5' (position x=0, y=2 within KEYPAD_PART2 layout)
    - Prevents movement to spaces/invalid positions
    - Each time a line of moves completes, records the label currently under the cursor

    Note: Each row of KEYPAD_PART2 can be indexed for both row (y) and column (x).
    """
    x = 0  # Starting column for '5' (row 2, column 0)
    y = 2  # Starting row for '5'
    code = []  # Will store code letters/digits after each line

    print(KEYPAD_PART2)  # Debug statement: prints out current keypad layout

    for line in _in:
        for instruction in line:
            # Check movement left is within bounds and doesn't land on a space
            if instruction == "L" and x - 1 >= 0 and KEYPAD_PART2[y][x - 1] != " ":
                x -= 1
            # Check movement right is within bounds and doesn't land on a space
            elif instruction == "R" and x + 1 < len(KEYPAD_PART2[y]) and KEYPAD_PART2[y][x + 1] != " ":
                x += 1
            # Check movement up is within bounds and doesn't land on a space
            if instruction == "U" and y - 1 >= 0 and KEYPAD_PART2[y - 1][x] != " ":
                y -= 1
            # Check movement down is within bounds and doesn't land on a space
            elif instruction == "D" and y + 1 < len(KEYPAD_PART2) and KEYPAD_PART2[y + 1][x] != " ":
                y += 1
        # After one line, add the current key to the code
        code.append(KEYPAD_PART2[y][x])

    # Return the resulting code as a string
    return "".join(str(x) for x in code)


def get_input(filename: str):
    """
    Reads the input file and returns the instructions as a list of non-empty lines.

    Parameters:
        filename (str): Path to the input file

    Returns:
        list of str: Each string is a set of instructions for one bathroom code digit

    Implementation notes:
    - Empty lines are skipped/ignored.
    """
    with open(filename, "r") as f:
        _in = [
            line
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
        *_in: Arguments to pass to the function (should be the instructions).

    Returns:
        None

    Implementation notes:
    - Prints running time and function result to stdout.
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

    Assumptions:
        argv[1] provides a valid and readable file name
    """
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    benchmark("PART 1", part1, _in)
    benchmark("PART 2", part2, _in)

if __name__ == "__main__":
    main()

