#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Union, Iterator


class File():
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory():
    def __init__(self, name: str, parent: Union["Directory", None] = None) -> None:
        self.name = name
        self.parent = parent
        self.children: List["Directory"] = []
        self.files: List[File] = []

    def get_size(self) -> int:
        return sum(map(lambda file: file.size, self.files)) + sum(map(lambda child: child.get_size(), self.children))


Input = List[List[str]]


def get_all_sizes(directory: Directory) -> Iterator[int]:
    yield directory.get_size()
    for child in directory.children:
        yield from get_all_sizes(child)


def build_file_system(output: Input) -> Directory:
    root: Directory = Directory("/")
    current = root
    for line in output:
        if line[0] == "$":
            if line[1] == "cd":
                if line[2] == ".." and current.parent:
                    current = current.parent
                    continue
                if line[2] == "/":
                    continue
                new_directory = Directory(line[2], current)
                current.children.append(new_directory)
                current = new_directory
        elif line[0] != "dir" and current:
            current.files.append(File(line[1], int(line[0])))
    return root


def part1(sizes: List[int]) -> int:
    return sum([ size for size in sizes if size <= 100_000])


def part2(sizes: List[int]) -> int:
    free_space = 70_000_000 - max(sizes)
    minimum_to_delete = 30_000_000 - free_space
    return min([ size for size in sizes if size >= minimum_to_delete])


def solve(puzzle_input: Input) -> Tuple[int, int]:
    sizes = [ size for size in get_all_sizes(build_file_system(puzzle_input)) ]
    return (part1(sizes), part2(sizes))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [line.strip().split() for line in file.readlines()]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
