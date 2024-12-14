package common

import (
    "io"
    "os"
	"strconv"
	"strings"
)

func ParseInput(input string) []Robot {
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

func GetInput() string {
    inputBytes, err := io.ReadAll(os.Stdin)
    if err != nil || len(inputBytes) == 0 {
        panic("No STDIN input is empty")
    }
    return string(inputBytes)
}
