package main

import (
    "fmt"
    "io"
    "os"
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
func (v Vector2D) GetTile(warehouseMap [][]byte) byte {
    return warehouseMap[v.Y][v.X]
}


type Robot struct {
    Position Vector2D
}
func (r *Robot) Move(warehouseMap [][]byte, direction Vector2D) {
    nextPosition := r.Position.Add(direction)
    nextTile := nextPosition.GetTile(warehouseMap)

    if nextTile == '#' {
        return
    }
    if nextTile == '.' {
        r.Position = nextPosition
        return
    }
    // Tile is O
    boxLineStartPosition := nextPosition
    for nextPosition.GetTile(warehouseMap) == 'O' {
        nextPosition = nextPosition.Add(direction)
    }
    
    boxLineEndPosition := nextPosition
    boxLineEndTile := boxLineEndPosition.GetTile(warehouseMap)
    if boxLineEndTile == '#' {
        // Nothing happens, the box line is to the wall
        return
    }
    // The box line is ending with a .
    warehouseMap[boxLineStartPosition.Y][boxLineStartPosition.X] = '.'
    warehouseMap[boxLineEndPosition.Y][boxLineEndPosition.X] = 'O'
    r.Position = boxLineStartPosition
}

func canMovePart2(warehouseMap [][]byte, direction Vector2D, position Vector2D) bool {
    tile := position.GetTile(warehouseMap)
    if tile == '.' {
        return true
    }
    if tile == '#' {
        return false
    }

    // Get the box position
    boxLeftEdgePosition := position
    boxRightEdgePosition := position.Add(Vector2D{X: 1, Y: 0})
    if tile == ']' {
        boxLeftEdgePosition = position.Add(Vector2D{X: -1, Y: 0})
        boxRightEdgePosition = position
    }

    if direction.Y == 0 {
        // Horizontal, easy case
        return canMovePart2(warehouseMap, direction, position.Add(direction).Add(direction))
    } else {
        // Vertical move
        return canMovePart2(warehouseMap, direction, boxLeftEdgePosition.Add(direction)) &&
                canMovePart2(warehouseMap, direction, boxRightEdgePosition.Add(direction))
    }
}

func moveRecursivelyPart2(warehouseMap [][]byte, direction Vector2D, position Vector2D) {

    tile := position.GetTile(warehouseMap)
    if tile == '.' {
        // End of recursion
        return
    }
    if tile == '#' {
        panic("The sequence is unmovable")
    }

    // Get the box position
    boxLeftEdgePosition := position
    boxRightEdgePosition := position.Add(Vector2D{X: 1, Y: 0})
    if tile == ']' {
        boxLeftEdgePosition = position.Add(Vector2D{X: -1, Y: 0})
        boxRightEdgePosition = position
    }


    warehouseMap[boxLeftEdgePosition.Y][boxLeftEdgePosition.X] = '.'
    warehouseMap[boxRightEdgePosition.Y][boxRightEdgePosition.X] = '.'

    if direction.Y == 0 {
        // Horizontal, easy case
        moveRecursivelyPart2(warehouseMap, direction, position.Add(direction).Add(direction))
    } else {
        moveRecursivelyPart2(warehouseMap, direction, boxLeftEdgePosition.Add(direction))
        moveRecursivelyPart2(warehouseMap, direction, boxRightEdgePosition.Add(direction))
    }

    boxLeftEdgePosition = boxLeftEdgePosition.Add(direction)
    boxRightEdgePosition = boxRightEdgePosition.Add(direction)
    warehouseMap[boxLeftEdgePosition.Y][boxLeftEdgePosition.X] = '['
    warehouseMap[boxRightEdgePosition.Y][boxRightEdgePosition.X] = ']'

}

func (r *Robot) MovePart2(warehouseMap [][]byte, direction Vector2D) {
    nextPosition := r.Position.Add(direction)
    if canMovePart2(warehouseMap, direction, nextPosition) {
        moveRecursivelyPart2(warehouseMap, direction, nextPosition)
        r.Position = nextPosition
    }
}


func parseInput(input string) (warehouseMap [][]byte, instructions string, robot Robot) {
    input = strings.Trim(input, "\n")
    inputSplit := strings.Split(input, "\n\n")
    
    warehouseMapLines := strings.Split(inputSplit[0], "\n")
    warehouseMap = make([][]byte, len(warehouseMapLines))
    for i, warehouseLine := range warehouseMapLines {
        warehouseMap[i] = []byte(warehouseLine)
    }
    instructions = strings.ReplaceAll(inputSplit[1], "\n", "")
    
    for y, row := range warehouseMap {
        for x, char := range row {
            if char == '@' {
                robot = Robot{Position: Vector2D{X: x, Y: y}}
                warehouseMap[y][x] = '.'
            }
        }
    }

    return warehouseMap, instructions, robot
}

func instructionToDirection(instruction byte) (direction Vector2D) {
    switch instruction {
    case '^':
        direction = Vector2D{X: 0, Y: -1}
    case '>':
        direction = Vector2D{X: 1, Y: 0}
    case 'v':
        direction = Vector2D{X: 0, Y: 1}
    case '<':
        direction = Vector2D{X: -1, Y: 0}
    default:
        panic("Unknown instruction")
    }
    return direction
}

func printWarehouseMap(warehouseMap [][]byte, robot Robot) {
    for y, warehouseMapRow := range warehouseMap {
        for x, tile := range warehouseMapRow {
            if robot.Position.Equals(Vector2D{X: x, Y: y}) {
                fmt.Print("@")
            } else {
                fmt.Print(string(tile))
            }
        } 
        fmt.Print("\n")
    }
    fmt.Print("\n")
}

func sumGpsCoordinates(warehouseMap [][]byte) int {
    gpsCoordinatesSum := 0
    
    for y, warehouseMapRow := range warehouseMap {
        for x, tile := range warehouseMapRow {
            if tile == 'O' || tile == '[' {
                gpsCoordinatesSum += x + y*100
            }
        }
    }
    
    return gpsCoordinatesSum
}


func part1(input string) int {
    warehouseMap, instructions, robot := parseInput(input)
    for _, instruction := range instructions {
        robot.Move(warehouseMap, instructionToDirection(byte(instruction)))
        // printWarehouseMap(warehouseMap, robot)
    }
    return sumGpsCoordinates(warehouseMap)
}


func expandWarehouse(warehouseMap [][]byte) [][]byte {
    expandedWarehouseMap := make([][]byte, len(warehouseMap))
    for y, warehouseMapRow := range warehouseMap {
        expandedWarehouseMap[y] = make([]byte, len(warehouseMapRow)*2)
        for x, tile := range warehouseMapRow {
            if tile == '.' || tile == '#' {
                expandedWarehouseMap[y][x*2] = tile
                expandedWarehouseMap[y][x*2 + 1] = tile
            } else if tile == '@' {
                expandedWarehouseMap[y][x*2] = '@'
                expandedWarehouseMap[y][x*2 + 1] = '.'
            } else if tile == 'O' {
                expandedWarehouseMap[y][x*2] = '['
                expandedWarehouseMap[y][x*2 + 1] = ']'
            } else {
                panic("Unknown instruction")
            }
        }
    }
    
    return expandedWarehouseMap
}


func part2(input string) int {
    warehouseMap, instructions, robot := parseInput(input)
    warehouseMap = expandWarehouse(warehouseMap)
    robot.Position.X *= 2
    
    for _, instruction := range instructions {
        robot.MovePart2(warehouseMap, instructionToDirection(byte(instruction)))
        // printWarehouseMap(warehouseMap, robot)
    }
    return sumGpsCoordinates(warehouseMap)
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
