

def sgn(n: int) -> int:
    return 1 if n > 0 else 0 if n == 0 else -1


class Point2D:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'Point2D({self.x}, {self.y})'

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)


class Rope:

    DIRECTIONS = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1)
    }

    def __init__(self, x: int = 0, y: int = 0):
        self.head = Point2D(x, y)
        self.tail = Point2D(x, y)

    def move(self, direction: str) -> None:
        vector = Point2D(*self.DIRECTIONS[direction])
        self.head += vector
        self.repair_tail()

    def move_multiple_times(self, direction: str, n: int) -> None:
        for i in range(n):
            self.move(direction)
            print(self.head, self.tail)
    
    def repair_tail(self) -> None:
        diff = self.tail - self.head
        
        if abs(diff.x) <= 1 and abs(diff.y) <= 1:
            return
        
        if diff.x == 0:
            # Vertical case
            self.tail.y -= sgn(diff.y)

        elif diff.y == 0:
            # Horizontal case
            self.tail.x -= sgn(diff.x)
        else:
            # Diagonal case
            self.tail.x -= sgn(diff.x)
            self.tail.y -= sgn(diff.y)


class LongRope:
    def __init__(self, length: int, x: int = 0, y: int = 0):
        self.length = length
        
        self._ropes = [Rope(x, y) for _ in range(length)]
    
    @property
    def tail(self) -> Rope:
        return self._ropes[-1].tail

    @property
    def head(self) -> Rope:
        return self._ropes[0]

    def move(self, direction: str) -> None:
        self.head.move(direction)
        
        tail = self.head.tail
        for rope in self._ropes[1:]:
            rope.head = Point2D(tail.x, tail.y)
            rope.repair_tail()
            tail = rope.tail


def get_input() -> list:
    with open("input.txt", "r") as f:
        _in = [(line.split()[0], int(line.split()[1])) for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in: list) -> None:
    
    rope = Rope(0, 0)

    visited_points = set()

    for direction, n in _in:
        for i in range(n):
            rope.move(direction)
            visited_points.add((rope.tail.x, rope.tail.y))

    print("PART 1:", len(visited_points))


def part2(_in: list) -> None:
    rope = LongRope(9, 0, 0)

    visited_points = set()

    for direction, n in _in:
        for i in range(n):
            rope.move(direction)
            visited_points.add((rope.tail.x, rope.tail.y))

    print("PART 2:", len(visited_points))


def main() -> None:
    _in = get_input()
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
