#! /usr/bin/python3

from itertools import permutations

from common import getInput, getPathDistance, getSingleNodes, getPossiblePaths


def main():
    edges = list(getInput())
    singleNodes = getSingleNodes(edges)
    possiblePaths = getPossiblePaths(singleNodes)
    minimalDistance = min(map(lambda permutation: getPathDistance(permutation, edges), possiblePaths))
    print("Minimal distance:", minimalDistance)


if __name__ == "__main__":
    main()
