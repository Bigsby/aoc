package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func part2(directions []int) int {
	currentFloor := 0
	for index, direction := range directions {
		currentFloor += direction
		if currentFloor == -1 {
			return index + 1
		}
	}
	println("Did not go below 0!")
	return 0
}

func part1(directions []int) int {
	total := 0
	for _, direction := range directions {
		total += direction
	}
	return total
}

func solve(directions []int) (int, int) {
	return part1(directions), part2(directions)
}

func getInput(filePath string) ([]int, error) {
	contentFileStream, err := ioutil.ReadFile(filePath)
	var directions []int
	if err != nil {
		return nil, errors.New("Unable to open file")
	} else {

		for _, c := range string(contentFileStream) {
			if c == '(' {
				directions = append(directions, 1)
			} else {
				directions = append(directions, -1)
			}
		}
		return directions, nil
	}
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Please, add input file path as parameter")
		os.Exit(1)
	}
	start := time.Now()
	puzzleInput, err := getInput(os.Args[1])
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	part1Result, part2Result := solve(puzzleInput)
	duration := time.Since(start)
	fmt.Printf("P1: %v\n", part1Result)
	fmt.Printf("P1: %v\n", part2Result)
	fmt.Println()
	fmt.Printf("Time: %.7f\n", float64(duration.Nanoseconds())/1000000000)
}
