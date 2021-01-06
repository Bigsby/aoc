#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re


def buildDependencies(pairs: List[Tuple[str,str]]) -> Dict[str, List[str]]:
    dependencies: Dict[str, List[str]] = {}
    for dependency, dependant in pairs:
        if dependant not in dependencies:
            dependencies[dependant] = []
        if dependency not in dependencies:
            dependencies[dependency] = []
        dependencies[dependant].append(dependency)
    return dependencies


def part1(pairs: List[Tuple[str,str]]) -> str:
    dependencies = buildDependencies(pairs)    
    path: List[str] = []
    while dependencies:
        nextStep = next(iter(sorted(step for step, stepDependencies in dependencies.items() if not stepDependencies)))
        del dependencies[nextStep]
        path.append(nextStep)
        for stepDependencies in dependencies.values():
            if nextStep in stepDependencies:
                stepDependencies.remove(nextStep)

    return "".join(path)
        

WORKER_COUNT = 5
STEP_DURATION_OFFSET = ord("A") - 60 - 1
def part2(pairs: List[Tuple[str,str]]):
    dependencies = buildDependencies(pairs)
    runningWorkers: Dict[str, int] = {}
    seconds = 0
    while dependencies or runningWorkers:
        toRemove: List[str] = []
        for step in runningWorkers.keys():
            runningWorkers[step] -= 1
            if runningWorkers[step] == 0:
                toRemove.append(step)
        for step in toRemove:
            del runningWorkers[step]
            for stepDependencies in dependencies.values():
                if step in stepDependencies:
                    stepDependencies.remove(step)

        nextSteps = iter(sorted(step for step, stepDependencies in dependencies.items() if not stepDependencies))
        nextStep = next(nextSteps, None)
        while len(runningWorkers) <= WORKER_COUNT and nextStep:
            runningWorkers[nextStep] = ord(nextStep) - STEP_DURATION_OFFSET
            del dependencies[nextStep]
            nextStep = next(nextSteps, None)

        seconds += 1
    
    return seconds - 1 # because 1 seconds is counted after emptying runningWorkers the last time


lineRegex = re.compile(r"\s([A-Z])\s")
def getInput(filePath: str) -> List[Tuple[str,str]] :
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ tuple(lineRegex.findall(line.strip())) for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()