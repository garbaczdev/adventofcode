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


func part1(input string) {
}


func part2(input string) {
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
    part1(input)
    fmt.Printf("[Part 1] Elapsed time: %v\n", time.Since(start))

    start = time.Now()
    part2(input)
    fmt.Printf("[Part 2] Elapsed time: %v\n", time.Since(start))
}
