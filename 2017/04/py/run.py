#! /usr/bin/python3

import sys, os, time
from typing import Callable, List, Tuple


def run_tests(passphrases: List[List[str]], validation_func: Callable[[List[str]],bool]) -> int:
    return sum(map(lambda passphrase: validation_func(passphrase), passphrases))


def is_anagram(word1: str, word2: str) -> bool:
    return len(word1) == len(word2) and \
        all(map(lambda c: word1.count(c) == word2.count(c), word1))


def has_no_anagram(passphrase: List[str]) -> bool:
    for index, word in enumerate(passphrase):
        for other_word in passphrase[:index] + passphrase[index + 1:]:
            if is_anagram(word, other_word):
                return False
    return True


def solve(passphrases: List[List[str]]) -> Tuple[int,int]:
    return (
        run_tests(passphrases, lambda passphrase: 
            not any(map(lambda word: passphrase.count(word) > 1, passphrase))),
        run_tests(passphrases, has_no_anagram)
    )


def get_input(file_path: str) -> List[List[str]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ line.strip().split(" ") for line in file.readlines() ]


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