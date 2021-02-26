#! /usr/bin/python3

import sys, os, time
from typing import Tuple
from hashlib import md5


PREFIX = "0" * 5


def solve(doorId: str) -> Tuple[str,str]:
    index = 0
    password1 = ""
    password2 = [ "_" for _ in range(8) ]
    missingIndexes = list("01234567")
    while missingIndexes:
        result = md5((doorId + str(index)).encode("utf-8")).hexdigest()
        if result.startswith(PREFIX):
            if len(password1) < 8:
                password1 += result[5]
            digitIndex = result[5]
            if digitIndex in missingIndexes:
                password2[int(digitIndex)] = result[6]
                missingIndexes.remove(digitIndex)
        index += 1
    return (
        password1, 
        "".join(password2)
    )


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read()


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