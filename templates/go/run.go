package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func part2(puzzleInput string) int {
	return len(puzzleInput)
}

func part1(puzzleInput string) int {
	return len(puzzleInput)
}

func solve(puzzleInput string) (int, int) {
	return part1(puzzleInput), part2(puzzleInput)
}

func getInput(filePath string) (string, error) {
	contentFileStream, err := ioutil.ReadFile(filePath)
	if err != nil {
		return "", errors.New("Unable to open file")
	} else {
		return string(contentFileStream), nil
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
	fmt.Printf("Time: %.7f\n", float64(duration.Nanoseconds())*1e-9)
}
