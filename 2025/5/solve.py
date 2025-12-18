#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime


def part1(_in):
    fresh_ranges, ingredient_ids = _in

    fresh_ingredients_count = 0
    for ingredient_id in ingredient_ids:
        if any(
            range_start <= ingredient_id <= range_end
            for range_start, range_end in fresh_ranges
        ):
            fresh_ingredients_count += 1

    return fresh_ingredients_count

def part2(_in):
    fresh_ranges, ingredient_ids = _in

    min_range_start = min(fresh_range[0] for fresh_range in fresh_ranges)
    max_range_end = max(fresh_range[1] for fresh_range in fresh_ranges)

    fresh_ingredients_count = 0

    ingredient_id = min_range_start
    # Iterate over all ranges by starting at the lowest start of any range
    while ingredient_id <= max_range_end:
        # Get all of the ranges that this id is currently in
        matching_ranges_end = [
            range_end
            for range_start, range_end in fresh_ranges
            if range_start <= ingredient_id <= range_end
        ]

        if matching_ranges_end:
            # Case: The current id is in some range.
            # Skip to the maximum range_end + 1
            furthest_range_end = max(matching_ranges_end)
            fresh_ingredients_count += furthest_range_end - ingredient_id + 1
            ingredient_id = furthest_range_end + 1
        else:
            # Case: The current id is not in any range.
            # Skip to the closest range_start
            closest_range_start = min(
                range_start
                for range_start, range_end in fresh_ranges
                if range_start > ingredient_id
            )
            ingredient_id = closest_range_start

    return fresh_ingredients_count


def get_input(filename: str):
    with open(filename, "r") as f:
        part1, part2 = f.read().split("\n\n")
        _in = (
            [
                (int(id_range.split("-")[0]), int(id_range.split("-")[1]))
                for id_range in part1.split("\n")
                if id_range.split()
            ],
            [
                int(_id)
                for _id in part2.split("\n")
                if _id.split()
            ]
        )
        
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
