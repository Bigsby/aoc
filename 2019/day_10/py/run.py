#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import math

Asteroid = complex


def getVisibleCount(asteroid: Asteroid, asteroids: List[Asteroid], maxX: int, maxY: int) -> int:
    asteroids = list(asteroids)
    asteroids.remove(asteroid)
    visibleCount = 0
    
    while asteroids:
        asteroidToCheck = asteroids.pop()
        visibleCount += 1
        delta: complex = asteroidToCheck - asteroid
        jump = delta / math.gcd(abs(int(delta.real)), abs(int(delta.imag)))
        asteroidToCheck = asteroid + jump
        while asteroidToCheck.real >= 0 and asteroidToCheck.real <= maxX \
            and asteroidToCheck.imag >= 0 and asteroidToCheck.imag <= maxY:
            if asteroidToCheck in asteroids:
                asteroids.remove(asteroidToCheck)
            asteroidToCheck += jump

    return visibleCount


def part1(asteroids: List[Asteroid]) -> Tuple[int,Asteroid]:
    maxX = int(max(map(lambda asteroid: asteroid.real, asteroids)))
    maxY = int(max(map(lambda asteroid: asteroid.imag, asteroids)))
    maxVisibleCount = 0
    monitoringStation = -1 -1j
    for asteroid in asteroids:
        visibleCount = getVisibleCount(asteroid, asteroids, maxX, maxY)
        if visibleCount > maxVisibleCount:
            maxVisibleCount = visibleCount
            monitoringStation = asteroid
    return maxVisibleCount, monitoringStation


def part2(asteroids: List[Asteroid], monitoringStation: Asteroid) -> int:
    asteroidAngleDistances: Dict[Asteroid,Tuple[float,int]] = {}
    asteroids.remove(monitoringStation)
    for asteroid in asteroids:
        delta = asteroid - monitoringStation
        angle = math.atan2(delta.real, delta.imag) + math.pi
        distance = int(abs(delta.real) + abs(delta.imag))
        asteroidAngleDistances[asteroid] = (angle, distance)

    targetCount = 1
    angle = 2 * math.pi
    lastRemoved = -1 -1j
    while targetCount <= 200:
        asteroid, (angle, _) = min(asteroidAngleDistances.items(), \
            key=lambda kv: (angle == kv[1][0] or targetCount == 1, (angle - kv[1][0]) % (2 * math.pi), kv[1][1]))
        del asteroidAngleDistances[asteroid]
        lastRemoved = asteroid
        angle = angle
        targetCount += 1
    
    return int(lastRemoved.real) * 100 + int(lastRemoved.imag)


def getInput(filePath: str) -> List[Asteroid]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        asteroids = []
        position = 0
        for line in file.readlines():
            for c in line.strip():
                if c == "#":
                    asteroids.append(position)
                position += 1
            position += 1j - position.real
        return asteroids


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result, monitoringStation = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput, monitoringStation)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()