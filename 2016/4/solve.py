#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime


def part1_is_real(room: str) -> bool:
    encrypted_name = "".join(room.split("-")[:-1])
    checksum = room.split("[")[1].replace("]", "")

    # Count the occurence of each letter
    letter_counts = dict()
    for letter in encrypted_name:
        if letter not in letter_counts:
            letter_counts[letter] = 0
        letter_counts[letter] += 1

    # Transform into a list of letter per each count
    letters_per_count = dict()
    for letter, count in letter_counts.items():
        if count not in letters_per_count:
            letters_per_count[count] = set()
        letters_per_count[count].add(letter)

    # Sort the dict to achieve: [(5, {'a', 'b', 'c'}), (3, {'z'}))]
    sorted_letters_per_count = sorted(letters_per_count.items(), key=lambda item: item[0], reverse=True)
    for letter in checksum:
        if len(sorted_letters_per_count) == 0:
            return False

        most_frequent_letters = sorted_letters_per_count[0][1]
        if letter in most_frequent_letters:
            most_frequent_letters.remove(letter)
        else:
            return False

        if len(most_frequent_letters) == 0:
            sorted_letters_per_count.pop(0)

    return True
        

def part1(_in):
    result = 0
    for room in _in:
        if part1_is_real(room):
            room_sector_id = int(room.split("-")[-1].split("[")[0])
            result += room_sector_id
    return result


def part2_decrypt(room: str) -> str:
    room_sector_id = int(room.split("-")[-1].split("[")[0])
    # Extract the encrypted text and replace dashes with spaces
    encrypted_letters = list(" ".join(room.split("-")[:-1]))

    ord_a = ord("a")
    
    decrypted_letters = list()
    for encrypted_letter in encrypted_letters:
        if encrypted_letter == " ":
            # Don't decrypt spaces
            decrypted_letters.append(encrypted_letter)
        else:
            decrypted_letter = chr(ord_a + (ord(encrypted_letter) - ord_a + room_sector_id) % 26)
            decrypted_letters.append(decrypted_letter)

    return "".join(decrypted_letters)
    


def part2(_in):
    for room in _in:
        decrypted_name = part2_decrypt(room)
        if "north" in decrypted_name:
            print(decrypted_name)
            room_sector_id = int(room.split("-")[-1].split("[")[0])
            return room_sector_id


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            line
            for line in f.read().split("\n")
            if line.split()
        ]
    return _in


def benchmark(name: str, func, *_in) -> None:
    """
    Utility function to benchmark the given part function, printing timing and result.

    Parameters:
        name (str): A label to print alongside the benchmark.
        func (callable): The function to call.
        *_in: Arguments to pass to the function.

    Returns:
        None
    """
    now = datetime.now()
    result = func(*_in)
    _time = datetime.now() - now
    print(f"({_time}) {name}: {result}")

def main() -> None:
    """
    Reads command-line argument for the input file name, processes both parts,
    and prints their results and timings.

    Returns:
        None
    """
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    benchmark("PART 1", part1, _in)
    benchmark("PART 2", part2, _in)

if __name__ == "__main__":
    main()
