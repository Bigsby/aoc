#! /usr/bin/python3

import sys, os, time
from typing import Generator, Tuple
import re


FACTOR_A = 16807
FACTOR_B = 48271


MODULUS = 2147483647
def buildGenerator(number: int, factor: int, divisor: int) -> Generator[int,int,int]:
    while True:
        number = number * factor % MODULUS
        if number % divisor == 0:
            yield number & 0xffff
            

def runSequences(generators: Tuple[int,int], divisorA: int, divisorB: int, millionCycles: int) -> int:
    generatorA, generatorB = generators
    sequenceA, sequenceB = buildGenerator(generatorA, FACTOR_A, divisorA), buildGenerator(generatorB, FACTOR_B, divisorB)
    return sum(next(sequenceA) == next(sequenceB) for _ in range(millionCycles * (10 ** 6)))


def part1(generators: Tuple[int,int]):
    return runSequences(generators, 1, 1, 40)


DIVISOR_A = 4
DIVISOR_B = 8
def part2(generators: Tuple[int,int]):
    return runSequences(generators, DIVISOR_A, DIVISOR_B, 5)


numbersRegex = re.compile(r"\d+")
def getInput(filePath: str) -> Tuple[int,int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        matches = numbersRegex.findall(file.read())
        return int(matches[0]), int(matches[1])


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