#! /usr/bin/python3

import re
from itertools import combinations_with_replacement

from common import getInput, processReplacementDirect


def getValidReplacements(molecule, replacements):
    return filter(lambda replacement: replacement.target in molecule, replacements)


def getNextIteration(branches, replacements):
    for branch in branches:
        for replacement in getValidReplacements(branch, replacements):
            for newBranch in processReplacementDirect(branch, replacement.target, replacement.source):
                yield newBranch

 

def main():
    replacements, targetMolecule = getInput()
    startingMolecule = "e"


    branches = [targetMolecule]
    iteration = 0
    maxIterations = 20
    while True:
        iteration += 1
        print("Iteration", iteration, "with", len(branches), "branches")
        newBranches = getNextIteration(branches, replacements)
        newBranches = set(newBranches)
        if any(map(lambda b: b == startingMolecule, newBranches)) or iteration == maxIterations:
            break
        branches = list(newBranches)
     
    print("Finished after", iteration, "iterations")


if __name__ == "__main__":
    main()
