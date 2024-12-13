package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func lcm(a, b int) int {
	return abs(a*b) / gcd(a, b)
}


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

func (v Vector2D) Multiply(multiplier int) Vector2D {
    return Vector2D{X: v.X*multiplier, Y: v.Y*multiplier}
}

func (v Vector2D) RateTo(vOther Vector2D) (canBeChanged bool, vCount int, vOtherCount int) {
    canBeChanged = false
    vCount = 0
    vOtherCount = 0

    xLcm := lcm(v.X, vOther.X)
    yLcm := lcm(v.Y, vOther.Y)

    vXRate := xLcm / v.X
    vYRate := yLcm / v.Y
    vOtherXRate := xLcm / vOther.X
    vOtherYRate := yLcm / vOther.Y

    canBeChanged = vXRate == vYRate && vOtherXRate == vOtherYRate
    if canBeChanged {
        vCount = vXRate
        vOtherCount = vOtherXRate
    }

    return
}


type Machine struct {
    ButtonA Vector2D
    ButtonB Vector2D
    PrizePosition Vector2D
}

func (m Machine) GetButtonClicks() (willReach bool, buttonAClicks int, buttonBClicks int) {
    crossProduct := m.ButtonA.X*m.ButtonB.Y - m.ButtonA.Y*m.ButtonB.X
    if crossProduct != 0 {
        // The vectors are on the same line
        // AV + BW = P
        // -------
        // AVx + BWx = Px
        // AVy + BWy = Py
        // -------
        // A = (Px - BWx) / Vx
        // A = (Py - BWy) / Vy
        // -------
        // (Px - BWx)*Vy = (Py - BWy)*Vx
        // VyPx - VyBWx = VxPy - VxBWy
        // B(VxWy - VyWx) = VxPy - VyPx
        // B = (VxPy - VyPx)/(VxWy - VyWx)
        // If the vectors are not on the same line, there is only 1 solution
        buttonBClicks = (m.ButtonA.X*m.PrizePosition.Y - m.ButtonA.Y*m.PrizePosition.X) / crossProduct
        buttonAClicks = (m.PrizePosition.X - buttonBClicks*m.ButtonB.X) / m.ButtonA.X
        
        // Check whether the prize is reachable with the current combination.
        // If it is not, it will not be reachable with minimized combination
        componentA := Vector2D{X: m.ButtonA.X*buttonAClicks, Y: m.ButtonA.Y*buttonAClicks}
        componentB := Vector2D{X: m.ButtonB.X*buttonBClicks, Y: m.ButtonB.Y*buttonBClicks}

        willReach = componentA.Add(componentB).Equals(m.PrizePosition)
        if !willReach {
            buttonAClicks = 0
            buttonBClicks = 0
        }
    }

    return
}


func (m Machine) GetButtonClicksBruteForce() (willReach bool, buttonAClicks int, buttonBClicks int) {
    // MAX_INT
    minPrice := int(^uint(0) >> 1)
    for a := 0; a <= 100; a++ {
        for b := 0; b <= 100; b++ {
            if m.ButtonA.Multiply(a).Add(m.ButtonB.Multiply(b)).Equals(m.PrizePosition) {
                willReach = true
                price := a*3 + b
                if price < minPrice {
                    buttonAClicks = a
                    buttonBClicks = b
                    minPrice = price
                }
            }
        }
    }
    
    return
}


func parseButtonLine(buttonLine string) Vector2D {
    rightPart := strings.Split(buttonLine, ": ")[1]
    rightPart = strings.ReplaceAll(rightPart, " ", "")
    rightPart = strings.ReplaceAll(rightPart, "X+", "")
    rightPart = strings.ReplaceAll(rightPart, "Y+", "")
    rightPartSplit := strings.Split(rightPart, ",")

    x, _ := strconv.Atoi(rightPartSplit[0])
    y, _ := strconv.Atoi(rightPartSplit[1])

    return Vector2D{X: x, Y: y}
}


func parsePrizeLine(buttonLine string) Vector2D {
    rightPart := strings.Split(buttonLine, ": ")[1]
    rightPart = strings.ReplaceAll(rightPart, " ", "")
    rightPart = strings.ReplaceAll(rightPart, "X=", "")
    rightPart = strings.ReplaceAll(rightPart, "Y=", "")
    rightPartSplit := strings.Split(rightPart, ",")

    x, _ := strconv.Atoi(rightPartSplit[0])
    y, _ := strconv.Atoi(rightPartSplit[1])

    return Vector2D{X: x, Y: y}
}

func parseInput(input string) []Machine {
    input = strings.Trim(input, "\n")
    machinesStr := strings.Split(input, "\n\n")
    machines := make([]Machine, 0, len(machinesStr))

    for _, machineStr := range machinesStr {
        machineLines := strings.Split(strings.Trim(machineStr, "\n"), "\n")
        machines = append(machines, Machine{
            ButtonA: parseButtonLine(machineLines[0]),
            ButtonB: parseButtonLine(machineLines[1]),
            PrizePosition: parsePrizeLine(machineLines[2]),
        }) 
    }

    return machines
}


func part1(input string) int {
    machines := parseInput(input)
    price := 0
    for _, machine := range machines {
        willReach, buttonAClicks, buttonBClicks := machine.GetButtonClicksBruteForce()
        if willReach {
            price += buttonAClicks*3 + buttonBClicks
        }
    }
    return price
}


func part2(input string) int {
    machines := parseInput(input)
    price := 0
    for _, machine := range machines {
        machine.PrizePosition = machine.PrizePosition.Add(Vector2D{X: 10000000000000, Y: 10000000000000})
        willReach, buttonAClicks, buttonBClicks := machine.GetButtonClicks()
        if willReach {
            price += buttonAClicks*3 + buttonBClicks
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
