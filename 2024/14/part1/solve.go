package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)

type Vector2D struct {
    X int
    Y int
}

func (v Vector2D) Add(vOther Vector2D) Vector2D {
    return Vector2D{X: v.X + vOther.X, Y:v.Y + vOther.Y}
}

func (v Vector2D) Equals(vOther Vector2D) bool {
    return v.X == vOther.X && v.Y == vOther.Y
}

type Robot struct {
    Position Vector2D
    Velocity Vector2D
}

func (r *Robot) Move(mapSize Vector2D) {
    r.Position.X = (r.Position.X + r.Velocity.X + mapSize.X) % mapSize.X
    r.Position.Y = (r.Position.Y + r.Velocity.Y + mapSize.Y) % mapSize.Y
}

func (r *Robot) MoveBack(mapSize Vector2D) {
    r.Position.X = (r.Position.X - r.Velocity.X + mapSize.X) % mapSize.X
    r.Position.Y = (r.Position.Y - r.Velocity.Y + mapSize.Y) % mapSize.Y
}


func parseInput(input string) []Robot {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")
    robots := make([]Robot, 0, len(lines))
    for _, line := range lines {
        lineSplit := strings.Split(line, " ")

        rightPart := strings.ReplaceAll(lineSplit[0], "p=", "")
        rightPartSplit := strings.Split(rightPart, ",")
        positionX, _ := strconv.Atoi(rightPartSplit[0])
        positionY, _ := strconv.Atoi(rightPartSplit[1])

        leftPart := strings.ReplaceAll(lineSplit[1], "v=", "")
        leftPartSplit := strings.Split(leftPart, ",")
        velocityX, _ := strconv.Atoi(leftPartSplit[0])
        velocityY, _ := strconv.Atoi(leftPartSplit[1])

        robots = append(robots, Robot{
            Position: Vector2D{X: positionX, Y: positionY},
            Velocity: Vector2D{X: velocityX, Y: velocityY},
        })
    }
    
    return robots
}


func getRobotsCountMap(robots []Robot, mapSize Vector2D) [][]int {
    robotsCountMap := make([][]int, 0, mapSize.Y)
    for range mapSize.Y {
        robotsCountMap = append(robotsCountMap, make([]int, mapSize.X))
    }
    
    for _, robot := range robots {
        robotsCountMap[robot.Position.Y][robot.Position.X]++
    }
    
    return robotsCountMap
}


func printMap(robots []Robot, mapSize Vector2D) {
    robotsCountMap := getRobotsCountMap(robots, mapSize)
    
    for _, row := range robotsCountMap {
        for _, count := range row {
            if count == 0 {
                fmt.Print(".")
            } else {
                fmt.Print(count)
            }
        }
        fmt.Print("\n")
    }
    fmt.Print("\n")
}


func getSafetyFactor(robots []Robot, mapSize Vector2D) int {
    robotsCountMap := getRobotsCountMap(robots, mapSize)
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

    robots := parseInput(input)
    mapSize := Vector2D{X: 101, Y: 103}

    for range 100 {
        // printMap(robots, mapSize)
        for robotIdx, _ := range robots {
            robots[robotIdx].Move(mapSize)
        }
    }

    // printMap(robots, mapSize)
    return getSafetyFactor(robots, mapSize)
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
}
