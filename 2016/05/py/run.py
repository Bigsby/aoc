#! /usr/bin/python3

import sys, os, time
from typing import Tuple
from hashlib import md5

PREFIX = "0" * 5


def solve(door_id: str) -> Tuple[str,str]:
    index = 0
    password1 = ""
    password2 = [ "_" for _ in range(8) ]
    missing_indexes = list("01234567")
    while missing_indexes:
        result = md5((door_id + str(index)).encode("utf-8")).hexdigest()
        if result.startswith(PREFIX):
            if len(password1) < 8:
                password1 += result[5]
            digit_index = result[5]
            if digit_index in missing_indexes:
                password2[int(digit_index)] = result[6]
                missing_indexes.remove(digit_index)
        index += 1
    return (
        password1, 
        "".join(password2)
    )


def get_input(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return file.read().strip()


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