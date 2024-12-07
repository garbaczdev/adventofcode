package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
    "math/big"
)


type Equation struct {
    Total *big.Int
    Factors []big.Int
}


func doesAddUp(equation Equation, currentTotal *big.Int, factorsIdx int) bool {
    if factorsIdx >= len(equation.Factors) {
        return equation.Total.Cmp(currentTotal) == 0
    }

    if currentTotal.Cmp(equation.Total) > 0 {
        return false
    }

    if doesAddUp(equation, new(big.Int).Add(currentTotal, &equation.Factors[factorsIdx]), factorsIdx+1) ||
        doesAddUp(equation, new(big.Int).Mul(currentTotal, &equation.Factors[factorsIdx]), factorsIdx+1) {
        return true
    }

    return false
}

func doesAddUpPart2(equation Equation, currentTotal *big.Int, factorsIdx int) bool {
    // In comparison to the first solution, this one goes backwards!

    nextFactor := &equation.Factors[factorsIdx]
    if factorsIdx == 0 {
        return currentTotal.Cmp(nextFactor) == 0
    }

    // Can be subtracted
    subtractedTotal := new(big.Int).Sub(currentTotal, nextFactor)
    if subtractedTotal.Cmp(big.NewInt(0)) >= 0 {
        if doesAddUpPart2(equation, subtractedTotal, factorsIdx-1) {
            // fmt.Printf(" + %d", nextFactor)
            return true
        }
    }

    // Is divisible
    if new(big.Int).Mod(currentTotal, nextFactor).Cmp(big.NewInt(0)) == 0 {
        if doesAddUpPart2(equation, new(big.Int).Div(currentTotal, nextFactor), factorsIdx-1) {
            // fmt.Printf(" * %d", nextFactor)
            return true
        }
    }
    
    // This gets the magnitude in base 10 - e.g. 123 -> 3 because 10^3 > 123
    nextFactorMagnitude := len(nextFactor.String())
    if len(currentTotal.String()) > nextFactorMagnitude {
        // This gets the rest of the number based on the magnitude - (magnitude 3) e.g. 2123 % 10^3 == 123
        nextFactorModulo := new(big.Int).Exp(big.NewInt(10), big.NewInt(int64(nextFactorMagnitude)), nil)
        remainder := new(big.Int).Mod(currentTotal, nextFactorModulo)
        // Can actually subtract the remainder
        if nextFactor.Cmp(remainder) == 0 {
            totalWithRemovedRemainder := new(big.Int).Div(new(big.Int).Sub(currentTotal, remainder), nextFactorModulo)
            if doesAddUpPart2(equation, totalWithRemovedRemainder, factorsIdx-1) {
                // fmt.Printf(" || %d", nextFactor)
                return true
            }
        }
    }

    return false
}


func (equation Equation) isValid() bool {
    return doesAddUp(equation, big.NewInt(0), 0)
}

func (equation Equation) isValidPart2() bool {
    // fmt.Print(equation.Total.String(), " = ")
    result := doesAddUpPart2(equation, equation.Total, len(equation.Factors)-1)
    // if result {
    //     fmt.Println(" GOOD")
    // } else {
    //     fmt.Println(" BAD")
    // }
    return result
}


func parseInput(input string) []Equation {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")

    equations := make([]Equation, 0, len(lines))
    for _, line := range lines {
        splitLine := strings.Split(line, ": ")

        totalInt, _ := strconv.Atoi(splitLine[0])
        splitFactorsStr := strings.Split(splitLine[1], " ")

        factors := make([]big.Int, 0, len(splitFactorsStr))
        for _, factorStr := range splitFactorsStr {
            factorInt, _ := strconv.Atoi(factorStr)
            factors = append(factors, *big.NewInt(int64(factorInt)))
        }
        
        equations = append(equations, Equation{Total: big.NewInt(int64(totalInt)), Factors: factors})
    }

    return equations
}


func part1(input string) {
    equations := parseInput(input)
    result := big.NewInt(0)

    for _, equation := range equations {
        if equation.isValid() {
            result = new(big.Int).Add(result, equation.Total)
        }
    }
    fmt.Printf("[Part 1] %d\n", result)
}


func part2(input string) {
    equations := parseInput(input)
    result := big.NewInt(0)

    for _, equation := range equations {
        if equation.isValid() || equation.isValidPart2() {
            result = new(big.Int).Add(result, equation.Total)
        }

        // if !equation.isValid() && equation.isValidPart2() {
        //     fmt.Print(equation.Total.String())
        //     for _, factor := range equation.Factors {
        //         fmt.Print(" ")
        //         fmt.Print(factor.String())
        //     }
        //     fmt.Print("\n")
        // }
    }
    fmt.Printf("[Part 2] %d\n", result)
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
    part1(input)
    fmt.Printf("[Part 1] Elapsed time: %v\n", time.Since(start))

    start = time.Now()
    part2(input)
    fmt.Printf("[Part 2] Elapsed time: %v\n", time.Since(start))
}
