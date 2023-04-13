
def is_small(cave_name: str) -> bool:
    return cave_name.lower() == cave_name

def task1(connections: dict) -> None:
    visited_caves = set()
    visited_caves.add("start")

    count = 0

    def dfs(current_node: str = "start") -> None:

        nonlocal count

        if current_node == "end":
            count += 1
            return

        for next_node in connections[current_node]:

            if next_node not in visited_caves:
                
                if is_small(next_node):
                    visited_caves.add(next_node)
                    dfs(next_node)
                    visited_caves.remove(next_node)

                else:
                    dfs(next_node)

    dfs()

    print(count)

def task2(connections: dict) -> None:
    visited_caves = set()
    visited_caves.add("start")

    count = 0
    visited_twice = None

    def dfs(current_node: str = "start") -> None:

        nonlocal count, visited_twice

        if current_node == "end":
            count += 1
            return

        for next_node in connections[current_node]:

            if is_small(next_node):
                if next_node in visited_caves:
                    if visited_twice is None and next_node != "start":
                        visited_twice = next_node
                        dfs(next_node)
                        visited_twice = None

                else:
                    visited_caves.add(next_node)
                    dfs(next_node)
                    visited_caves.remove(next_node)

            else:
                dfs(next_node)

    dfs()

    print(count)

def main() -> None:
    
    connections = dict()

    with open("input.txt", "r") as f:
        lines = [line.split("-") for line in f.read().split("\n") if line.strip()]

        for _from, to in lines:
            if connections.get(_from) is None:
                connections[_from] = list()

            connections[_from].append(to)

            if connections.get(to) is None:
                connections[to] = list()

            connections[to].append(_from)

    task2(connections)


if __name__ == '__main__':
    main()
