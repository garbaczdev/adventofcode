#!/usr/bin/env python3
from sys import argv
from datetime import datetime


class Point2D:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y

    def __sub__(self, point):
        return Point2D(self.x - point.x, self.y - point.y)

    def __add__(self, point):
        return Point2D(self.x + point.x, self.y + point.y)

    def dist_from(self, point) -> int:
        diff = point - self
        return abs(diff.x) + abs(diff.y)


class Sensor:
    def __init__(self, line: str):

        self._line = line

        self.cord = self._get_sensor_cord(line)
        self.beacon = self._get_beacon_cord(line)

        self.dist_from_beacon = self.cord.dist_from(self.beacon)

    def __repr__(self) -> str:
        return f'Sensor({self.cord}, {self.dist_from_beacon})'

    def covers(self, point: Point2D) -> bool:
        return point.dist_from(self.cord) <= self.dist_from_beacon

    @staticmethod
    def _get_sensor_cord(line: str) -> Point2D:
        sensor_line = line.split(":")[0] 
        x_line, y_line = sensor_line.split(",")
        x = int(x_line.split("x=")[1])
        y = int(y_line.split("y=")[1])
        return Point2D(x, y)
        
    @staticmethod
    def _get_beacon_cord(line: str) -> Point2D:
        beacon_line = line.split(":")[1] 
        x_line, y_line = beacon_line.split(",")
        x = int(x_line.split("x=")[1])
        y = int(y_line.split("y=")[1])
        return Point2D(x, y)


class Board:
    def __init__(self, sensors: list[Sensor]):
        self.sensors = sensors
        self.beacons = [sensor.beacon for sensor in sensors]

        self.min_corner, self.max_corner = self.get_corners_cords(sensors)

    def print(self, show_coverage=False) -> None:
        diff = self.max_corner - self.min_corner
        width = diff.x + 1
        height = diff.y + 1

        for y in range(height):
            line = list()
            for x in range(width):

                point = Point2D(self.min_corner.x + x, self.min_corner.y + y)

                if any(sensor.cord == point for sensor in self.sensors):
                    line.append("S")
                elif any(sensor.beacon == point for sensor in self.sensors):
                    line.append("B")
                elif show_coverage and any(sensor.covers(point) for sensor in self.sensors):
                    line.append("#")
                else:
                    line.append(".")
            print("%5d" % point.y, "".join(line))

    def calculate_occupied_beacon_spots(self, y: int) -> int:
        diff = self.max_corner - self.min_corner
        width = diff.x + 1

        count = 0
        for x in range(width):
            point = Point2D(self.min_corner.x + x, y)

            for sensor in self.sensors:
                if sensor.covers(point):
                    if sensor.beacon != point:
                        count += 1
                    break


        return count
            
    
    @staticmethod
    def get_corners_cords(sensors: list) -> tuple[Point2D, Point2D]:
        
        return (
            Point2D(
                min(map(lambda sensor: sensor.cord.x - sensor.dist_from_beacon, sensors)),
                min(map(lambda sensor: sensor.cord.y - sensor.dist_from_beacon, sensors))
            ),
            Point2D(
                max(map(lambda sensor: sensor.cord.x + sensor.dist_from_beacon, sensors)),
                max(map(lambda sensor: sensor.cord.y + sensor.dist_from_beacon, sensors))
            )
        )


def get_input(filename: str) -> list:
    with open(filename, "r") as f:
        _in = [Sensor(line) for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in: list):
    board = Board(_in)
    result = board.calculate_occupied_beacon_spots(2000000)
    board.print()
    print()
    board.print(True)
    return result


def part2(_in: list):
    pass


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
