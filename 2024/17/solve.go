package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)


func reverseArray[T any](array []T) []T {
    reversedArray := make([]T, len(array))
    for i, _ := range array {
        reversedArray[i] = array[len(array) - 1 - i]
    }
    return reversedArray
}


type Computer struct {
    RegA int
    RegB int
    RegC int
    Instructions []int
    InstructionPointer int
    Output []int
}

func (c *Computer) getComboOperandValue(operand int) int {
    if 0 <= operand && operand <= 3 {
        return operand
    }
    if operand == 4 {
        return c.RegA
    }
    if operand == 5 {
        return c.RegB
    }
    if operand == 6 {
        return c.RegC
    }
    panic("Unknown operand")
}

func (c *Computer) ExecuteInstruction(opcode int, operand int) {
    switch opcode {
    case 0:
        c.RegA = c.RegA >> c.getComboOperandValue(operand)
    case 1:
        c.RegB = c.RegB ^ operand
    case 2:
        c.RegB = c.getComboOperandValue(operand) % 8
    case 3:
        if c.RegA != 0 {
            c.InstructionPointer = operand
            return
        }
    case 4:
        c.RegB = c.RegB ^ c.RegC
    case 5:
        c.Output = append(c.Output, c.getComboOperandValue(operand) % 8)
    case 6:
        c.RegB = c.RegA >> c.getComboOperandValue(operand)
    case 7:
        c.RegC = c.RegA >> c.getComboOperandValue(operand)
    } 
    c.InstructionPointer += 2
}

func (c *Computer) ExecuteInstructions() {
    for 0 <= c.InstructionPointer && c.InstructionPointer < len(c.Instructions) {
        c.ExecuteInstruction(c.Instructions[c.InstructionPointer], c.Instructions[c.InstructionPointer + 1])
    }
}


func parseRegisterValue(registerLine string) int {
    registerLineSplit := strings.Split(registerLine, ": ")
    registerValue, _ := strconv.Atoi(registerLineSplit[1])
    return registerValue
}


func parseInput(input string) (Computer, []int) {
    input = strings.Trim(input, "\n")
    lines := strings.Split(input, "\n")

    computer := Computer{
        RegA: parseRegisterValue(lines[0]),
        RegB: parseRegisterValue(lines[1]),
        RegC: parseRegisterValue(lines[2]),
    } 
    
    instructionLineSplit := strings.Split(lines[len(lines) - 1], ": ")
    instructionsStr := strings.Split(instructionLineSplit[1], ",")
    instructions := make([]int, 0, len(instructionsStr))
    for _, instructionStr := range instructionsStr {
        instruction, _ := strconv.Atoi(instructionStr)
        instructions = append(instructions, instruction)
    }
    
    return computer, instructions
}


func part1(input string) string {
    computer, instructions := parseInput(input)

    computer.Instructions = instructions
    computer.ExecuteInstructions()

    outputStr := ""
    for _, outputNumber := range computer.Output {
        outputStr += strconv.Itoa(outputNumber)
        outputStr += ","
    }
    outputStr = outputStr[:len(outputStr) - 1]

    return outputStr
}


func getRegisterAValue(reversedInstructions []int, regA int) int {
    // I have reverse engineered my input program to come up with a recursive 
    // bruteforce of possible register A's based on bit operations.
    //
    // while A != 0:
    //     // 2,4
    //     B = A % 8
    //     // 1,5 
    //     B = B ^ 5
    //     // 7,5
    //     C = A >> B
    //     // 0,3
    //     A = A >> 3
    //     // 4,0
    //     B = B ^ C
    //     // 1,6
    //     B = B ^ 6
    //     // 5,5
    //     print(B % 8)
    //
    // OUTPUT:
    // 2415750340165530
    // A = 48 bit number
    //
    // Formula:
    // B ^ C = instruction ^ 6
    // A ^ 5 ^ (Af >> A^5) = instrution ^ 6
    // A ^ (Af >> A^5) = instruction ^ 6 ^ 5
    // A ^ (Af >> A^5) = instruction ^ 3

    if len(reversedInstructions) == 0 {
        return regA
    }
    instruction := reversedInstructions[0]

    for possibleA := range 8 {
        newRegA := regA << 3
        newRegA += possibleA
        if possibleA ^ ((newRegA >> (possibleA ^ 5)) % 8) == instruction ^ 3 {
            recursiveRegA := getRegisterAValue(reversedInstructions[1:], newRegA)
            if recursiveRegA != -1 {
                return recursiveRegA
            }
        }
    }

    return -1
    // return regA
}


func part2(input string) int {
    computer, instructions := parseInput(input)

    reversedInstructions := reverseArray(instructions)
    regA := getRegisterAValue(reversedInstructions, 0)
    if regA == -1 {
        panic("RegA == -1")
    }

    computer.Instructions = instructions
    computer.RegA = regA
    computer.ExecuteInstructions()

    outputStr := ""
    for _, outputNumber := range computer.Output {
        outputStr += strconv.Itoa(outputNumber)
        outputStr += ","
    }
    outputStr = outputStr[:len(outputStr) - 1]
    fmt.Println(outputStr)

    return regA
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
    fmt.Printf("[Part 1][%v] %s\n", time.Since(start), result1)

    start = time.Now()
    result2 := part2(input)
    fmt.Printf("[Part 2][%v] %d\n", time.Since(start), result2)
}
