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
    numbersStr := strings.Split(strings.Replace(input, "\n", "", -1), ",")
    numbers := make([]int, 0, len(numbersStr))

    for numberStrIdx, numberStr := range numbersStr {
        if numberStr == "" {
            continue
        }
        num, err := strconv.Atoi(numberStr)
        fmt.Println(numberStr);
        if err != nil {
            log.Fatal(fmt.Sprintf("%d is not a valid numberStr in idx %d", numberStr, numberStrIdx))
        }

        numbers = append(numbers, num)
    }

    return numbers
}


func part1(input string) {
    opcodes := parseInput(input)
    opcodes[1] = 12
    opcodes[2] = 2
    var pos int = 0

    for opcodes[pos] != 99 {
        fmt.Println(opcodes)
        if opcodes[pos] == 1 {
            opcodes[opcodes[pos+3]] = opcodes[opcodes[pos+1]] + opcodes[opcodes[pos+2]]
        } else if opcodes[pos] == 2 {
            opcodes[opcodes[pos+3]] = opcodes[opcodes[pos+1]] * opcodes[opcodes[pos+2]]
        } else {
            log.Fatal(fmt.Sprintf("Invalid opcode %d at pos %d", opcodes[pos], pos))
        }
        
        pos += 4
    }

    fmt.Printf("Part 1: %d\n", opcodes[0])
}


func part2(input string) {
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
