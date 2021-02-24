#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple

Instruction = Tuple[int,int,int]


def toOrd(programs: str) -> List[int]:
    return [ ord(c) for c in programs ]


def toStr(programs: List[int]) -> str:
    return "".join([ chr(c) for c in programs ])


def dance(instructions: List[Instruction], programs: List[int]) -> List[int]:
    for instruction in instructions:
        move, a, b = instruction
        if move == 0:
            programs = programs[-a:] + programs[:-a]
        elif move == 1:
            oldA = programs[a]
            programs[a] = programs[b]
            programs[b] = oldA
        elif move == 2:
            aIndex = programs.index(a)
            bIndex = programs.index(b)
            oldA = programs[aIndex]
            programs[aIndex] = programs[bIndex]
            programs[bIndex] = oldA
    return programs


def part1(instructions: List[Instruction]) -> str:
    return toStr(dance(instructions, toOrd("abcdefghijklmnop")))


CYCLES = 10**9
def part2(instructions: List[Instruction]) -> str:    
    programs = toOrd("abcdefghijklmnop")
    seen = [ tuple(programs) ]
    
    for cycle in range(CYCLES):
        programs = dance(instructions, programs)
        p = tuple(programs)
        if p in seen:
            return toStr(list(seen[CYCLES % (cycle + 1)]))
        seen.append(p)
    return toStr(programs)


def parseInstruction(text: str) -> Instruction:
    if text.startswith("s"):
        return (0, int(text[1:]), 0)
    elif text.startswith("x"):
        a, b = text[1:].split("/")
        return (1, int(a), int(b))
    elif text.startswith("p"):
        a, b = text[1:].split("/")
        return (2, ord(a), ord(b))
    raise Exception("Unknow instruction", text)


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        return [ parseInstruction(text) for text in file.read().strip().split(",") ]


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()