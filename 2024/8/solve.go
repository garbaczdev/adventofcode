package main

import (
    "fmt"
    "io"
    "os"
    "strings"
    "time"
)


type Antenna struct {
    Frequency byte
    X int
    Y int
}

func (antenna Antenna) Equals(otherAntenna Antenna) bool {
    return antenna.Frequency == otherAntenna.Frequency &&
        antenna.X == otherAntenna.X &&
        antenna.Y == otherAntenna.Y
}


func parseInput(input string) []string {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")
    return lines
}


func isInBounds(puzzleMap []string, x int, y int) bool {
    if y < 0 || y >= len(puzzleMap) {
        return false
    }
    if x < 0 || x >= len(puzzleMap[y]) {
        return false
    }
    return true
}


func getAntennaGroups(puzzleMap []string) map[byte][]Antenna {
    antennaGroups := make(map[byte][]Antenna)
    for y, row := range puzzleMap {
        for x, frequencyRune := range row {
            frequency := byte(frequencyRune)
            if frequency != '.' {

                _, antennaGroupExists := antennaGroups[frequency]
                if !antennaGroupExists {
                    antennaGroups[frequency] = make([]Antenna, 0, 1)
                }

                antennaGroups[frequency] = append(antennaGroups[frequency], Antenna{
                    Frequency: frequency,
                    X: x,
                    Y: y,
                })
            }
        }
    }
    return antennaGroups
}


func part1(input string) int {
    puzzleMap := parseInput(input)
    antinodeBitmap := make([][]bool, 0, len(puzzleMap))
    for _, row := range puzzleMap {
        antinodeBitmap = append(antinodeBitmap, make([]bool, len(row)))
    }

    antennaGroups := getAntennaGroups(puzzleMap)
    for _, antennaGroup := range antennaGroups {
        for antenna1Idx, antenna1 := range antennaGroup {
            for antenna2Idx, antenna2 := range antennaGroup {
                if antenna1Idx == antenna2Idx {
                    continue
                }

                x_d := antenna2.X - antenna1.X
                y_d := antenna2.Y - antenna1.Y
                // Overshoot the antenna 2
                x_n1 := antenna2.X + x_d
                y_n1 := antenna2.Y + y_d
                if isInBounds(puzzleMap, x_n1, y_n1) {
                    antinodeBitmap[y_n1][x_n1] = true
                }
                // Overshoot the antenna 1 the other way
                x_n2 := antenna1.X - x_d
                y_n2 := antenna1.Y - y_d
                if isInBounds(puzzleMap, x_n2, y_n2) {
                    antinodeBitmap[y_n2][x_n2] = true
                }
            }
        }
    }

    totalAntinodes := 0
    for _, row := range antinodeBitmap {
        for _, isAntinode := range row {
            if isAntinode {
                totalAntinodes++
            }
        }
    }

    return totalAntinodes
}


func part2(input string) int {
    puzzleMap := parseInput(input)
    antinodeBitmap := make([][]bool, 0, len(puzzleMap))
    for _, row := range puzzleMap {
        antinodeBitmap = append(antinodeBitmap, make([]bool, len(row)))
    }

    antennaGroups := getAntennaGroups(puzzleMap)
    for _, antennaGroup := range antennaGroups {
        for antenna1Idx, antenna1 := range antennaGroup {
            for antenna2Idx, antenna2 := range antennaGroup {
                if antenna1Idx == antenna2Idx {
                    continue
                }

                x_d := antenna2.X - antenna1.X
                y_d := antenna2.Y - antenna1.Y
                
                // Overshoot the antenna 2
                // In the first iteration it will also match the antenna actual positions
                x_n1 := antenna2.X
                y_n1 := antenna2.Y
                for isInBounds(puzzleMap, x_n1, y_n1) {
                    antinodeBitmap[y_n1][x_n1] = true
                    x_n1 += x_d
                    y_n1 += y_d
                }
                // Overshoot the antenna 1
                // In the first iteration it will also match the antenna actual positions
                x_n2 := antenna1.X
                y_n2 := antenna1.Y
                for isInBounds(puzzleMap, x_n2, y_n2) {
                    antinodeBitmap[y_n2][x_n2] = true
                    x_n2 -= x_d
                    y_n2 -= y_d
                }
            }
        }
    }

    totalAntinodes := 0
    for _, row := range antinodeBitmap {
        for _, isAntinode := range row {
            if isAntinode {
                totalAntinodes++
            }
        }
    }

    return totalAntinodes
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
