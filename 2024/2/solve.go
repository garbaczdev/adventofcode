package main

import (
    "fmt"
    "io"
    "os"
    "log"
    "strings"
    "strconv"
    // "sort"
)


func parseInput(input string) [][]int {
    // Remove the empty lines
    rawLines := strings.Split(input, "\n")
    lines := make([]string, 0, len(rawLines))
    for _, rawLine := range rawLines {
        if strings.TrimSpace(rawLine) != "" {
            lines = append(lines, rawLine)
        }
    }
    // Parse the reports
    reports := make([][]int, len(lines))
    for lineIdx, line := range lines {
        lineSplit := strings.Split(line, " ")
        reports[lineIdx] = make([]int, len(lineSplit))
        for numIdx, numStr := range lineSplit {
            reports[lineIdx][numIdx], _ = strconv.Atoi(numStr)
        }
    }
    return reports
}


func isReportSafe(report []int) bool {
    // Returns whether the provided report is safe or not

    // Check for the right differences
    for numIdx := 1; numIdx < len(report); numIdx++ {
        diff := report[numIdx] - report[numIdx-1]
        if diff < 0 {
            diff = -diff
        }
        if !(1 <= diff && diff <= 3) {
            return false
        }
    }

    // Check if the reading has the right change pattern based on the
    // first elements
    var isGrowing bool
    if report[1] > report[0] {
        isGrowing = true
    } else {
        isGrowing = false
    }
    for numIdx := 1; numIdx < len(report); numIdx++ {
        diff := report[numIdx] - report[numIdx-1]
        if (diff < 0 && isGrowing) || (diff > 0 && !isGrowing) {
            return false
        }
    }

    return true
}


func part1(input string) {
    reports := parseInput(input)
    safeReportCount := 0
    for _, report := range reports {
        if isReportSafe(report) {
            safeReportCount++
        }
    }
    fmt.Println(safeReportCount)
}


func part2(input string) {
    reports := parseInput(input)
    safeReportCount := 0
    for _, report := range reports {
        isAnyAlteredReportSafe := false
        // Iterate over all combinations of removed readings
        for removedIdx := range report {
            alteredReport := make([]int, 0, len(report)-1)
            alteredReport = append(alteredReport, report[:removedIdx]...)
            alteredReport = append(alteredReport, report[removedIdx+1:]...)
            if isReportSafe(alteredReport) {
                isAnyAlteredReportSafe = true
                break
            }
        }
        if isAnyAlteredReportSafe {
            safeReportCount++
        }
    }
    fmt.Println(safeReportCount)
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
