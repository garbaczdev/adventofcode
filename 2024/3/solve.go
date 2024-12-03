package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"regexp"
	"strings"
	"strconv"
    "sort"
)


func part1(input string) {
    regexPattern := `mul\([0-9]+,[0-9]+\)`
    regex := regexp.MustCompile(regexPattern)
    matches := regex.FindAllString(input, -1)

    result := 0
    for _, match := range matches {
        // Leave only the number string with ,
        match = strings.ReplaceAll(match, "mul(", "")
        match = strings.ReplaceAll(match, ")", "")

        // Parse the numbers
        splitMatch := strings.Split(match, ",")
        leftNum, _ := strconv.Atoi(splitMatch[0])
        rightNum, _ := strconv.Atoi(splitMatch[1])

        result += leftNum*rightNum
    }

    fmt.Println(result)
}


func part2(input string) {
    // Add do() to the start of an input because it does that implicitly
    input = "don't()do()" + input

    // Get the matches of mul
    mulRegexPattern := `mul\([0-9]+,[0-9]+\)`
    mulRegex := regexp.MustCompile(mulRegexPattern)
    mulRangeIndicesForMatch := mulRegex.FindAllStringIndex(input, -1)

    // Get the sorted start indices of do matches
    doRegex := regexp.MustCompile(`do\(\)`)
    doRangeIndicesForMatch := doRegex.FindAllStringIndex(input, -1)
    doIdxForMatch := make([]int, len(doRangeIndicesForMatch))
    for doRangeIndicesIdx, doRangeIndices := range doRangeIndicesForMatch {
        doIdxForMatch[doRangeIndicesIdx] = doRangeIndices[0]
    }
    sort.Ints(doIdxForMatch)

    // Get the sorted start indices of dont matches
    dontRegex := regexp.MustCompile(`don\'t\(\)`)
    dontRangeIndicesForMatch := dontRegex.FindAllStringIndex(input, -1)
    dontIdxForMatch := make([]int, len(dontRangeIndicesForMatch))
    for dontRangeIndicesIdx, dontRangeIndices := range dontRangeIndicesForMatch {
        dontIdxForMatch[dontRangeIndicesIdx] = dontRangeIndices[0]
    }
    sort.Ints(dontIdxForMatch)

    // This contains the index of which match was the most recent.
    // With that index you can access the array containing the actual input index
    mostRecentDoMatch := 0
    mostRecentDontMatch := 0

    result := 0
    for _, mulRangeIndices := range mulRangeIndicesForMatch {
        // Unpack the actual match
        mulStartIdx := mulRangeIndices[0]
        mulEndIdx := mulRangeIndices[1]
        
        // Update the location of the most recent do/don't
        for mostRecentDoMatch < len(doIdxForMatch)-1 && doIdxForMatch[mostRecentDoMatch+1] < mulStartIdx {
            mostRecentDoMatch++
        }
        for mostRecentDontMatch < len(dontIdxForMatch)-1 && dontIdxForMatch[mostRecentDontMatch+1] < mulStartIdx {
            mostRecentDontMatch++
        }
        // If dont is more recent than do, continue
        if dontIdxForMatch[mostRecentDontMatch] > doIdxForMatch[mostRecentDoMatch] {
            continue
        }

        mulMatch := input[mulStartIdx:mulEndIdx]
        // Leave only the number string with ,
        mulMatch = strings.ReplaceAll(mulMatch, "mul(", "")
        mulMatch = strings.ReplaceAll(mulMatch, ")", "")

        // Parse the numbers
        splitMatch := strings.Split(mulMatch, ",")
        leftNum, _ := strconv.Atoi(splitMatch[0])
        rightNum, _ := strconv.Atoi(splitMatch[1])

        result += leftNum*rightNum
    }

    fmt.Println(result)
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
