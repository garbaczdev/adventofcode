// package main

// import (
// 	"fmt"
// 	"io"
// 	"os"
// 	"strconv"
// 	"strings"
// 	"time"
// )


// func parseInput(input string) (map[int][]int, [][]int) {
//     input = strings.Trim(input, "\n")
//     splitInput := strings.Split(input, "\n\n")
//     graphLines := strings.Split(splitInput[0], "\n")
//     updateLines := strings.Split(splitInput[1], "\n")

//     graph := make(map[int][]int)
//     for _, graphLine := range graphLines {
//         splitGraphLine := strings.Split(graphLine, "|")
//         beforePageNum, _ := strconv.Atoi(splitGraphLine[0])
//         afterPageNum, _ := strconv.Atoi(splitGraphLine[1])
        
//         if _, exists := graph[beforePageNum]; exists {
//             graph[beforePageNum] = append(graph[beforePageNum], afterPageNum)
//         } else {
//             graph[beforePageNum] = []int{afterPageNum}
//         }
//     }

//     allUpdates := make([][]int, 0, len(updateLines))
//     for _, updateLine := range updateLines {
//         splitUpdateLine := strings.Split(updateLine, ",")
//         updates := make([]int, 0, len(splitUpdateLine))
//         for _, updateStr := range splitUpdateLine {
//             update, _ := strconv.Atoi(updateStr)
//             updates = append(updates, update)
//         }
//         allUpdates = append(allUpdates, updates)
//     }
    
//     return graph, allUpdates
// }


// func isThereACycle(graph map[int][]int, visitedNodes map[int]bool, currentNode int) bool {
//     fmt.Println(visitedNodes, currentNode)
//     _, isNodeVisited := visitedNodes[currentNode]
//     if isNodeVisited {
//         return true
//     }

//     visitedNodes[currentNode] = true
//     neighbourNodes := graph[currentNode]

//     if len(neighbourNodes) > 0 {
//         for _, neighbourNode := range neighbourNodes {
//             if isThereACycle(graph, visitedNodes, neighbourNode) {
//                 return true
//             }
//         }
//     }
//     delete(visitedNodes, currentNode)

//     return false
// }


// func isDag(graph map[int][]int) bool {
//     for node, _ := range graph {
//         visitedNodes := make(map[int]bool)
//         if isThereACycle(graph, visitedNodes, node) {
//             return false
//         }
//     }
//     return true
// }

// func dfsSearch(graph map[int][]int, visitedNodes map[int]bool, currentNode int) {
//     _, isNodeVisited := visitedNodes[currentNode]
//     if isNodeVisited {
//         return
//     }

//     visitedNodes[currentNode] = true
//     neighbourNodes := graph[currentNode]

//     if len(neighbourNodes) > 0 {
//         for _, neighbourNode := range neighbourNodes {
//             dfsSearch(graph, visitedNodes, neighbourNode)
//         }
//     }
// }


// func isUpdateValid(graph map[int][]int, cachedPagesThatMustBeAfter map[int]map[int]bool, update []int) bool {
//     for pageNumIdx, pageNum := range update {
//         pagesThatMustBeAfter, isCached := cachedPagesThatMustBeAfter[pageNum]
//         if !isCached {
//             pagesThatMustBeAfter = make(map[int]bool)
//             dfsSearch(graph, pagesThatMustBeAfter, pageNum)
//             cachedPagesThatMustBeAfter[pageNum] = pagesThatMustBeAfter
//         }

//         for _, pageBefore := range update[:pageNumIdx] {
//             for pageThatMustBeAfter := range pagesThatMustBeAfter {
//                 if pageBefore == pageThatMustBeAfter {
//                     fmt.Println("NOT VALID:", update, pageNum, pagesThatMustBeAfter)
//                     return false
//                 }
//             }
//         }
//     }
//     return true
// }


// func part1(input string) {
//     graph, allUpdates := parseInput(input)

//     cachedPagesThatMustBeAfter := make(map[int]map[int]bool)
//     middleSum := 0
    
//     for _, update := range allUpdates {
//         if isUpdateValid(graph, cachedPagesThatMustBeAfter, update) {
//             middleSum += update[len(update)/2]
//             fmt.Println("VALID: ", update)
//         }
//     }
//     // fmt.Println(cachedPagesThatMustBeAfter)
//     fmt.Println(middleSum)
// }


// func part2(input string) {
// }


// func getInput() string {
//     inputBytes, err := io.ReadAll(os.Stdin)
//     if err != nil || len(inputBytes) == 0 {
//         panic("No STDIN input is empty")
//     }
//     return string(inputBytes)
// }


// func main() {
//     input := getInput()

//     start := time.Now()
//     part1(input)
//     fmt.Printf("[Part 1] Elapsed time: %v\n", time.Since(start))

//     start = time.Now()
//     part2(input)
//     fmt.Printf("[Part 2] Elapsed time: %v\n", time.Since(start))
// }
