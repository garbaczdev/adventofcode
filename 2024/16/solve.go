package main

import (
	"fmt"
	"io"
	"math"
	"os"
	"strings"
	"time"
)

// Extending the vector struct
func (v Vector2D) ToMazeCostTableIndex() int {
    if v.Equals(Vector2D{X: 0, Y: -1}) {
        return 0
    }
    if v.Equals(Vector2D{X: 1, Y: 0}) {
        return 1
    }
    if v.Equals(Vector2D{X: 0, Y: 1}) {
        return 2
    }
    if v.Equals(Vector2D{X: -1, Y: 0}) {
        return 3
    }
    panic("Invalid direction")
}


type Reindeer struct {
    Position Vector2D
    Direction Vector2D
}

func (r Reindeer) Move() Reindeer {
    r.Position = r.Position.Add(r.Direction)
    return r
}

func (r Reindeer) GetTile(maze [][]byte) byte {
    return maze[r.Position.Y][r.Position.X]
}

func (r Reindeer) RotateClockwise() Reindeer {
    r.Direction = r.Direction.RotateClockwise()
    return r
}

func (r Reindeer) RotateCounterClockwise() Reindeer {
    r.Direction = r.Direction.RotateCounterClockwise()
    return r
}


type MazeCostTable [][][4]int

func (m MazeCostTable) GetCost(r Reindeer) int {
    return m[r.Position.Y][r.Position.X][r.Direction.ToMazeCostTableIndex()]
}

func (m MazeCostTable) UpdateCost(r Reindeer, newCost int) {
    m[r.Position.Y][r.Position.X][r.Direction.ToMazeCostTableIndex()] = newCost
}

func NewMazeCostTable(maze [][]byte) MazeCostTable {
    mazeCostTable := make([][][4]int, 0, len(maze))
    for _, mazeRow := range maze {
        mazeRowCostTable := make([][4]int, 0, len(mazeCostTable))
        for range mazeRow {
            var mazeTileCostTable [4]int
            for i := range 4 {
                mazeTileCostTable[i] = math.MaxInt
            }
            mazeRowCostTable = append(mazeRowCostTable, mazeTileCostTable)
        }
        mazeCostTable = append(mazeCostTable, mazeRowCostTable)
    }
    return MazeCostTable(mazeCostTable)
}


func findShortestPathLength(maze [][]byte) int {
    var reindeerPosition Vector2D
    for y, mazeRow := range maze {
        for x, tile := range mazeRow {
            if tile == 'S' {
                reindeerPosition = Vector2D{X: x, Y: y}
            }
        }
    }
    startReindeer := Reindeer{
        Position: reindeerPosition,
        Direction: Vector2D{X: 1, Y: 0},
    }

    mazeCostTable := NewMazeCostTable(maze)

    pq := NewReversePriorityQueue[Reindeer]()
    pq.Push(startReindeer, 0)

    for !pq.Empty() {
        reindeer, cost := pq.Pop()
        // fmt.Println(reindeer, cost)

        // A reindeer with a lower cost has already been here
        if cost >= mazeCostTable.GetCost(reindeer) {
            continue
        }
        mazeCostTable.UpdateCost(reindeer, cost)

        // Arrived at the finish point!
        if reindeer.GetTile(maze) == 'E' {
            return cost
        }
        
        movedReindeer := reindeer.Move()
        clockwiseRotatedReindeer := reindeer.RotateClockwise()
        counterClockwiseRotatedReindeer := reindeer.RotateCounterClockwise()
        
        if movedReindeer.GetTile(maze) != '#' && cost + 1 < mazeCostTable.GetCost(movedReindeer) {
            pq.Push(movedReindeer, cost + 1)
        }
        if clockwiseRotatedReindeer.GetTile(maze) != '#' && cost + 1000 < mazeCostTable.GetCost(clockwiseRotatedReindeer) {
            pq.Push(clockwiseRotatedReindeer, cost + 1000)
        }
        if counterClockwiseRotatedReindeer.GetTile(maze) != '#' && cost + 1000 < mazeCostTable.GetCost(counterClockwiseRotatedReindeer) {
            pq.Push(counterClockwiseRotatedReindeer, cost + 1000)
        }
    }
    
    panic("No path to finish")
}


func parseInput(input string) [][]byte {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")

    maze := make([][]byte, 0, len(lines))
    for _, line := range lines {
        maze = append(maze, []byte(line))
    }

    return maze
}


func printMaze(maze [][]byte) {
    for _, mazeRow := range maze {
        for _, tile := range mazeRow {
            fmt.Print(string(tile))
        }
        fmt.Print("\n")
    }
    fmt.Print("\n")
}


func part1(input string) int {
    maze := parseInput(input)
    return findShortestPathLength(maze)
}


func part2(input string) int {
    return 0
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
