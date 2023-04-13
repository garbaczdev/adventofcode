
class Segment:
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:

        self.start_x = start_x
        self.start_y = start_y

        self.end_x = end_x
        self.end_y = end_y

    def __repr__(self) -> str:
        return f"Segment({self.start_x}, {self.start_y} -> {self.end_x}, {self.end_y})"

    def is_straight(self) -> bool:
        return self.start_x == self.end_x or self.start_y == self.end_y

    def get_points(self) -> list:

        x_mark = self.get_num_mark(self.end_x - self.start_x)
        y_mark = self.get_num_mark(self.end_y - self.start_y)

        x = self.start_x
        y = self.start_y

        points = list()

        while x != self.end_x + x_mark or y != self.end_y + y_mark:
            points.append((x, y))
            
            x += x_mark
            y += y_mark

        return points

        # if self.is_straight():
        #     start_x, end_x = sorted([self.start_x, self.end_x])
        #     start_y, end_y = sorted([self.start_y, self.end_y])
        #     return [(x, y) for x in range(start_x, end_x + 1) for y in range(start_y, end_y + 1)]

    @staticmethod
    def get_num_mark(num: int) -> int:
        if num > 0:
            return 1
        
        elif num == 0:
            return 0

        else:
            return -1

def count_point_overlaps(segments: list) -> None:
    point_overlaps = dict()

    for segment in segments:
        for point in segment.get_points():
            if point_overlaps.get(point) is None:
                point_overlaps[point] = 0

            point_overlaps[point] += 1

    return point_overlaps

def get_overlapping_points(point_overlaps) -> list:
    return [points_item[0] for points_item in point_overlaps.items() if points_item[1] >= 2]


def task2(segments: list) -> None:
    point_overlaps = count_point_overlaps(segments)

    print(len(get_overlapping_points(point_overlaps)))


def task1(segments: list) -> None:
    segments = [segment for segment in segments if segment.is_straight()]

    point_overlaps = count_point_overlaps(segments)

    print(len(get_overlapping_points(point_overlaps)))



def get_input() -> list:
    with open("input.txt", "r") as f:
        return [Segment(*[int(num) for num in line.replace(" -> ", ",").split(",")]) for line in f.read().split("\n") if line.strip()]


def main() -> None:
    segments = get_input()
    # task1(segments)
    task2(segments)


if __name__ == '__main__':
    main()
