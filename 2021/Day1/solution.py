
def task1(numbers: list) -> None:
    print(sum([1 if num2 > num1 else 0 for num1, num2 in zip(numbers, numbers[1:])]))

def task2(numbers:list) -> None:
    windows = [sum(num for num in numbers[i:i+3]) for i in range(len(numbers) - 2)]
    print(sum([1 if num2 > num1 else 0 for num1, num2 in zip(windows, windows[1:])]))

def main() -> None:
    with open("input.txt", "r") as f:
        numbers = [int(line) for line in f.read().split("\n") if line.strip()]

    task1(numbers)
    task2(numbers)

if __name__ == "__main__":
    main()