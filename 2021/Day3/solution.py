with open("input.txt", "r") as f:
    lines = [line for line in f.read().split("\n") if line.strip()]

# PART 1
gamma = ""
epsilon = ""

for x in range(len(lines[0])):
    bits = [line[x] for line in lines]
    if bits.count("1") > bits.count("0"):
        gamma += "1"
        epsilon += "0"

    else:
        gamma += "0"
        epsilon += "1"


print(int(gamma, 2) * int(epsilon, 2))

# PART 2
numbers = lines
index = 0
most_common = None

while len(numbers) > 1:

    bits = [number[index] for number in numbers]
    
    if bits.count("1") >= bits.count("0"):
        most_common = "1"

    else:
        most_common = "0"
    
    numbers = [number for number in numbers if number[index] == most_common]

    index += 1

oxygen = int(numbers[0], 2)
print(oxygen)

# PART 2
numbers = lines
index = 0
least_common = None

while len(numbers) > 1:

    bits = [number[index] for number in numbers]
    
    if bits.count("1") >= bits.count("0"):
        least_common = "0"

    else:
        least_common = "1"
    
    numbers = [number for number in numbers if number[index] == least_common]

    index += 1

co2 = int(numbers[0], 2)
print(co2)

print(co2*oxygen)