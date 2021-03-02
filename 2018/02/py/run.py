#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from itertools import combinations


def part1(ids: List[str]) -> int:
    twice_count = 0
    thrice_count = 0
    for id in ids:
        id_counts = { id.count(c) for c in id }
        twice_count += 2 in id_counts
        thrice_count += 3 in id_counts
    return twice_count * thrice_count
    

def part2(ids: List[str]) -> str:
    for id1, id2 in combinations(ids, 2):
        differences = [ i for i in range(len(id1)) if id1[i] != id2[i] ]
        if len(differences) == 1:
            diferent_index = differences[0]
            return id1[:diferent_index] + id1[diferent_index + 1:]
    raise Exception("Ids differencing 1 not found")


def solve(ids: List[str]) -> Tuple[int,str]:
    return (
        part1(ids),
        part2(ids)
    )


def get_input(file_path: str) -> List[str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ line.strip() for line in file.readlines() ]


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