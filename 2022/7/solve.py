from functools import lru_cache


def dict_list_add(_dict: dict, key, element) -> None:
    if _dict.get(key) is None:
        _dict[key] = [element]
    else:
        _dict[key].append(element)

class Command:
    def __init__(self, command: str):
        lines = [line for line in command.split("\n") if line.split()]
        self.input = lines[0].split()
        self.output = lines[1:]

        self.type = "cd" if len(self.input) == 2 else "ls"

        if self.type == "ls":
            self.output = [content.split() for content in self.output]


class FileSystem:
    def __init__(self, commands: list[Command]):
        self.dirs, self.files = self.build_system(commands)


    def print(self) -> None:
        self.print_dir(("/",))
    
    def print_dir(self, _dir: tuple, indent=1) -> None:
        
        tabs = '\t'*(indent-1)
        print(f"{tabs}- {_dir[-1]} (dir)")
        
        if self.dirs.get(_dir) is not None:
            for _dir_inside in self.dirs[_dir]:
                self.print_dir((*_dir, _dir_inside), indent + 1)

        tabs += '\t'

        if self.files.get(_dir) is not None:
            for file in self.files[_dir]:
                print(f"{tabs}- {file[0]} (file, size={file[1]})")

    def get_dir_sizes(self) -> dict:
        
        dir_sizes = {}

        def get_dir_size(_dir: tuple) -> int:

            if dir_sizes.get(_dir) is not None:
                return dir_sizes[_dir]

            size = 0

            if self.dirs.get(_dir) is not None:
                for _dir_inside in self.dirs[_dir]:
                    size += get_dir_size((*_dir, _dir_inside))


            if self.files.get(_dir) is not None:
                for file in self.files[_dir]:
                    size += file[1]

            dir_sizes[_dir] = size

            return size
    
        get_dir_size(('/',))

        return dir_sizes


    @staticmethod
    def build_system(commands: list[Command]) -> tuple[dict, dict]:

        files = dict()
        dirs = dict()

        cwd = []

        for command in commands:
            if command.type == "cd":
                if command.input[1] == "..":
                    cwd.pop()
                else:
                    cwd.append(command.input[1])
            
            elif command.type == "ls":
                for entity in command.output:
                    if entity[0] == "dir":
                        dict_list_add(dirs, tuple(cwd), entity[1])
                    else:
                        dict_list_add(files, tuple(cwd), (entity[1], int(entity[0])))

            else:
                raise Exception(f"{command.type} is not a correct command type.")
        
        return dirs, files


def get_input() -> list:
    with open("input.txt", "r") as f:
        commands = [command for command in f.read().split("$ ") if command.split()]

    _in = [Command(command) for command in commands]

    return _in


def part1(_in: list) -> None:
    system = FileSystem(_in)
    # Debugging
    system.print()
    sizes = system.get_dir_sizes()
    
    _sum = 0
    for _dir, size in sizes.items():
        if size <= 100000:
            _sum += size

    print("(PART 1) SUM OF DIRS:",_sum)

def part2(_in: list) -> None:
    system = FileSystem(_in)
    # Debugging
    # system.print()
    sizes = system.get_dir_sizes()
    
    REQUIRED_SPACE = 30_000_000 - 70_000_000 + sizes[("/",)]
    possible_dir_sizes = [size for _dir, size in sizes.items() if size >= REQUIRED_SPACE]
    _min = min(possible_dir_sizes)
    print("(PART 2) MIN DIR TO DELETE:", _min)



def main() -> None:
    _in = get_input()
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
