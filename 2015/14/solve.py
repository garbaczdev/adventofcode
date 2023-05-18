#!/usr/bin/env python3
from sys import argv
from datetime import datetime


class Reindeer:
    def __init__(self, speed: int, sprint_time: int, rest_time: int):
        self.speed = speed
        self.sprint_time = sprint_time
        self.rest_time = rest_time

    def __repr__(self):
        return f"Reindeer({self.speed} km/s, {self.sprint_time}s sprint, {self.rest_time}s rest)"


class RacingReindeer(Reindeer):

    def __init__(self, speed: int, sprint_time: int, rest_time: int):
        super().__init__(speed, sprint_time, rest_time)
        
        self.distance = 0
        self.is_resting = False
        self.seconds_sprinting = 0
        self.seconds_resting = 0

    def __repr__(self):
        return f"RacingReindeer(distance={self.distance}, is_resting={self.is_resting})"

    def run(self):
        if self.is_resting:

            self.seconds_resting += 1

            if self.seconds_resting == self.rest_time:
                self.is_resting = False
                self.seconds_resting = 0 
        else:

            self.seconds_sprinting += 1
            self.distance += self.speed

            if self.seconds_sprinting == self.sprint_time:
                self.is_resting = True
                self.seconds_sprinting = 0


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line.split() for line in f.read().split("\n") if line.split()]
    return _in


def part1(_in, time = 2503):
    reindeers = [
        Reindeer(int(line[3]), int(line[6]), int(line[13]))
        for line in _in
    ]

    distances = []
    for reindeer in reindeers:

        dist = 0
        seconds = 0

        while seconds + reindeer.sprint_time + reindeer.rest_time < time:
            seconds += reindeer.sprint_time + reindeer.rest_time
            dist += reindeer.sprint_time * reindeer.speed

        sprint_seconds = time - seconds \
                            if time - seconds < reindeer.sprint_time \
                            else reindeer.sprint_time

        dist += reindeer.speed*sprint_seconds
        distances.append(dist)

    return max(distances)



def part2(_in, time=2503):
    reindeers = [
        RacingReindeer(int(line[3]), int(line[6]), int(line[13]))
        for line in _in
    ]

    points = [0 for reindeer in reindeers]

    previous_leading_reindeer = None

    for second in range(time):

        for reindeer in reindeers:
            reindeer.run()

        max_distance = max(reindeer.distance for reindeer in reindeers)
        
        for index, reindeer in enumerate(reindeers):
            if reindeer.distance == max_distance:
                points[index] += 1
    
    return max(points)


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
