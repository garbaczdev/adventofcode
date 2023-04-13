
def task1(commands: list) -> None:
    depth = 0
    x = 0
    for command in commands:

        if command[0] == "forward":
            x += int(command[1])

        elif command[0] == "down":
            depth += int(command[1])

        elif command[0] == "up":
            depth -= int(command[1])
    
    print(depth*x)

def task2(commands:list) -> None:
    depth = 0
    x = 0
    aim = 0
    for command in commands:

        if command[0] == "forward":
            x += int(command[1])
            depth += aim*int(command[1])

        elif command[0] == "down":
            aim += int(command[1])

        elif command[0] == "up":
            aim -= int(command[1])
    
    print(depth*x)

def main() -> None:
    with open("input.txt", "r") as f:
        commands = [line.split() for line in f.read().split("\n") if line.strip()]

    task1(commands)
    task2(commands)

if __name__ == "__main__":
    main()