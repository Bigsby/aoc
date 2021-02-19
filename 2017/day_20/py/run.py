#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Set, Tuple
import re, math
from collections import defaultdict

Values = Tuple[int,int,int]
Particle = Tuple[Values,Values,Values]


def getManhatanValue(values: Values) -> int:
    return abs(values[0]) + abs(values[1]) + abs(values[2])


def part1(particles: List[Particle]) -> int:
    closestParticle = 0
    lowestAcceleration = sys.maxsize
    lowestPosition = sys.maxsize
    for index, (position, _, acceleration) in enumerate(particles):
        accelerationTotal = getManhatanValue(acceleration)
        if accelerationTotal < lowestAcceleration:
            lowestAcceleration = accelerationTotal
            closestParticle = index
            lowestPosition = getManhatanValue(position)
        if accelerationTotal == lowestAcceleration and getManhatanValue(position) < lowestPosition:
            closestParticle = index
            lowestPosition = getManhatanValue(position)
    return closestParticle


def getQuadraticABC(particleA: Particle, particleB: Particle, coordinate: int) -> Tuple[float,float,int]:
    pAp = particleA[0][coordinate]
    pAa = particleA[2][coordinate]
    pAv = particleA[1][coordinate] + pAa / 2 
    pBp = particleB[0][coordinate]
    pBa = particleB[2][coordinate]
    pBv = particleB[1][coordinate] + pBa / 2
    return (pAa - pBa) / 2, pAv - pBv, pAp - pBp

def getColitionTimes(particleA: Particle, particleB: Particle) -> List[int]:
    a, b, c = getQuadraticABC(particleA, particleB, 0)
    times = []
    if a == 0:
        if b != 0:
            times.append(-c / b)
    else:
        bb = b * b
        ac4 = a * c * 4
        if bb < ac4:
            return []
        elif bb == ac4:
            times.append(-b / (2 * a))
        else:
            rt = math.sqrt(bb - ac4)
            times.append((-b + rt) / (2 * a))
            times.append((-b - rt) / (2 * a))
    times = map(int, filter(lambda t: t >= 0 and round(t) == t, times))
    result = []
    for t in times:
        collide = True
        for k in [1, 2]:
            a, b, c = getQuadraticABC(particleA, particleB, k)
            if a * t * t + b * t + c != 0:
                collide = False
                break
        if collide:
            result.append(t)
    return result


def part2(particles: List[Particle]) -> int:
    collisions: Dict[int,List[Tuple[int,int]]] = defaultdict(list)
    for thisIndex in range(len(particles) - 1):
        for otherIndex in range(thisIndex + 1, len(particles)):
            for time in getColitionTimes(particles[thisIndex], particles[otherIndex]):
                collisions[time].append((thisIndex, otherIndex))
    particleIndexes: Set[int] = set(range(len(particles)))
    for time in sorted(list(collisions.keys())):
        collidedToRemove = set()
        for indexA, indexB in collisions[time]:
            if indexA in particleIndexes and indexB in particleIndexes:
                collidedToRemove.add(indexA)
                collidedToRemove.add(indexB)
        particleIndexes -= collidedToRemove
    return len(particleIndexes)
    


lineRegex = re.compile(r"^p=<(?P<p>[^>]+)>, v=<(?P<v>[^>]+)>, a=<(?P<a>[^>]+)>$")
def parseLine(line: str) -> Particle:
    match = lineRegex.match(line)
    if match:
        return tuple(map(int,match.group("p").split(","))), tuple(map(int,match.group("v").split(","))), tuple(map(int,match.group("a").split(",")))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Particle]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]
            


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()