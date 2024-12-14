package common

import (
	"fmt"
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


func GetRobotsCountMap(robots []Robot, mapSize Vector2D) [][]int {
    robotsCountMap := make([][]int, 0, mapSize.Y)
    for range mapSize.Y {
        robotsCountMap = append(robotsCountMap, make([]int, mapSize.X))
    }
    
    for _, robot := range robots {
        robotsCountMap[robot.Position.Y][robot.Position.X]++
    }
    
    return robotsCountMap
}

func PrintMap(robots []Robot, mapSize Vector2D) {
    robotsCountMap := GetRobotsCountMap(robots, mapSize)
    
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
