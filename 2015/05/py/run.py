#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re


FORBIDEN_PAIRS = [ "ab", "cd", "pq", "xy" ]
vowel_regex = re.compile("[aeiou]")
repeat_regex = re.compile("(.)\\1{1,}")
def is_word_nice(word: str) -> bool:
    return not any(map(lambda pair: pair in word, FORBIDEN_PAIRS)) \
        and len(vowel_regex.findall(word)) > 2 \
        and len(repeat_regex.findall(word)) != 0


def has_repeating_pair(word: str) -> bool:
    for pair_start in range(len(word) - 2):
        pair_to_test = word[pair_start : pair_start + 2]
        if pair_to_test in word[pair_start + 2:]:
            return True
    return False


def has_repeating_letter(word: str) -> bool:
    for index in range(len(word) - 2):
        if word[index] == word[index + 2]:
            return True
    return False


def solve(words: List[str]) -> Tuple[int,int]:
    return (
        len(list(filter(is_word_nice, words))), 
        len(list(filter(lambda word: has_repeating_pair(word) and has_repeating_letter(word), words)))
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