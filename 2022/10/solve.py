

class SimpleCPU:
    def __init__(self, instructions: list) -> None:
        self.instructions = instructions
        self.cycle = 0
        self.current_instruction = [0, 0] # [index, counter]
        self.reg = 1

    def do_cycle(self) -> None:

        if self.current_instruction[0] >= len(self.instructions):
            print("CPU: NO MORE INSTRUCTIONS TO PERFORM")
            return
        
        self.cycle += 1
        instruction = self.instructions[self.current_instruction[0]]

        if instruction[0] == "addx":
            if self.current_instruction[1] == 0:
                self.current_instruction[1] += 1
                return

        if instruction[0] == "addx":
            self.reg += instruction[1]
        
        self.current_instruction = [self.current_instruction[0] + 1, 0]


class AdvancedCPU(SimpleCPU):
    def __init__(self, instructions: list):
        super().__init__(instructions)

        self.screen = [["." for __ in range(40)] for _ in range(6)]

    def do_cycle(self) -> None:
        self._draw_pixel()
        super().do_cycle()

    def draw_screen(self) -> None:
        
        for _ in range(0, 240):
            self.do_cycle()

        self.print_display()

    def print_display(self) -> None:
        for row in self.screen:
            print("".join(row))

    def _draw_pixel(self) -> None:
        x, y = self.cycle % 40, self.cycle // 40

        for x_i in range(-1, 2):
            if self.reg + x_i == x:
                self.screen[y][x] = "#"



def get_input() -> list:
    with open("input.txt", "r") as f:
        _in = [[line.split()[0], int(line.split()[1])] if len(line.split()) == 2 else line.split() for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in: list) -> None:
    
    cpu = SimpleCPU(_in)

    wanted_cycles = set(range(20, 221, 40))
    cycles = dict()

    for i in range(1, 221):
        if i in wanted_cycles:
            cycles[i] = cpu.reg * i
        cpu.do_cycle()

    _sum = sum(cycles.values())
    print("PART 1:", _sum)


def part2(_in: list) -> None:
    cpu = AdvancedCPU(_in)
    cpu.draw_screen()


def main() -> None:
    _in = get_input()
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
