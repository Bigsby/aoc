#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Edge = Tuple[str,str]
Input = List[Edge]


def find_paths(edges: Input, repeat: bool) -> int:
    queue = [ ("start", "start", not repeat) ]
    complete_paths_count = 0 
    while (len(queue)):
        node, path, small_repeat = queue.pop(0)
        if node == "end":
            complete_paths_count += 1
            continue
        for edge in filter(lambda edge: edge[0] == node or edge[1] == node, edges):
            other = edge[0] if edge[1] == node else edge[1]
            if not(other == "start" or (small_repeat and other.lower() == other and other in path)):
                new_path = f"{path},{other}"
                queue.append((other, new_path, small_repeat or (other == other.lower() and other in path)))
    return complete_paths_count
    

def solve(edges: Input) -> Tuple[int,int]:
    return (find_paths(edges, False), find_paths(edges, True))


def parse_line(line: str) -> Tuple[str,str]:
    split = line.split("-")
    return split[0], split[1]


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ parse_line(line.strip()) for line in file.readlines() ]


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
