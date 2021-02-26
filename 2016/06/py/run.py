#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
from functools import reduce


def getColumnRecords(messages: List[str]) -> Dict[int,Dict[str,int]]:
    columnRecords = { i: {} for i in range(len(messages[0]))}
    for message in messages:
        for column, c in enumerate(message):
            if c in columnRecords[column]:
                columnRecords[column][c] += 1
            else:
                columnRecords[column][c] = 1
    return columnRecords


def solve(messages: List[str]) -> Tuple[str,str]:
    columnRecords = getColumnRecords(messages)
    return (
        reduce(lambda soFar, column: soFar + max(columnRecords[column].items(), key=lambda cr: cr[1])[0], range(len(messages[0])), ""), 
        reduce(lambda soFar, column: soFar + min(columnRecords[column].items(), key=lambda cr: cr[1])[0], range(len(messages[0])), "")
    )


def getInput(filePath: str) -> List[str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip() for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()