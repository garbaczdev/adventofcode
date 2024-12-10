package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)


func parseInput(input string) [][]int {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")

    topographicMap := make([][]int, 0, len(lines))
    for _, line := range lines {
        row := make([]int, 0, len(line))
        for _, char := range line {
            height, _ := strconv.Atoi(string(char))
            row = append(row, height)
        }
        topographicMap = append(topographicMap, row)
    } 

    return topographicMap
}


func isInBounds(topographicMap [][]int, x int, y int) bool {
    if y < 0 || y >= len(topographicMap) {
        return false
    }
    if x < 0 || x >= len(topographicMap[y]) {
        return false
    }
    return true
}

func abs(num int) int {
    if num < 0 {
        num = -num
    }
    return num
}


func traverseMap(topographicMap [][]int, topographicMapVisited[][] bool, x int, y int) {
    if topographicMapVisited[y][x] {
        return
    }
    
    topographicMapVisited[y][x] = true
    currentHeight := topographicMap[y][x]
    
    for y_d := -1; y_d <= 1; y_d++ {
        for x_d := -1; x_d <= 1; x_d++ {
            // Skips the diagonal directions
            if abs(y_d) + abs(x_d) != 1 {
                continue
            }
            x_n := x + x_d
            y_n := y + y_d
            if !isInBounds(topographicMap, x_n, y_n) {
                continue
            }
            
            nextHeight := topographicMap[y_n][x_n]
            if nextHeight - currentHeight == 1 {
                traverseMap(topographicMap, topographicMapVisited, x_n, y_n)
            }
        }
    }
}


func getTrailheadScore(topographicMap [][]int, trailheadX int, trailheadY int) int {
    // Bitmap of locations that have been visited
    topographicMapVisited := make([][]bool, 0, len(topographicMap))
    for _, row := range topographicMap {
        topographicMapVisited = append(topographicMapVisited, make([]bool, len(row)))
    }

    // Recursively fill the map starting from the trailhead
    traverseMap(topographicMap, topographicMapVisited, trailheadX, trailheadY)
    
    // Count all of the visited 9s
    score := 0
    for y, row := range topographicMap {
        for x, height := range row {
            if height == 9 && topographicMapVisited[y][x] {
                score++
            }
        }
    }

    return score
}


func part1(input string) int {
    topographicMap := parseInput(input)

    totalScore := 0
    for y, row := range topographicMap {
        for x, height := range row {
            if height == 0 {
                totalScore += getTrailheadScore(topographicMap, x, y)
            }
        }
    }

    return totalScore
}

func traverseMap2(topographicMap [][]int, topographicMapTrailsCountCache [][]int, x int, y int) {
    if topographicMapTrailsCountCache[y][x] != -1 {
        return
    }

    if topographicMap[y][x] == 9 {
        topographicMapTrailsCountCache[y][x] = 1
        return
    }
    
    currentHeight := topographicMap[y][x]
    totalTrails := 0

    for y_d := -1; y_d <= 1; y_d++ {
        for x_d := -1; x_d <= 1; x_d++ {
            // Skips the diagonal directions
            if abs(y_d) + abs(x_d) != 1 {
                continue
            }
            x_n := x + x_d
            y_n := y + y_d
            if !isInBounds(topographicMap, x_n, y_n) {
                continue
            }
            
            nextHeight := topographicMap[y_n][x_n]
            if nextHeight - currentHeight == 1 {
                traverseMap2(topographicMap, topographicMapTrailsCountCache, x_n, y_n)
                totalTrails += topographicMapTrailsCountCache[y_n][x_n]
            }
        }
    }
    
    topographicMapTrailsCountCache[y][x] = totalTrails
}


func part2(input string) int {
    topographicMap := parseInput(input)

    topographicMapTrailsCountCache := make([][]int, 0, len(topographicMap))
    for _, row := range topographicMap {
        trailsCountCacheRow := make([]int, 0, len(row))
        for range row {
            trailsCountCacheRow = append(trailsCountCacheRow, -1)
        }
        topographicMapTrailsCountCache = append(topographicMapTrailsCountCache, trailsCountCacheRow)
    }

    totalScore := 0
    for y, row := range topographicMap {
        for x, height := range row {
            if height == 0 {
                traverseMap2(topographicMap, topographicMapTrailsCountCache, x, y)
                totalScore += topographicMapTrailsCountCache[y][x]
            }
        }
    }

    return totalScore
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
