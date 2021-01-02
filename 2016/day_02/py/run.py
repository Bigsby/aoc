#! /usr/bin/python3

import sys, os, time


MOVES = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}


def getCodeForButton(currentPosition, moves, keypad, getNewPositionFunc):
    for move in moves:
        currentPosition = getNewPositionFunc(currentPosition, move)
    return currentPosition, keypad[currentPosition[0]][currentPosition[1]]


def getCode(currentPosition, buttons, keypad, getNewPositionFunc):
    code = []
    for button in buttons:
        currentPosition, digit = getCodeForButton(currentPosition, button, keypad, getNewPositionFunc)
        code.append(digit)
    return "".join(code)


KEYPAD1 = [
   [ "1", "2", "3" ],
   [ "4", "5", "6" ],
   [ "7", "8", "9" ]
]


def getNewPosition1(current, move):
    step = MOVES[move]
    newPosition = (current[0] + step[0], current[1] + step[1])
    if newPosition[0] < 0 or newPosition[0] > 2 or newPosition[1] < 0 or newPosition[1] > 2:
        return current
    return newPosition


def part1(buttons):
    return getCode((1,1), buttons, KEYPAD1, getNewPosition1)


N_A = None
KEYPAD2 = [
    [ N_A, N_A, "1", N_A, N_A ],
    [ N_A, "2", "3", "4", N_A ],
    [ "5", "6", "7", "8", "9" ],
    [ N_A, "A", "B", "C", N_A ],
    [ N_A, N_A, "D", N_A, N_A ]
]


def getNewPosition2(current, move):
    stepX, stepY = MOVES[move]
    currentX, currentY = current
    newX, newY = (currentX + stepX, currentY + stepY)
    if newX < 0 \
        or newX > 4 \
        or newY < 0 \
        or newY > 4 \
        or KEYPAD2[newX][newY] == N_A:
        return current
    return (newX, newY)


def part2(buttons):
    return getCode((2,0), buttons, KEYPAD2, getNewPosition2)


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