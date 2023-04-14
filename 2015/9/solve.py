#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in

def get_distances(routes: dict) -> list[int]:

    visited = list()
    distances = list()
    distance = 0

    def dfs(source: str) -> None:

        nonlocal distance

        if len(visited) == len(routes):
            distances.append(distance)
            return

        if routes.get(source) is None:
            return

        for dest in routes[source]:
            if dest not in visited:
                visited.append(dest)
                distance += routes[source][dest]
                dfs(dest)
                distance -= routes[source][dest]
                visited.pop()


    for source in routes:
        visited.append(source)
        dfs(source)
        visited.pop()

    return distances

def part1(_in):
    routes = dict()
    for line in _in:
        source, part2 = line.split(" to ")
        dest, dist = part2.split(" = ")
        dist = int(dist)

        if routes.get(source) is None:
            routes[source] = dict()
        routes[source][dest] = dist


        if routes.get(dest) is None:
            routes[dest] = dict()
        routes[dest][source] = dist

    return min(get_distances(routes))

def part2(_in):
    routes = dict()
    for line in _in:
        source, part2 = line.split(" to ")
        dest, dist = part2.split(" = ")
        dist = int(dist)

        if routes.get(source) is None:
            routes[source] = dict()
        routes[source][dest] = dist


        if routes.get(dest) is None:
            routes[dest] = dict()
        routes[dest][source] = dist

    return max(get_distances(routes))


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
