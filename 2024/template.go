package main

import (
    // "fmt"
    "io"
    "os"
    "log"
    "strings"
    // "strconv"
    // "sort"
)


func parseInput(input string) []int {
    rawLines := strings.Split(input, "\n")
    lines := make([]string, 0, len(rawLines))
    for _, rawLine := range rawLines {
        if strings.TrimSpace(rawLine) != "" {
            lines = append(lines, rawLine)
        }
    }
    return []int{}
}


func part1(input string) {
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
