package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)


func parseInput(input string) []int {
    input = strings.Trim(input, "\n")

    stonesStr := strings.Split(input, " ")
    stones := make([]int, 0, len(stonesStr))

    for _, stoneStr := range stonesStr {
        stone, _ := strconv.Atoi(stoneStr)
        stones = append(stones, stone)
    }

    return stones
}


func getMagnitude(num int) int {
    magnitude := 1
    currentPower := 10
    for currentPower <= num {
        currentPower *= 10
        magnitude++
    }

    return magnitude
}


func blinkStone(stone int) []int {
    resultStones := make([]int, 0)
    if stone == 0 {
        resultStones = append(resultStones, 1)
    } else {
        stoneMagnitude := getMagnitude(stone)
        if stoneMagnitude % 2 == 0 {
            split := 1
            for range stoneMagnitude / 2 {
                split *= 10
            }
            resultStones = append(resultStones, stone / split)
            resultStones = append(resultStones, stone % split)
        } else {
            resultStones = append(resultStones, stone*2024)
        }
    }
    
    return resultStones
}


func blink(stones []int) []int {
    evenStonesCount := 0
    for _, stone := range stones {
        if getMagnitude(stone) % 2 == 0 {
            evenStonesCount++
        }
    }

    newStones := make([]int, 0, len(stones) + evenStonesCount)

    for _, stone := range stones {
        newStones = append(newStones, blinkStone(stone)...)
    }

    return newStones
}


func part1(input string) int {
    stones := parseInput(input)
    for range 25 {
        stones = blink(stones)
    }
    return len(stones)
}


func blink2(countByStone map[int]int) map[int]int {
    newCountByStone := make(map[int]int)

    for stone, count := range countByStone {
        resultStones := blinkStone(stone)
        for _, resultStone := range resultStones {
            _, isStoneCounted := newCountByStone[resultStone]
            if isStoneCounted {
                newCountByStone[resultStone] += count
            } else {
                newCountByStone[resultStone] = count
            }
        }
    }

    return newCountByStone
}


func part2(input string) int {
    // Previous part worked on arrays as I have assumed that part2 will require remembering about
    // the order of the stones.
    // As it turns out, the order of the stones does not matter so I can just keep the count of how many 
    // stones of each number I have in an iteration and blink all of them at once, instead of allocating
    // an array that keeps their order.

    stones := parseInput(input)

    countByStone := make(map[int]int)
    for _, stone := range stones {
        _, isStoneCounted := countByStone[stone]
        if isStoneCounted {
            countByStone[stone]++
        } else {
            countByStone[stone] = 1
        }
    }

    for range 75 {
        countByStone = blink2(countByStone)
    }
    
    totalStonesCount := 0
    for _, count := range countByStone {
        totalStonesCount += count
    }
    return totalStonesCount
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
