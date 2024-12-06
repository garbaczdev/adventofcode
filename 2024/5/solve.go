package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)


func parseInput(input string) (map[int][]int, [][]int) {
    input = strings.Trim(input, "\n")
    splitInput := strings.Split(input, "\n\n")
    graphLines := strings.Split(splitInput[0], "\n")
    updateLines := strings.Split(splitInput[1], "\n")

    graph := make(map[int][]int)
    for _, graphLine := range graphLines {
        splitGraphLine := strings.Split(graphLine, "|")
        beforePageNum, _ := strconv.Atoi(splitGraphLine[0])
        afterPageNum, _ := strconv.Atoi(splitGraphLine[1])
        
        if _, exists := graph[beforePageNum]; exists {
            graph[beforePageNum] = append(graph[beforePageNum], afterPageNum)
        } else {
            graph[beforePageNum] = []int{afterPageNum}
        }
    }

    allUpdates := make([][]int, 0, len(updateLines))
    for _, updateLine := range updateLines {
        splitUpdateLine := strings.Split(updateLine, ",")
        updates := make([]int, 0, len(splitUpdateLine))
        for _, updateStr := range splitUpdateLine {
            update, _ := strconv.Atoi(updateStr)
            updates = append(updates, update)
        }
        allUpdates = append(allUpdates, updates)
    }
    
    return graph, allUpdates
}


func isUpdateValid(graph map[int][]int, update []int) bool {
    for pageNumIdx, pageNum := range update {
        for _, pageBefore := range update[:pageNumIdx] {
            for _, pageThatMustBeAfter := range graph[pageNum] {
                if pageBefore == pageThatMustBeAfter {
                    return false
                }
            }
        }
    }
    return true
}


func part1(input string) {
    graph, allUpdates := parseInput(input)
    middleSum := 0
    for _, update := range allUpdates {
        if isUpdateValid(graph, update) {
            middleSum += update[len(update)/2]
        }
    }
    fmt.Println(middleSum)
}


func findGoodUpdateOrdering(graph map[int][]int, originalUpdate []int, reversedGoodUpdate []int, usedPagesBitmask []bool) bool {

    // If it came to the end and it used all of the numbers, it means it found the right ordering
    if len(originalUpdate) == len(reversedGoodUpdate) {
        return true
    }

    // Check whether you can use all of the remaining numbers with the current ordering.
    // If not, then there is no reason to continue.
    for bitmaskIdx, isPageUsed := range usedPagesBitmask {
        if !isPageUsed {
            unusedPage := originalUpdate[bitmaskIdx]
            for _, usedPage := range reversedGoodUpdate {
                pagesThatMustBeAfter := graph[usedPage] 
                for _, pageThatMustBeAfter := range pagesThatMustBeAfter {
                    if unusedPage == pageThatMustBeAfter {
                        return false
                    }
                }
            }
        }
    }

    // Iterate over unused numbers and recursively try each combination.
    for bitmaskIdx, isPageUsed := range usedPagesBitmask {
        if !isPageUsed {

            // fmt.Println(originalUpdate, reversedGoodUpdate, usedPagesBitmask)
            reversedGoodUpdate = append(reversedGoodUpdate, originalUpdate[bitmaskIdx])
            usedPagesBitmask[bitmaskIdx] = true

            if findGoodUpdateOrdering(graph, originalUpdate, reversedGoodUpdate, usedPagesBitmask) {
                return true
            }

            reversedGoodUpdate = reversedGoodUpdate[:len(reversedGoodUpdate)-1]
            usedPagesBitmask[bitmaskIdx] = false
        }
    }
    
    // No combination worked, return false
    return false
}


func repairUpdate(graph map[int][]int, update []int) []int {
    reversedGoodUpdate := make([]int, len(update))
    usedBitmask := make([]bool, len(update))

    findGoodUpdateOrdering(graph, update, reversedGoodUpdate[:0], usedBitmask)

    // Reverse the array
    for i, j := 0, len(reversedGoodUpdate)-1; i < j; i, j = i+1, j-1 {
        reversedGoodUpdate[i], reversedGoodUpdate[j] = reversedGoodUpdate[j], reversedGoodUpdate[i]
    }
    
    return reversedGoodUpdate
}


func part2(input string) {
    graph, allUpdates := parseInput(input)
    middleSum := 0
    for _, update := range allUpdates {
        if !isUpdateValid(graph, update) {
            repairedUpdate := repairUpdate(graph, update)
            middleSum += repairedUpdate[len(update)/2]
        }
    }
    fmt.Println(middleSum)
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
