#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime


def part1(_in):
    number_of_splits = 0
    beam_column_indices = set()

    beam_start_idx = _in[0].index('S')
    beam_column_indices.add(beam_start_idx)

    current_idx = 0
    # Go row by row with the positions of beams
    # Adjust the positions of beams in a new row based on splits
    while current_idx < len(_in):
        new_beam_column_indices = set()

        for beam_column_idx in beam_column_indices:
            symbol_at_beam = _in[current_idx][beam_column_idx]
            if symbol_at_beam == '.' or symbol_at_beam == 'S':
                new_beam_column_indices.add(beam_column_idx)
            elif symbol_at_beam == '^':
                new_beam_column_indices.add(beam_column_idx - 1)
                new_beam_column_indices.add(beam_column_idx + 1)
                number_of_splits += 1
            else:
                raise ValueError(f"Unsupported map symbol {symbol_at_beam}")

        beam_column_indices = new_beam_column_indices
        current_idx += 1
            

    return number_of_splits


def part2(_in):
    beam_column_indices = dict()

    beam_start_idx = _in[0].index('S')
    beam_column_indices[beam_start_idx] = 1

    # This is the same as in part 1 but it keeps track of the
    # "strength" of a beam. If 2 beams merge, the strength of 
    # the new beam is the sum of the strengths of those 2 beams.
    #
    # The "strength" denotes the number of universes in which this
    # beam is in.
    current_idx = 0
    while current_idx < len(_in):
        new_beam_column_indices = dict()

        for beam_column_idx, beam_count in beam_column_indices.items():
            symbol_at_beam = _in[current_idx][beam_column_idx]

            if symbol_at_beam == '.' or symbol_at_beam == 'S':
                if new_beam_column_indices.get(beam_column_idx) is None:
                    new_beam_column_indices[beam_column_idx] = beam_count
                else:
                    new_beam_column_indices[beam_column_idx] += beam_count 
            elif symbol_at_beam == '^':
                if new_beam_column_indices.get(beam_column_idx - 1) is None:
                    new_beam_column_indices[beam_column_idx - 1] = beam_count
                else:
                    new_beam_column_indices[beam_column_idx - 1] += beam_count 

                if new_beam_column_indices.get(beam_column_idx + 1) is None:
                    new_beam_column_indices[beam_column_idx + 1] = beam_count
                else:
                    new_beam_column_indices[beam_column_idx + 1] += beam_count 
            else:
                raise ValueError(f"Unsupported map symbol {symbol_at_beam}")

        beam_column_indices = new_beam_column_indices
        current_idx += 1

    return sum(list(beam_column_indices.values()))


def get_input(filename: str):
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
