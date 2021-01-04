#! /usr/bin/python3

import sys, os, time


DIRECTIONS = {
    "U": -1j,
    "D":  1j,
    "L": -1,
    "R":  1
}
def getButtonForPath(position, path, keypad):
    for move in path:
        newPosition = position + DIRECTIONS[move]
        if newPosition in keypad:
            position = newPosition
    return position, keypad[position]


def getCode(paths, keypad):
    position = 0
    code = []
    for path in paths:
        position, digit = getButtonForPath(position, path, keypad)
        code.append(digit)
    return "".join(code)


KEYPAD1 = {
    -1 - 1j: "1", -1j: "2",  1 - 1j: "3",
    -1     : "4",   0: "5",  1     : "6",
    -1 + 1j: "7",  1j: "8",  1 + 1j: "9"
}
def part1(paths):
    return getCode(paths, KEYPAD1)


KEYPAD2 = {
                            -2j: "1",
              -1 - 1j: "2", -1j: "3", 1 - 1j: "4",
    -2: "5",  -1     : "6",   0: "7", 1     : "8", 2: "9",
              -1 + 1j: "A",  1j: "B", 1 + 1j: "C",
                             2j: "D"
}
def part2(paths):
    return getCode(paths, KEYPAD2)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip() for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()