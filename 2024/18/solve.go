package main

import (
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)


const SPACE_SIZE = 71


var ALL_DIRECTIONS []Vector2D = []Vector2D{
    Vector2D{X: 0, Y: -1},
    Vector2D{X: 1, Y: 0},
    Vector2D{X: 0, Y: 1},
    Vector2D{X: -1, Y: 0},
}


// Extending the Vector2D
func (v Vector2D) IsInBounds(array [][]bool) bool {
    if v.Y < 0 || v.Y >= len(array) {
        return false
    }
    if v.X < 0 || v.X >= len(array[v.Y]) {
        return false
    }
    return true
}


func parseInput(input string) []Vector2D {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")

    bytePositions := make([]Vector2D, len(lines))
    for lineIdx, line := range lines {
        lineSplit := strings.Split(line, ",")
        x, _ := strconv.Atoi(lineSplit[0])
        y, _ := strconv.Atoi(lineSplit[1])
        bytePositions[lineIdx] = Vector2D{X: x, Y: y}
    }
    
    return bytePositions
}


func createSpace(spaceSize int, bytePositions []Vector2D) [][]bool {
    space := make([][]bool, 0, spaceSize) 
    for range spaceSize {
        space = append(space, make([]bool, spaceSize))
    }
    
    for _, bytePosition := range bytePositions {
        space[bytePosition.Y][bytePosition.X] = true
    }
    
    return space
}


func createSpaceCostTable(spaceSize int) [][]int {
    spaceCostTable := make([][]int, 0, spaceSize) 
    for range spaceSize {
        spaceCostTableRow := make([]int, spaceSize)
        for x := range spaceCostTableRow {
            spaceCostTableRow[x] = math.MaxInt
        }
        spaceCostTable = append(spaceCostTable, spaceCostTableRow)
    }
    return spaceCostTable
}


func findShortestPath(space [][]bool, startPosition Vector2D, endPosition Vector2D) ([][]int, int) {
    spaceCostTable := createSpaceCostTable(SPACE_SIZE)

    pq := NewReversePriorityQueue[Vector2D]()
    pq.Push(startPosition, 0)
    
    for !pq.Empty() {
        currentPosition, cost := pq.Pop()

        // This position has already been visited with lower costs
        if cost >= spaceCostTable[currentPosition.Y][currentPosition.X] {
            continue
        }
        spaceCostTable[currentPosition.Y][currentPosition.X] = cost

        if currentPosition.Equals(endPosition) {
            break
        }
    
        for _, direction := range ALL_DIRECTIONS {
            newPosition := currentPosition.Add(direction)
            if !newPosition.IsInBounds(space) {
                continue
            }
            if space[newPosition.Y][newPosition.X] {
                continue
            }
            if cost + 1 >= spaceCostTable[newPosition.Y][newPosition.X] {
                continue
            }
            pq.Push(newPosition, cost + 1)
        }

    }
    
    return spaceCostTable, spaceCostTable[endPosition.Y][endPosition.X]
}


func part1(input string) int {
    bytePositions := parseInput(input)
    bytePositions = bytePositions[:1024]

    space := createSpace(SPACE_SIZE, bytePositions)
    _, shortestPathLength := findShortestPath(
        space,
        Vector2D{X: 0, Y: 0},
        Vector2D{X: SPACE_SIZE-1, Y: SPACE_SIZE-1},
    )

    // fmt.Println(bytePositions, space, spaceCostTable)
    return shortestPathLength
}


func hasPath(bytePositions []Vector2D) bool {
    space := createSpace(SPACE_SIZE, bytePositions)
    _, shortestPathLength := findShortestPath(
        space,
        Vector2D{X: 0, Y: 0},
        Vector2D{X: SPACE_SIZE-1, Y: SPACE_SIZE-1},
    )
    return shortestPathLength != math.MaxInt
}


func part2(input string) string {
    bytePositions := parseInput(input)

    index := len(bytePositions) / 2
    jump := len(bytePositions) / 4
    
    for {

        if index < 0 || index > len(bytePositions) {
            panic("The index exceeded the array")
        }

        currentIndexHasPath := hasPath(bytePositions[:index])
        nextIndexHasPath := hasPath(bytePositions[:index+1])
        // fmt.Println(index, jump, currentIndexHasPath, nextIndexHasPath)
        
        if currentIndexHasPath && nextIndexHasPath {
            index += jump
        } else if !currentIndexHasPath && !nextIndexHasPath {
            index -= jump
        } else if currentIndexHasPath && !nextIndexHasPath {
            break
        } else {
            panic("This is impossible!")
        }

        if jump != 1 {
            jump /= 2
        }
    }
    
    faultyByte := bytePositions[index]

    return fmt.Sprintf("%d,%d", faultyByte.X, faultyByte.Y)
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
    fmt.Printf("[Part 2][%v] %s\n", time.Since(start), result2)
}
