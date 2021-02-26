#! /usr/bin/python3

import sys, os, time
from typing import Generator, Tuple
import re


MODULUS = 2147483647
def buildGenerator(number: int, factor: int, divisor: int) -> Generator[int,int,int]:
    while True:
        number = number * factor % MODULUS
        if number % divisor == 0:
            yield number & 0xffff


FACTOR_A = 16807
FACTOR_B = 48271
def runSequences(generators: Tuple[int,int], divisorA: int, divisorB: int, millionCycles: int) -> int:
    generatorA, generatorB = generators
    sequenceA, sequenceB = buildGenerator(generatorA, FACTOR_A, divisorA), buildGenerator(generatorB, FACTOR_B, divisorB)
    return sum(next(sequenceA) == next(sequenceB) for _ in range(millionCycles * (10 ** 6)))


DIVISOR_A = 4
DIVISOR_B = 8
def solve(generators: Tuple[int,int]) -> Tuple[int,int]:
    return (
        runSequences(generators, 1, 1, 40),
        runSequences(generators, DIVISOR_A, DIVISOR_B, 5)
    )


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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()