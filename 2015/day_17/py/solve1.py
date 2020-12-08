#! /usr/bin/python3

from itertools import combinations
from functools import reduce

from common import getInput


def main():
    containers = list(getInput())
    targetTotal = 150
    
    validCombinations = []
    for containerCount in range(3, len(containers)):
        for combination in combinations(containers, containerCount):
            combinationTotal = reduce(lambda soFar, current: soFar + current, combination)
            if combinationTotal == targetTotal:
                validCombinations.append(combination)

    result = len(validCombinations)
    print("Valid combinations:", result)





if __name__ == "__main__":
    main()
