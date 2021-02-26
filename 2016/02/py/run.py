#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple


DIRECTIONS: Dict[str,complex] = {
    "U": -1j,
    "D":  1j,
    "L": -1,
    "R":  1
}
def getButtonForPath(position: complex, path: str, keypad: Dict[complex,str]) -> Tuple[complex,str]:
    for move in path:
        newPosition = position + DIRECTIONS[move]
        if newPosition in keypad:
            position = newPosition
    return position, keypad[position]


def getCode(paths: List[str], keypad: Dict[complex,str]) -> str:
    position = 0
    code = []
    for path in paths:
        position, digit = getButtonForPath(position, path, keypad)
        code.append(digit)
    return "".join(code)


KEYPAD1: Dict[complex,str] = {
    -1 - 1j: "1", -1j: "2",  1 - 1j: "3",
    -1     : "4",   0: "5",  1     : "6",
    -1 + 1j: "7",  1j: "8",  1 + 1j: "9"
}


KEYPAD2: Dict[complex,str] = {
                            -2j: "1",
              -1 - 1j: "2", -1j: "3", 1 - 1j: "4",
    -2: "5",  -1     : "6",   0: "7", 1     : "8", 2: "9",
              -1 + 1j: "A",  1j: "B", 1 + 1j: "C",
                             2j: "D"
}


def solve(paths: List[str]) -> Tuple[str,str]:
    return (
        getCode(paths, KEYPAD1), 
        getCode(paths, KEYPAD2)
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