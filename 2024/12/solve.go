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

func (v Vector2D) RotateClockwise() Vector2D {
    return Vector2D{X: -v.Y, Y:v.X}
}

func (v Vector2D) RotateCounterClockwise() Vector2D {
    return Vector2D{X: v.Y, Y:-v.X}
}

func (v Vector2D) IsInBounds(cropMap []string) bool {
    if v.Y < 0 || v.Y >= len(cropMap) {
        return false
    }
    if v.X < 0 || v.X >= len(cropMap[v.Y]) {
        return false
    }
    return true
}

func (v Vector2D) GetCrop(cropMap []string) byte {
    return cropMap[v.Y][v.X]
}

func (v Vector2D) isWall(cropMap []string, direction Vector2D) bool {
    nextPoint := v.Add(direction)
    if nextPoint.IsInBounds(cropMap) && nextPoint.GetCrop(cropMap) == v.GetCrop(cropMap) {
        return false
    } else {
        return true
    }
}


type PerimeterWall struct {
    Location Vector2D
    Direction Vector2D
}

func (w PerimeterWall) Equals(wOther PerimeterWall) bool {
    return w.Location.Equals(wOther.Location) && w.Direction.Equals(wOther.Direction)
}


func parseInput(input string) []string {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")
    return lines
}


func abs(num int) int {
    if num < 0 {
        num = -num
    }
    return num
}


func getBitmap(map2d []string) [][]bool {
    bitMap := make([][]bool, 0, len(map2d))
    for _, map2dRow := range map2d {
        bitMap = append(bitMap, make([]bool, len(map2dRow)))
    }
    return bitMap
}


func traverseArea(cropMap []string, cropMapVisited [][]bool, point Vector2D) (area int, perimeter int) {
    area = 0
    perimeter = 0

    if cropMapVisited[point.Y][point.X] {
        return
    }
    cropMapVisited[point.Y][point.X] = true

    area = 1
    crop := point.GetCrop(cropMap)

    for yDirection := -1; yDirection <= 1; yDirection++ {
        for xDirection := -1; xDirection <= 1; xDirection++ {
            if abs(yDirection) + abs(xDirection) != 1 {
                continue
            }
                
            pointNew := point.Add(Vector2D{X: xDirection, Y: yDirection})

            if !pointNew.IsInBounds(cropMap) || pointNew.GetCrop(cropMap) != crop {
                perimeter += 1
                continue
            }
            
            recursiveArea, recursivePerimeter := traverseArea(cropMap, cropMapVisited, pointNew)
            area += recursiveArea
            perimeter += recursivePerimeter
        }
    }

    return
}


func part1(input string) int {
    cropMap := parseInput(input)

    cropMapVisited := getBitmap(cropMap)

    price := 0
    for y, cropMapRow := range cropMap {
        for x, _ := range cropMapRow {
            area, perimeter := traverseArea(cropMap, cropMapVisited, Vector2D{X: x, Y: y})
            price += area*perimeter
       }
    }

    return price
}


func traversePerimeter(cropMap []string, traversedWalls map[PerimeterWall]bool, wallStart PerimeterWall) (numberOfSides int) {
    numberOfSides = 0 
    
    wall := wallStart
    point := wallStart.Location
    direction := wallStart.Direction
    crop := point.GetCrop(cropMap)

    for {
        traversedWalls[wall] = true

        directionRotatedClockwise := direction.RotateClockwise()
        pointNextInRow := point.Add(directionRotatedClockwise)

        if pointNextInRow.IsInBounds(cropMap) && pointNextInRow.GetCrop(cropMap) == crop {
            pointDiagonal := pointNextInRow.Add(direction)

            if pointDiagonal.IsInBounds(cropMap) && pointDiagonal.GetCrop(cropMap) == crop {
                direction = direction.RotateCounterClockwise()
                point = pointDiagonal
                numberOfSides++
            } else {
                point = pointNextInRow
            }
        } else {
            direction = directionRotatedClockwise
            numberOfSides++
        }
        
        wall = PerimeterWall{Location: point, Direction: direction}
        // If it is in the starting position
        if wall.Equals(wallStart) {
            break
        }
    }

    return
}


func getNumberOfSides(cropMap []string, point Vector2D) (numberOfSides int) {
    numberOfSides = 0

    directionUp := Vector2D{X: 0, Y: -1}

    cropMapVisited := getBitmap(cropMap)
    traverseArea(cropMap, cropMapVisited, point)

    traversedWalls := make(map[PerimeterWall]bool)

    for y, cropMapRow := range cropMap {
        for x, _ := range cropMapRow {
            // Not part of the current cropfield
            if !cropMapVisited[y][x] {
                continue
            }

            pointCurrent := Vector2D{X: x, Y: y}
            // Not a wall
            if !pointCurrent.isWall(cropMap, directionUp) {
                continue
            }
            
            wallCurrent := PerimeterWall{Location: pointCurrent, Direction: directionUp}
            _, hasWallBeenVisited := traversedWalls[wallCurrent]
            // Already traversed
            if hasWallBeenVisited {
                continue
            }

            numberOfSides += traversePerimeter(cropMap, traversedWalls, wallCurrent)
        }
    }

    return
}


func part2(input string) int {
    cropMap := parseInput(input)

    cropMapVisited := getBitmap(cropMap)

    price := 0
    for y, cropMapRow := range cropMap {
        for x, _ := range cropMapRow {
            if !cropMapVisited[y][x] {
                point := Vector2D{X: x, Y: y}
                numberOfSides := getNumberOfSides(cropMap, point)
                area, _ := traverseArea(cropMap, cropMapVisited, point)
                price += area*numberOfSides
            }
        }
    }

    return price
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
