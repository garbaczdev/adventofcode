#!/usr/bin/env python3
from sys import argv
from datetime import datetime


MAP_ORDER = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]


def get_input(filename: str):
    with open(filename, "r") as f:
        content = f.read()
        _in = (
            {
                tuple(
                    segment.split("\n")[0].split()[0].split("-")[::2]
                ): [list(map(int, line.split())) for line in segment.split("\n")[1:] if line.split()]
                for segment in content.split("\n\n")[1:] if segment.split()
            },
            tuple(map(int, content.split("\n")[0].split(": ")[1].split()))
        )

    return _in


def get_current_mapping(maps, current_mapping):
    for start2, start1, _range in maps:
        # print(start1, start2, _range, current_mapping)
        if start1 <= current_mapping < start1 + _range:
            return current_mapping - start1 + start2
    return current_mapping


def part1(_in):
    
    maps, seeds = _in

    locations = []
    for seed in seeds:
        current_mapping = seed
        for n1, n2 in zip(MAP_ORDER, MAP_ORDER[1:]):
            current_mapping = get_current_mapping(maps[(n1,n2)], current_mapping)
        locations.append(current_mapping)
    return min(locations)


def split_ranges(maps, ranges:list[tuple[int, int]]) -> list[tuple[int, int]]:
    initial_ranges = ranges
    ranges = ranges[:]
    new_ranges = []

    while ranges:
        _range = ranges.pop(0)
        for start2, start1, map_length in maps:
            map_range = (start1, start1 + map_length - 1)
            overlap = (max(map_range[0], _range[0]), min(map_range[1], _range[1]))
            if overlap[0] > overlap[1]:
                continue

            if _range[0] < overlap[0]:
                ranges.append((_range[0], overlap[0]-1))
            if _range[1] > overlap[1]:
                ranges.append((overlap[1]+1, _range[1]))
            new_ranges.append((
                overlap[0] - start1 + start2,
                overlap[1] - start1 + start2
            ))
            break
        # Nobreak
        else:
            # No overlap with any range!
            new_ranges.append(_range)
    # print(initial_ranges, new_ranges, maps)
    return new_ranges



def part2(_in):
    
    maps, o_seeds = _in
    
    min_location = float("inf")
    for o_seed, length in zip(o_seeds[::2], o_seeds[1::2]):
        current_mapping = [(o_seed, o_seed+length-1)]
        for n1, n2 in zip(MAP_ORDER, MAP_ORDER[1:]):
            current_mapping = split_ranges(maps[(n1,n2)], current_mapping)
        min_location = min(min_location, min(s for s,e in current_mapping))
    return min_location



def benchmark(name: str, func, *_in) -> None:
    now = datetime.now()
    result = func(*_in)
    _time = datetime.now() - now
    print(f"({_time}) {name}: {result}")


def main() -> None:
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    benchmark("PART 1", part1, _in)
    benchmark("PART 2", part2, _in)


if __name__ == "__main__":
    main()
