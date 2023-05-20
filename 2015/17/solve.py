#!/usr/bin/env python3
from sys import argv
from datetime import datetime


# def get_possible_containers(
#     available_containers: list[int], 
#     total_quanity: int
# ) -> list[int]:
# 
#     container_map = {
#         i: container
#         for i, container in enumerate(available_containers)
#     }
# 
#     available_containers = [
#         (container, i)
#         for i, container in enumerate(available_containers)
#     ]
# 
#     containers = set()
#     current_containers = list()
#     current_container_ids = set()
# 
#     def iterate_quanities() -> None:
# 
#         remaining_quanity = total_quanity - sum(current_containers)
#         
#         if remaining_quanity < 0:
#             return
# 
#         if remaining_quanity == 0:
#             containers.add(tuple(sorted(list(current_container_ids))))
#             return
# 
#         for container, id in available_containers:
#             if id not in current_container_ids:
#                 current_container_ids.add(id)
#                 current_containers.append(container)
#                 iterate_quanities()
#                 current_container_ids.remove(id)
#                 current_containers.pop()
#         
#     iterate_quanities()
#     return [[container_map[item] for item in container] for container in containers]


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            int(line)    
            for line in f.read().split("\n") 
            if line.split()
        ]

    return _in


def part1(_in, eggnog=150):

    valid_combinations = 0

    for i in range(2**len(_in)):
        bitmask = bin(i)[2:].zfill(len(_in))
        containers = [
            container 
            for i, container in enumerate(_in) 
            if bitmask[i] == "1"
        ]
        if sum(containers) == eggnog:
            valid_combinations += 1

    return valid_combinations


def part2(_in, eggnog=150):

    min_number = float("inf")

    for i in range(2**len(_in)):
        bitmask = bin(i)[2:].zfill(len(_in))
        containers = [
            container 
            for i, container in enumerate(_in) 
            if bitmask[i] == "1"
        ]
        if len(containers) < min_number and sum(containers) == eggnog:
            min_number = len(containers)
            min_containers = containers

    min_containers_count = 0

    for i in range(2**len(_in)):
        bitmask = bin(i)[2:].zfill(len(_in))
        containers = [
            container 
            for i, container in enumerate(_in) 
            if bitmask[i] == "1"
        ]
        if len(containers) == min_number and sum(containers) == eggnog:
            min_containers_count += 1

    return min_containers_count


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
