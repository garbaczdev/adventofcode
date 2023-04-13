from typing import Tuple

import numpy as np


DIRECTIONS = [(x, y) for y in range(1, -2, -1) for x in range(-1, 2)]


class ImageEnhancer:

    def __init__(self, image_points: set, enhancement_algorithm: np.array) -> None:
        self.image_points = image_points
        self.enhancement_algorithm = enhancement_algorithm

        self.enhancement_count = 0
        self.is_algorithm_devilish = enhancement_algorithm[0] and not enhancement_algorithm[-1]

    def enhance(self) -> None:
        (x_min, y_min), (x_max, y_max) = self.get_extreme_points()

        new_image_points = set()

        for y in range(y_min - 1, y_max + 2):
            for x in range(x_min - 1, x_max + 2):
                
                binary_number = ""

                for x_d, y_d in DIRECTIONS:
                    
                    new_x = x + x_d
                    new_y = y + y_d

                    if self.is_algorithm_devilish and self.enhancement_count % 2 == 1:
                        if new_x < x_min or new_x > x_max or new_y < y_min or new_y > y_max:
                            binary_number += "1"
                            continue

                    if (new_x, new_y) in self.image_points:
                        binary_number += "1"

                    else:
                        binary_number += "0"

                if self.enhancement_algorithm[int(binary_number, 2)]:
                    new_image_points.add((x, y))

        self.enhancement_count += 1
        self.image_points = new_image_points


    def print_image(self) -> None:
        (x_min, y_min), (x_max, y_max) = self.get_extreme_points()

        image = np.zeros((y_max - y_min + 1, x_max - x_min + 1))

        for x, y in self.image_points:
            image[y_max - y][x - x_min] = 1

        for row in image:
            line = ""
            for element in row:
                if element == 0:
                    line += "."

                elif element == 1:
                    line += "#"

            print(line)
        print()

    def get_extreme_points(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        x_min = min(self.image_points, key = lambda point: point[0])[0]
        y_min = min(self.image_points, key = lambda point: point[1])[1]

        x_max = max(self.image_points, key = lambda point: point[0])[0]
        y_max = max(self.image_points, key = lambda point: point[1])[1]

        return ((x_min, y_min), (x_max, y_max))



def task1(image_points: set, enhancement_algorithm: np.array) -> None:
    image_enhancer = ImageEnhancer(image_points, enhancement_algorithm)

    for _ in range(2):
        image_enhancer.enhance()

    print(len(image_enhancer.image_points))


def task2(image_points: set, enhancement_algorithm: np.array) -> None:
    image_enhancer = ImageEnhancer(image_points, enhancement_algorithm)

    for _ in range(50):
        image_enhancer.enhance()

    print(len(image_enhancer.image_points))


def main() -> None:
    with open("input.txt", "r") as f:
        segments = [segment for segment in f.read().split("\n\n")]
        
        image_points = set()

        image = segments[1].split("\n")

        for y, row in enumerate(image):
            for x, element in enumerate(row):
                if element == "#":
                    image_points.add((x, len(image) - y))

        enhancement_algorithm = np.array([char == "#" for char in segments[0].replace("\n", "")], dtype=np.bool)

    # task1(image_points, enhancement_algorithm)
    task2(image_points, enhancement_algorithm)

    


if __name__ == '__main__':
    main()
