package main

import (
    "fmt"
    "io"
    "os"
    "strings"
    "time"
)


func parseInput(input string) ([]string, []string) {
    input = strings.Trim(input, "\n")
    inputSplit := strings.Split(input, "\n\n")
    
    patterns := strings.Split(inputSplit[0], ", ")
    designs := strings.Split(inputSplit[1], "\n")
    return patterns, designs
}



func canUsePattern(design string, pattern string) bool {
    if len(pattern) > len(design) {
        return false
    }
    
    for idx := range pattern {
        if design[idx] != pattern[idx] {
            return false
        }
    }

    return true
}


func getNumberOfPossibleDesigns(possibleDesignsCountCache map[string]int, patterns []string, design string) int {
    
    possibleDesignsCount, isCached := possibleDesignsCountCache[design]
    if isCached {
        return possibleDesignsCount
    }

    possibleDesignsCount = 0

    if len(design) == 0 {
        possibleDesignsCount = 1
    } else {
        for _, pattern := range patterns {
            if !canUsePattern(design, pattern) {
                continue
            }
            recursivePossibleDesignsResult := getNumberOfPossibleDesigns(possibleDesignsCountCache, patterns, design[len(pattern):])
            if recursivePossibleDesignsResult > 0 {
                possibleDesignsCount += recursivePossibleDesignsResult
            }
        }
    }

    possibleDesignsCountCache[design] = possibleDesignsCount
    return possibleDesignsCount
}


func part1(input string) int {
    patterns, designs := parseInput(input)
    possibleDesignsCountCache := make(map[string]int)

    possibleDesignsCount := 0
    for _, design := range designs {
        if getNumberOfPossibleDesigns(possibleDesignsCountCache, patterns, design) > 0 {
            possibleDesignsCount++
        }
    }
    return possibleDesignsCount
}


func part2(input string) int {
    patterns, designs := parseInput(input)
    possibleDesignsCountCache := make(map[string]int)

    totalPossibleDesignsCount := 0
    for _, design := range designs {
        possibleDesignsCount := getNumberOfPossibleDesigns(possibleDesignsCountCache, patterns, design)
        if possibleDesignsCount > 0 {
            totalPossibleDesignsCount += possibleDesignsCount
        }
    }
    return totalPossibleDesignsCount
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
