package main

import (
    "fmt"
    "io"
    "os"
    "log"
    "strings"
    "strconv"
    "sort"
)


func parseInput(input string) ([]int, []int) {
    lines := strings.Split(input, "\n")
    leftNumbers := make([]int, len(lines))
    rightNumbers := make([]int, len(lines))

    for lineIdx, line := range lines {
        if line == "" {
            continue
        }
        var err error
        var splittedLine []string = strings.Split(line, "   ")
        leftNumbers[lineIdx], err = strconv.Atoi(splittedLine[0])
        if err != nil {
            log.Fatal(fmt.Sprintf("%s is not a valid integer in line %d", line, lineIdx))
        }
        rightNumbers[lineIdx], err = strconv.Atoi(splittedLine[1])
        if err != nil {
            log.Fatal(fmt.Sprintf("%s is not a valid integer in line %d", line, lineIdx))
        }
    }

    return leftNumbers, rightNumbers
}


func part1(input string) {
    leftNumbers, rightNumbers := parseInput(input)
    sort.Ints(leftNumbers)
    sort.Ints(rightNumbers)

    var totalDistance int = 0
    var distance int
    for i := 0; i < len(leftNumbers); i++ {
        distance = leftNumbers[i] - rightNumbers[i]
        if distance < 0 {
            distance = -distance
        }
        totalDistance += distance
    }
    fmt.Printf("Part 1: %d\n", totalDistance)
}


func getOccurences(countCache map[int]int, numbers []int, searchedNumber int) int {
    if val, exists := countCache[searchedNumber]; exists {
        return val
    }
    occurencesCount := 0
    for _, number := range numbers {
        if number == searchedNumber {
            occurencesCount += 1
        }
    }
    countCache[searchedNumber] = occurencesCount
    return occurencesCount
}


func part2(input string) {
    leftNumbers, rightNumbers := parseInput(input)
    countCache := make(map[int]int)
    var totalOccurences int = 0
    for _, leftNumber := range leftNumbers {
        totalOccurences += leftNumber*getOccurences(countCache, rightNumbers, leftNumber)
    }
    fmt.Printf("Part 2: %d\n", totalOccurences)
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
