#! /usr/bin/python3

import sys, os, time

def part1(elfCount: int) -> int:
    # 1 + 2 * (elfCount - 2 ** (math.floor(math.log(elfCount, 2))))
    return int(f"{elfCount:b}"[1:] + "1", 2)


class Elf:
    def __init__(self, position: int):
        self.position = position + 1
        self.next = self
        self.previous = self

    def remove(self):
        self.previous.next = self.next
        self.next.previous = self.previous


def part2(elfCount: int) -> int:
    elves = list(map(Elf, range(elfCount)))
    for index in range(elfCount):
        elves[index].next = elves[(index + 1) % elfCount]
        elves[index].previous = elves[(index -1 ) % elfCount]
    
    currentElf = elves[0]
    elfToRemove = elves[elfCount // 2]
    for index in range(elfCount - 1):
        elfToRemove.remove()
        elfToRemove = elfToRemove.next
        if (elfCount - index) % 2 == 1:
            elfToRemove = elfToRemove.next
        currentElf = currentElf.next

    return currentElf.position


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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