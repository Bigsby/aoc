#! /usr/bin/python3

import sys, os, time
from typing import Tuple


class Elf:
    def __init__(self, position: int):
        self.position = position + 1
        self.next = self
        self.previous = self

    def remove(self):
        self.previous.next = self.next
        self.next.previous = self.previous


def part2(elf_count: int) -> int:
    elves = list(map(Elf, range(elf_count)))
    for index in range(elf_count):
        elves[index].next = elves[(index + 1) % elf_count]
        elves[index].previous = elves[(index -1 ) % elf_count]
    current_elf = elves[0]
    elf_to_remove = elves[elf_count // 2]
    for index in range(elf_count - 1):
        elf_to_remove.remove()
        elf_to_remove = elf_to_remove.next
        if (elf_count - index) % 2 == 1:
            elf_to_remove = elf_to_remove.next
        current_elf = current_elf.next
    return current_elf.position


def solve(elf_count: int) -> Tuple[int,int]:
    return (
        # 1 + 2 * (elfCount - 2 ** (math.floor(math.log(elfCount, 2))))
        int(f"{elf_count:b}"[1:] + "1", 2),
        part2(elf_count)
    )


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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