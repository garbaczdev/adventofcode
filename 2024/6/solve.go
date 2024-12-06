package main

import (
    "fmt"
    "io"
    "os"
    "strings"
    "time"
)

type Guard struct {
    PositionX int
    PositionY int
    DirectionX int
    DirectionY int
}

type Obstruction struct {
    X int
    Y int
}

func (guard Guard) Equals(otherGuard Guard) bool {
    return guard.PositionX == otherGuard.PositionX &&
        guard.PositionY == otherGuard.PositionY &&
        guard.DirectionX == otherGuard.DirectionX &&
        guard.DirectionY == otherGuard.DirectionY
}

func (guard Guard) GetObstruction() Obstruction {
    return Obstruction{
        X: guard.PositionX + guard.DirectionX,
        Y: guard.PositionY + guard.DirectionY,
    }
}


func parseInput(input string) ([][]byte, Guard) {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")

    puzzleMap := make([][]byte, 0, len(lines))
    for _, line := range lines {
        puzzleMap = append(puzzleMap, []byte(line))
    }

    var guard Guard
    for y, row := range puzzleMap {
        for x, character := range row {
            if character == '^' {
                guard = Guard{
                    PositionX: x,
                    PositionY: y,
                    DirectionX: 0,
                    DirectionY: -1,
                }
                row[x] = '.'
            }
        }
    }
    
    return puzzleMap, guard
}


func isInBounds(puzzleMap [][]byte, x int, y int) bool {
    if y < 0 || y >= len(puzzleMap) {
        return false
    }
    if x < 0 || x >= len(puzzleMap[y]) {
        return false
    }
    return true
}


func part1(input string) {
    puzzleMap, guard := parseInput(input)
    
    puzzleMapBitmask := make([][]bool, 0, len(puzzleMap))
    for _, row := range puzzleMap {
        puzzleMapBitmask = append(puzzleMapBitmask, make([]bool, len(row)))
    }
    
    visitedPositionsCount := 0

    for {
        if !puzzleMapBitmask[guard.PositionY][guard.PositionX] {
            visitedPositionsCount++ 
            puzzleMapBitmask[guard.PositionY][guard.PositionX] = true
        }

        nextX := guard.PositionX + guard.DirectionX
        nextY := guard.PositionY + guard.DirectionY

        // If out of bounds break
        if !isInBounds(puzzleMap, nextX, nextY) {
            break
        }

        if puzzleMap[nextY][nextX] == '.' {
            guard.PositionX = nextX
            guard.PositionY = nextY
        } else {
            guard.DirectionY, guard.DirectionX = guard.DirectionX, -guard.DirectionY
        }
    }
    fmt.Printf("[Part 1] %d\n", visitedPositionsCount)
}


func isGuardStuck(puzzleMap [][]byte, guard Guard) bool {
    pastGuards := make([]Guard, 0, 1000)
    for {
        for _, pastGuard := range pastGuards {
            if pastGuard.Equals(guard) {
                return true
            }
        }
        pastGuards = append(pastGuards, guard)

        nextX := guard.PositionX + guard.DirectionX
        nextY := guard.PositionY + guard.DirectionY

        // If out of bounds break
        if !isInBounds(puzzleMap, nextX, nextY) {
            break
        }

        if puzzleMap[nextY][nextX] == '.' {
            guard.PositionX = nextX
            guard.PositionY = nextY
        } else {
            guard.DirectionY, guard.DirectionX = guard.DirectionX, -guard.DirectionY
        }
    }
    return false
}

func part2(input string) {
    puzzleMap, originalGuard := parseInput(input)
    guard := originalGuard

    // To optimize the number of checked places, I am running a check only
    // on the path of the guard.
    // Additionaly, I am saving which obstructions I have placed to avoid overlaps.
    obstructionPlacedMap := make(map[Obstruction]bool)
    obstructionPlacedMap[guard.GetObstruction()] = true

    possibleObstructionsCount := 0

    for {
        nextX := guard.PositionX + guard.DirectionX
        nextY := guard.PositionY + guard.DirectionY

        // If out of bounds break
        if !isInBounds(puzzleMap, nextX, nextY) {
            break
        }

        if puzzleMap[nextY][nextX] == '.' {
            // Calculate the position of the obstruction
            obstruction := guard.GetObstruction()
            // Has this obstruction been tried already?
            _, obstructionPlaced := obstructionPlacedMap[obstruction]

            if !obstructionPlaced {
                obstructionPlacedMap[obstruction] = true

                // Replace the puzzleMap and run a simulation
                puzzleMap[obstruction.Y][obstruction.X] = '#'
                if isGuardStuck(puzzleMap, originalGuard) {
                    possibleObstructionsCount++
                }
                puzzleMap[obstruction.Y][obstruction.X] = '.'
            }

            guard.PositionX = nextX
            guard.PositionY = nextY
        } else {
            guard.DirectionY, guard.DirectionX = guard.DirectionX, -guard.DirectionY
        }
    }

    guard = originalGuard

    fmt.Printf("[Part 2] %d\n", possibleObstructionsCount)
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
