#! /usr/bin/python3

import sys, os, time
from typing import Deque, List, Tuple
from collections import deque

Instruction = Tuple[int,int,int]
SWAP_POSITION = 0
SWAP_LETTER = 1
ROTATE_LEFT = 2
ROTATE_RIGHT = 3
ROTATE_LETTER = 4
REVERSE = 5
MOVE = 6


def process(start: str, instructions: List[Instruction], reverse: bool = False) -> str:
    password: Deque[int] = deque(ord(value) for value in start)
    if reverse:
        instructions.reverse()
    for opCode, a, b in instructions:
        if opCode == SWAP_POSITION:
            oldA = password[a]
            password[a] = password[b]
            password[b] = oldA
        elif opCode == SWAP_LETTER:
            indexOfA = password.index(a)
            indexOfB = password.index(b)
            oldA = password[indexOfA]
            password[indexOfA] = password[indexOfB]
            password[indexOfB] = oldA
        elif opCode == ROTATE_LEFT:
            password.rotate(a if reverse else -a)
        elif opCode == ROTATE_RIGHT:
            password.rotate(-a if reverse else a)
        elif opCode == ROTATE_LETTER:
            indexOfA = password.index(a)
            rotation = indexOfA + 1 + (1 if indexOfA >= 4 else 0)
            if reverse:
                rotation = -(indexOfA // 2 + (1 if indexOfA % 2 == 1 or indexOfA == 0 else 5))
            password.rotate(rotation)
        elif opCode == REVERSE:
            passwordList = list(password)
            password = deque(passwordList[:a] + passwordList[a:b + 1][::-1] + passwordList[b + 1:])
        elif opCode == MOVE:
            origin, destination = (b, a) if reverse else (a, b)
            letterToMove = password[origin]
            password.remove(letterToMove)
            password.insert(destination, letterToMove)
    return "".join(chr(c) for c in password)


def solve(instructions: List[Instruction]) -> Tuple[str,str]:
    return (
        process("abcdefgh", instructions),
        process("fbgdceah", instructions, True)
    )


def parseLine(line: str) -> Instruction:
    if line.startswith("swap position"):
        return (SWAP_POSITION, int(line[14]), int(line[-1]))
    elif line.startswith("swap letter"):
        return (SWAP_LETTER, ord(line[12]), ord(line[-1]))
    elif line.startswith("rotate left"):
        return (ROTATE_LEFT, int(line[12]), 0)
    elif line.startswith("rotate right"):
        return (ROTATE_RIGHT, int(line[13]), 0)
    elif line.startswith("rotate based"):
        return (ROTATE_LETTER, ord(line[-1]), 0)
    elif line.startswith("reverse"):
        return (REVERSE, int(line[18]), int(line[-1]))
    elif line.startswith("move"):
        return (MOVE, int(line[14]), int(line[-1]))
    raise Exception("Unknow instruction", line)


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line.strip()) for line in file.readlines() ]


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