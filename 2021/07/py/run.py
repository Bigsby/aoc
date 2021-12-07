#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Callable


def test_cost_in_direction(crabs: List[int], position: int, direction: int, cost: int, cost_func: Callable[[List[int],int],int]) -> int:
    position += direction
    last_cost = cost
    current_cost = cost_func(crabs, position)
    while current_cost <= last_cost:
        last_cost = current_cost
        position += direction
        current_cost = cost_func(crabs, position)
    return last_cost
    
    
def get_cost1(crabs: List[int], mean: int) -> int:
    return sum([ abs(position - mean) for position in crabs])
       

def part1(crabs: List[int]) -> int:
    crabs.sort()
    mean = crabs[int(len(crabs) / 2)]
    return get_cost1(crabs, mean)

    mean_cost = get_cost1(crabs, mean)
    print(mean_cost)
    mean_cost = min(mean_cost, test_cost_in_direction(crabs, mean, -1, mean_cost, get_cost1))
    print(mean_cost)
    mean_cost = min(mean_cost, test_cost_in_direction(crabs, mean, 1, mean_cost, get_cost1))
    print(mean_cost)
    return mean_cost


def get_distance_cost(pos_a: int, pos_b: int) -> int:
    distance = abs(pos_a - pos_b)
    return int((distance * (distance + 1)) / 2)


def get_cost2(crabs: List[int], average: int) -> int:
    return sum([ get_distance_cost(average, position) for position in crabs])


def part2(crabs: List[int]) -> int:
    avg = int(sum(crabs) / len(crabs))
    return get_cost2(crabs, avg)
    avg_cost = get_cost2(crabs, avg)
    print(avg_cost)
    avg_cost = min(avg_cost, test_cost_in_direction(crabs, avg, -1, avg_cost, get_cost2))
    print(avg_cost)
    avg_cost = min(avg_cost, test_cost_in_direction(crabs, avg, 1, avg_cost, get_cost2))
    print(avg_cost)
    return avg_cost


def solve(puzzle_input: List[int]) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ int(number) for number in file.read().strip().split(',') ]


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
