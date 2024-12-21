package main

import (
	"fmt"
	"io"
	"math"
	"os"
	"strings"
	"time"
)

// Utility functions
func abs(num int) int {
    if num < 0 {
        num = -num
    }
    return num
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

func (v Vector2D) GetTile(gameMap [][]bool) bool {
    return gameMap[v.Y][v.X]
}

func (v Vector2D) GetCost(gameMapCostTable [][]int) int {
    return gameMapCostTable[v.Y][v.X]
}


type Cheat struct {
    From Vector2D
    To Vector2D
    Profit int
}


func parseInput(input string) ([][]bool, Vector2D, Vector2D) {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")

    var startPosition Vector2D
    var endPosition Vector2D
    gameMap := make([][]bool, 0, len(lines))

    for y, line := range lines {
        gameMapRow := make([]bool, len(line))
        for x, tile := range line {
            if tile == '#' {
                gameMapRow[x] = true
            } else if tile == 'S' {
                startPosition = Vector2D{X: x, Y: y}
            } else if tile == 'E' {
                endPosition = Vector2D{X: x, Y: y}
            }
        }
        gameMap = append(gameMap, gameMapRow)
    }
    
    return gameMap, startPosition, endPosition
}


func createGameMapCostTable(gameMap [][]bool) [][]int {
    gameMapCostTable := make([][]int, 0, len(gameMap))
    for _, gameMapRow := range gameMap {
        gameMapCostTableRow := make([]int, len(gameMapRow))
        for x := range gameMapCostTableRow {
            gameMapCostTableRow[x] = math.MaxInt
        }
        gameMapCostTable = append(gameMapCostTable, gameMapCostTableRow)
    }
    return gameMapCostTable
}


func findShortestPath(gameMap [][]bool, startPosition Vector2D, endPosition Vector2D) ([][]int, int) {
    gameMapCostTable := createGameMapCostTable(gameMap)

    pq := NewReversePriorityQueue[Vector2D]()
    pq.Push(startPosition, 0)
    
    for !pq.Empty() {
        currentPosition, cost := pq.Pop()

        // This position has already been visited with lower costs
        if cost >= currentPosition.GetCost(gameMapCostTable) {
            continue
        }
        gameMapCostTable[currentPosition.Y][currentPosition.X] = cost
    
        for y := -1; y < 2; y++ {
            for x := -1; x < 2; x++ {
                direction := Vector2D{X: x, Y: y}
                // Get only the horizontal/vertical directions
                if direction.ManhattanDistance() != 1 {
                    continue
                }
                newPosition := currentPosition.Add(direction)

                if !newPosition.IsInBounds(gameMap) {
                    continue
                }
                if newPosition.GetTile(gameMap) {
                    continue
                }
                if cost + 1 >= newPosition.GetCost(gameMapCostTable) {
                    continue
                }
                pq.Push(newPosition, cost + 1)
            }
        }
    }
    
    return gameMapCostTable, endPosition.GetCost(gameMapCostTable)
}

func findCheatsForPosition(gameMap [][]bool, gameMapCostTable [][]int, position Vector2D, ghostingLength int) []Cheat {

    cost := position.GetCost(gameMapCostTable)
    cheats := make([]Cheat, 0)
    
    for y := -ghostingLength; y < ghostingLength + 1; y++ {
        for x := -ghostingLength; x < ghostingLength + 1; x++ {
            // Get only the horizontal/vertical directions
            direction := Vector2D{X: x, Y: y}
            if 0 < direction.ManhattanDistance() && direction.ManhattanDistance() > ghostingLength {
                continue
            }

            newPosition := position.Add(direction)
            if !newPosition.IsInBounds(gameMap) {
                continue
            }
            if newPosition.GetTile(gameMap) {
                continue
            }

            newCost := newPosition.GetCost(gameMapCostTable)
            if cost + direction.ManhattanDistance() >= newCost {
                continue
            }
            cheats = append(cheats, Cheat{From: position, To: newPosition, Profit: newCost - cost - direction.ManhattanDistance()})
        }
    }

    return cheats
}

func findAllCheats(gameMap [][]bool, startPosition Vector2D, endPosition Vector2D, ghostingLength int) []Cheat {
    gameMapCostTable, _ := findShortestPath(gameMap, startPosition, endPosition)
    cheats := make([]Cheat, 0)

    for y, gameMapRow := range gameMap {
        for x, isWall := range gameMapRow {
            if !isWall {
                cheats = append(cheats, findCheatsForPosition(gameMap, gameMapCostTable, Vector2D{X: x, Y: y}, ghostingLength)...)
            }
        }
    }
    
    return cheats
}


func getNumberOfCheatsWithOver100Profit(cheats []Cheat) int {
    cheatsCountByProfit := make(map[int]int)
    for _, cheat := range cheats {
        _, isCounted := cheatsCountByProfit[cheat.Profit]
        if !isCounted {
            cheatsCountByProfit[cheat.Profit] = 1
        } else {
            cheatsCountByProfit[cheat.Profit]++
        }
    }

    numberOfCheatsWithOver100Profit := 0
    for profit, count := range cheatsCountByProfit {
        if profit >= 100 {
            numberOfCheatsWithOver100Profit += count
        }
    }
    
    return numberOfCheatsWithOver100Profit
}


func part1(input string) int {
    gameMap, startPosition, endPosition := parseInput(input)
    cheats := findAllCheats(gameMap, startPosition, endPosition, 2)
    return getNumberOfCheatsWithOver100Profit(cheats) 
}


func part2(input string) int {
    gameMap, startPosition, endPosition := parseInput(input)
    cheats := findAllCheats(gameMap, startPosition, endPosition, 20)
    return getNumberOfCheatsWithOver100Profit(cheats) 
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
