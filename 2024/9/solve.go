package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)

type File struct {
    Id int
    LocationIndex int
    Size int
}

type FreeSpace struct {
    LocationIndex int
    Size int
}


func parseInput(input string) string {
    return strings.Trim(input, "\n")
}


func getDiskMap(diskMapInput string) []int {
    diskMapLength := 0
    for i := 0; i < len(diskMapInput); i++ {
        size, _ := strconv.Atoi(string(diskMapInput[i]))
        diskMapLength += size
    }
    diskMap := make([]int, diskMapLength)

    currentPos := 0
    for i := 0; i < len(diskMapInput); i++ {
        fileSize, _ := strconv.Atoi(string(diskMapInput[i]))
        
        for j := 0; j < fileSize; j++ {
            if i % 2 == 0 {
                diskMap[currentPos] = i/2
            } else {
                diskMap[currentPos] = -1
            }
            currentPos++
        }
    }
    
    return diskMap
}


func fixDiskMap(diskMap []int) {
    leftIdx := 0
    rightIdx := len(diskMap)-1
    for leftIdx < rightIdx {
        if diskMap[leftIdx] == -1 {
            if diskMap[rightIdx] != -1 {
                diskMap[leftIdx], diskMap[rightIdx] = diskMap[rightIdx], diskMap[leftIdx]
            }
            rightIdx--
        } else {
            leftIdx++
        }
    }
}

func calculateChecksum(diskMap []int) int {
    checksum := 0
    for idx, num := range diskMap {
        if num != -1 {
            checksum += idx*num
        }
    }
    return checksum
}


func part1(input string) int {
    diskMapInput := parseInput(input)
    diskMap := getDiskMap(diskMapInput)

    fixDiskMap(diskMap)

    return calculateChecksum(diskMap)
}


func getFilesAndFreeSpaces(diskMapInput string) ([]File, []FreeSpace) {
    filesLength := 0
    for i := 0; i < len(diskMapInput); i += 2 {
        fileSize, _ := strconv.Atoi(string(diskMapInput[i]))
        filesLength += fileSize
    }

    freeSpacesLength := 0
    for i := 1; i < len(diskMapInput); i += 2 {
        freeSpaceSize, _ := strconv.Atoi(string(diskMapInput[i]))
        freeSpacesLength += freeSpaceSize
    }

    files := make([]File, 0, filesLength)
    freeSpaces := make([]FreeSpace, 0, freeSpacesLength)

    currentPos := 0
    for i := 0; i < len(diskMapInput); i++ {
        size, _ := strconv.Atoi(string(diskMapInput[i]))

        if i % 2 == 0 {
            files = append(files, File{
                Id: i/2,
                LocationIndex: currentPos,
                Size: size,
            })
        } else {
            freeSpaces = append(freeSpaces, FreeSpace{
                LocationIndex: currentPos,
                Size: size,
            })
        }
        
        currentPos += size
    }
    
    return files, freeSpaces
}


func squashFilesIntoFreeSpaces(files []File, freeSpaces []FreeSpace) {
    for i := len(files) - 1; i >= 0; i-- {
        file := &files[i]
        for j := 0; j < len(freeSpaces); j++ {
            freeSpace := &freeSpaces[j]

            // If the freeSpaces are on the right of the file, stop iteration
            if freeSpace.LocationIndex > file.LocationIndex {
                break
            }
            
            // If the freeSpace cannot fit the file, skip it
            if file.Size > freeSpace.Size {
                continue
            }

            // This is a free space for the file
            file.LocationIndex = freeSpace.LocationIndex
            freeSpace.Size -= file.Size
            freeSpace.LocationIndex += file.Size
        }
    }
}


func decodeDiskMapFromFiles(files []File) []int {
    rightmostFile := files[0]
    for _, file := range files {
        if file.LocationIndex > rightmostFile.LocationIndex {
            rightmostFile = file
        }
    }
    
    diskMap := make([]int, rightmostFile.LocationIndex + rightmostFile.Size)
    for i, _ := range diskMap {
        diskMap[i] = -1
    }
    
    for _, file := range files {
        for i := 0; i < file.Size; i++ {
            diskMap[file.LocationIndex + i] = file.Id
        }
    }

    return diskMap
}


func part2(input string) int {
    diskMapInput := parseInput(input)

    files, freeSpaces := getFilesAndFreeSpaces(diskMapInput)

    squashFilesIntoFreeSpaces(files, freeSpaces)

    diskMap := decodeDiskMapFromFiles(files)

    return calculateChecksum(diskMap)
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
