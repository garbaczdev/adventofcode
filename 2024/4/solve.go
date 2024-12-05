package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"strings"
)

var XMAS_PATTERNS = [][]string{
    {
        "M.S",
        ".A.",
        "M.S",
    },
    {
        "M.M",
        ".A.",
        "S.S",
    },
    {
        "S.M",
        ".A.",
        "S.M",
    },

    {
        "S.S",
        ".A.",
        "M.M",
    },
}


func parseInput(input string) []string {
    rawLines := strings.Split(input, "\n")
    lines := make([]string, 0, len(rawLines))
    for _, rawLine := range rawLines {
        if strings.TrimSpace(rawLine) != "" {
            lines = append(lines, rawLine)
        }
    }
    return lines
}

func isInBounds(puzzle []string, x int, y int) bool {
    if y < 0 || y >= len(puzzle) {
        return false
    }
    if x < 0 || x >= len(puzzle[y]) {
        return false
    }
    return true
}

func starSearchPosition(puzzle []string, x int, y int, word string) int {
    // Try a pattern search in every possible direction from a given position and
    // return how many directions have a matching word

    matchedWordsCount := 0
    for yDelta := -1; yDelta < 2; yDelta++ {
        for xDelta := -1; xDelta < 2; xDelta++ {

            wordIdx := 0
            wordLength := len(word)
            xNew := x
            yNew := y

            for isInBounds(puzzle, xNew, yNew) && wordIdx < wordLength && puzzle[yNew][xNew] == word[wordIdx] {
                wordIdx++
                xNew += xDelta
                yNew += yDelta
            }
            
            if wordIdx == wordLength {
                matchedWordsCount++
            }
        }
    }
    
    return matchedWordsCount
}


func doesPosMatchPattern(puzzle []string, x int, y int, pattern []string) bool {
    for yDelta, patternRow := range pattern {
        for xDelta, patternChar := range patternRow {
            if patternChar == '.' {
                continue
            }
            xNew := x + xDelta
            yNew := y + yDelta
            if !(isInBounds(puzzle, xNew, yNew) && puzzle[yNew][xNew] == byte(patternChar)) {
                return false
            }
        }
    }
    return true
}


func part1(input string) {
    puzzle := parseInput(input)
    totalMatchedWordsCount := 0
    // On each position, run a search into every possible direction for the given pattern.
    for y := range puzzle {
        for x := range puzzle[y] {
            totalMatchedWordsCount += starSearchPosition(puzzle, x, y, "XMAS")
        }
    }
    fmt.Printf("Part1: %d\n", totalMatchedWordsCount)
}


func part2(input string) {
    puzzle := parseInput(input)
    totalMatchedPatterns := 0
    // On each position check for each pattern
    for y := range puzzle {
        for x := range puzzle[y] {
            for _, pattern := range XMAS_PATTERNS {
                if doesPosMatchPattern(puzzle, x, y, pattern) {
                    totalMatchedPatterns += 1
                }
            }
        }
    }
    fmt.Printf("Part1: %d\n", totalMatchedPatterns)
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
