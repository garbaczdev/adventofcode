import numpy as np

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_lowest(map: np.array, x: int, y: int) -> bool:
    for x_d, y_d in DIRECTIONS:
        try:
            if map[y + y_d][x + x_d] <= map[y][x]:
                return False
        except IndexError:
            pass

    return True


def get_lowest_points(map: np.array) -> list:
    
    lowest_points = list()

    for y in range(len(map)):
        for x in range(len(map[y])):
            if is_lowest(map, x, y):
                lowest_points.append((x, y))

    return lowest_points


def task1(map: np.array) -> None:

    lowest_points = get_lowest_points(map)
    point_values = [map[y][x] for x, y in lowest_points]

    print(sum(point_values) + len(point_values))


def task2(map: np.array) -> None:

    basin_mask = np.zeros(map.shape)

    def basin_dfs(x: int, y: int) -> int:

        if basin_mask[y][x]:
            return 0
        
        basin_mask[y][x] = 1

        basin_sum = 1

        for x_d, y_d in DIRECTIONS:
            try:
                xc = x + x_d
                yc = y + y_d

                if xc < 0 or yc < 0:
                    raise IndexError("Out of range")

                if map[yc][xc] >= map[y][x] and map[yc][xc] != 9:
                    basin_sum += basin_dfs(xc, yc)
            except IndexError:
                pass
        return basin_sum

    basin_sizes = list()

    for lowest_point in get_lowest_points(map):
        basin_sizes.append(basin_dfs(*lowest_point))

    largest_basins = sorted(basin_sizes, reverse=True)[:3]
    
    result = 1
    for largest_basin in largest_basins:
        result *= largest_basin
    
    print(result)



def main() -> None:
    with open("input.txt", "r") as f:
        map = np.array([[int(char) for char in line] for line in f.read().split("\n") if line.strip()])

    # task1(map)
    task2(map)

if __name__ == '__main__':
    main()
