package main

import (
    "fmt"
    "io"
    "os"
    "strings"
    "time"
)


func parseInput(input string) []int {
    input = strings.Trim(input, "\n")
    // lines := strings.Split(input, "\n")
    return []int{}
}


func part1(input string) int {
    return 0
}


func part2(input string) int {
    return 0
}


func getInput() string {
    inputBytes, err := io.ReadAll(os.Stdin)
    if err != nil || len(inputBytes) == 0 {
        panic("No STDIN input is empty")
    }
    return string(inputBytes)
}


func main() {
    input := getInput()

    start := time.Now()
    result1 := part1(input)
    fmt.Printf("[Part 1][%v] %d\n", time.Since(start), result1)

    start = time.Now()
    result2 := part2(input)
    fmt.Printf("[Part 2][%v] %d\n", time.Since(start), result2)
}
