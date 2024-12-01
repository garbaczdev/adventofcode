package main

import (
    "fmt"
    "io"
    "os"
    "log"
    "strings"
    "strconv"
)


func parseInput(input string) []int {
    lines := strings.Split(input, "\n")
    numbers := make([]int, 0, len(lines))

    for lineIdx, line := range lines {
        if line == "" {
            continue
        }
        num, err := strconv.Atoi(line)
        if err != nil {
            log.Fatal(fmt.Sprintf("%d is not a valid integer in line %d", line, lineIdx))
        }

        numbers = append(numbers, num)
    }

    return numbers
}


func part1(input string) {
    masses := parseInput(input)
    var fuelRequired int = 0
    for _, mass := range masses {
        fuelRequired += int(mass/3) - 2
    }
    fmt.Printf("Part 1: %d\n", fuelRequired)
}


func part2(input string) {
    masses := parseInput(input)
    var totalFuelRequired int = 0
    for _, mass := range masses {
        mass = int(mass/3) - 2
        newFuelRequired := mass
        for newFuelRequired > 0 {
            mass = newFuelRequired
            totalFuelRequired += mass
            newFuelRequired = int(mass/3) - 2
        }
    }
    fmt.Printf("Part 2: %d\n", totalFuelRequired)
}


func getInput() string {
    inputBytes, err := io.ReadAll(os.Stdin)
    if err != nil || len(inputBytes) == 0 {
        log.Fatal("No STDIN input is empty")
    }
    return string(inputBytes)
}


func main() {
    input := getInput()
    part1(input)
    part2(input)
}
