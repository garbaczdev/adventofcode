package main

import (
	"fmt"
	"time"
    common "aoc2024-14/common"
)


func GetSafetyFactor(robots []common.Robot, mapSize common.Vector2D) int {
    robotsCountMap := common.GetRobotsCountMap(robots, mapSize)
    quarterSafetyFactors := make([]int, 0, 4)
    
    // Iterate over the quarters
    for _, indices := range [][]int{
        {0, mapSize.X/2, 0, mapSize.Y/2},
        {mapSize.X/2 + 1, mapSize.X, 0, mapSize.Y/2},
        {0, mapSize.X/2, mapSize.Y/2+1, mapSize.Y},
        {mapSize.X/2 + 1, mapSize.X, mapSize.Y/2+1, mapSize.Y},
    } {
        xStart := indices[0]
        xEnd := indices[1]
        yStart := indices[2]
        yEnd := indices[3]
        
        quarterSafetyFactor := 0
        for y := yStart; y < yEnd; y++ {
            for x := xStart; x < xEnd; x++ {
                quarterSafetyFactor += robotsCountMap[y][x]
            }
        }
        
        quarterSafetyFactors = append(quarterSafetyFactors, quarterSafetyFactor)
    }

    safetyFactor := 1
    for _, quarterSafetyFactor := range quarterSafetyFactors {
        safetyFactor *= quarterSafetyFactor
    }
    
    return safetyFactor
}


func part1(input string) int {

    robots := common.ParseInput(input)
    mapSize := common.Vector2D{X: 101, Y: 103}

    for range 100 {
        // printMap(robots, mapSize)
        for robotIdx, _ := range robots {
            robots[robotIdx].Move(mapSize)
        }
    }

    return GetSafetyFactor(robots, mapSize)
}

func main() {
    input := common.GetInput()

    start := time.Now()
    result1 := part1(input)
    fmt.Printf("[Part 1][%v] %d\n", time.Since(start), result1)
}
