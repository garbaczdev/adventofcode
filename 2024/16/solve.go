package main

import (
	"fmt"
	"io"
	"math"
	"os"
	"strings"
	"time"
)


var ALL_DIRECTIONS []Vector2D = []Vector2D{
    Vector2D{X: 0, Y: -1},
    Vector2D{X: 1, Y: 0},
    Vector2D{X: 0, Y: 1},
    Vector2D{X: -1, Y: 0},
}


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


type mazeCostTableEntry struct {
    cost int
    from []Reindeer
}

// This is a structure used to keep the shortest path to (position, direction) for dijkstra's algorithm
type MazeCostTable [][][4]mazeCostTableEntry

func (m MazeCostTable) GetCost(r Reindeer) int {
    return m[r.Position.Y][r.Position.X][r.Direction.ToMazeCostTableIndex()].cost
}

func (m MazeCostTable) GetEntry(r Reindeer) (int, []Reindeer) {
    cell := &m[r.Position.Y][r.Position.X][r.Direction.ToMazeCostTableIndex()]
    return cell.cost, cell.from
}

func (m MazeCostTable) UpdateCost(r Reindeer, previousR Reindeer, newCost int) {
    cell := &m[r.Position.Y][r.Position.X][r.Direction.ToMazeCostTableIndex()]

    if newCost != cell.cost {
        cell.from = make([]Reindeer, 0, 1)
    }

    cell.from = append(cell.from, previousR) 
    cell.cost = newCost
}

func NewMazeCostTable(maze [][]byte) MazeCostTable {
    mazeCostTable := make([][][4]mazeCostTableEntry, 0, len(maze))
    for _, mazeRow := range maze {
        mazeRowCostTable := make([][4]mazeCostTableEntry, 0, len(mazeCostTable))
        for range mazeRow {
            var mazeTileCostTable [4]mazeCostTableEntry
            for i := range 4 {
                mazeTileCostTable[i].cost = math.MaxInt
            }
            mazeRowCostTable = append(mazeRowCostTable, mazeTileCostTable)
        }
        mazeCostTable = append(mazeCostTable, mazeRowCostTable)
    }
    return MazeCostTable(mazeCostTable)
}


// Used as a structure kept in the priority queue
type priorityQueueReindeerEntry struct {
    PreviousReindeer Reindeer
    Reindeer Reindeer
}


func findShortestPathLength(maze [][]byte) (int, MazeCostTable) {
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

    pq := NewReversePriorityQueue[priorityQueueReindeerEntry]()
    pq.Push(priorityQueueReindeerEntry{Reindeer: startReindeer, PreviousReindeer: startReindeer}, 0)

    pathFound := false
    minPathCost := math.MaxInt

    for !pq.Empty() {
        pqEntry, cost := pq.Pop()
        reindeer := pqEntry.Reindeer

        // A reindeer with a lower cost has already been here
        if cost > mazeCostTable.GetCost(reindeer) {
            // The cost has been exceeded and the minpath has been found, so stop the algorithm
            if pathFound {
                break
            }
            continue
        }
        mazeCostTable.UpdateCost(reindeer, pqEntry.PreviousReindeer, cost)

        // Arrived at the finish point!
        if reindeer.GetTile(maze) == 'E' {
            pathFound = true
            minPathCost = cost
            continue
        }
        
        movedReindeer := reindeer.Move()
        clockwiseRotatedReindeer := reindeer.RotateClockwise()
        counterClockwiseRotatedReindeer := reindeer.RotateCounterClockwise()
        
        if movedReindeer.GetTile(maze) != '#' && cost + 1 < mazeCostTable.GetCost(movedReindeer) {
            pq.Push(priorityQueueReindeerEntry{Reindeer: movedReindeer, PreviousReindeer: reindeer}, cost + 1)
        }
        if clockwiseRotatedReindeer.GetTile(maze) != '#' && cost + 1000 < mazeCostTable.GetCost(clockwiseRotatedReindeer) {
            pq.Push(priorityQueueReindeerEntry{Reindeer: clockwiseRotatedReindeer, PreviousReindeer: reindeer}, cost + 1000)
        }
        if counterClockwiseRotatedReindeer.GetTile(maze) != '#' && cost + 1000 < mazeCostTable.GetCost(counterClockwiseRotatedReindeer) {
            pq.Push(priorityQueueReindeerEntry{Reindeer: counterClockwiseRotatedReindeer, PreviousReindeer: reindeer}, cost + 1000)
        }
    }
    
    return minPathCost, mazeCostTable
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
    minCost, _ := findShortestPathLength(maze)
    return minCost
}


func backtrackMaze(maze [][]byte, mazeCostTable MazeCostTable, mazeBitmap MazeCostTable, reindeer Reindeer) {
    // Mark the position as visited
    if mazeBitmap.GetCost(reindeer) == 0 || reindeer.GetTile(maze) == 'S' {
        return
    }
    mazeBitmap.UpdateCost(reindeer, reindeer , 0)

    _, previousReindeers := mazeCostTable.GetEntry(reindeer)
    for _, previousReindeer := range previousReindeers {
        backtrackMaze(maze, mazeCostTable, mazeBitmap, previousReindeer)
    }
}


func getNumberOfTilesOnMinPaths(maze [][]byte, mazeCostTable MazeCostTable) int {
    // Find end position
    var endPosition Vector2D
    for y, mazeRow := range maze {
        for x, tile := range mazeRow {
            if tile == 'E' {
                endPosition = Vector2D{X: x, Y: y}
            }
        }
    }
    // Create bitmap for visited tiles
    mazeBitmap := NewMazeCostTable(maze)

    minCost := math.MaxInt
    for _, direction := range ALL_DIRECTIONS {
        cost := mazeCostTable.GetCost(Reindeer{Position: endPosition, Direction: direction})
        if cost < minCost {
            minCost = cost
        }
    }

    for _, direction := range ALL_DIRECTIONS {
        cost, previousReindeers := mazeCostTable.GetEntry(Reindeer{Position: endPosition, Direction: direction})
        if cost != minCost {
            continue
        }
        for _, previousReindeer := range previousReindeers {
            backtrackMaze(maze, mazeCostTable, mazeBitmap, previousReindeer)
        }
    }

    // Includes start and end
    visitedTilesCount := 2
    for y, mazeRow := range maze {
        for x, tile := range mazeRow {
            isTileVisited := false
            for _, direction := range ALL_DIRECTIONS {
                if mazeBitmap.GetCost(Reindeer{Position: Vector2D{X: x, Y: y}, Direction: direction}) == 0 {
                    isTileVisited = true
                    break
                }
            }
            
            if isTileVisited {
                visitedTilesCount++
                fmt.Print("O")
            } else {
                fmt.Print(string(tile))
            }
        }
        fmt.Print("\n")
    }

    return visitedTilesCount
}


func part2(input string) int {
    maze := parseInput(input)
    _, mazeCostTable := findShortestPathLength(maze)
    return getNumberOfTilesOnMinPaths(maze, mazeCostTable)
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
