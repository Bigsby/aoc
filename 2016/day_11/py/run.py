#! /usr/bin/python3

import sys, os, time
from typing import Dict, Iterable, List, Tuple
import re
from itertools import combinations


Floor = List[int]
Floors = List[Floor]
Elevator = Tuple[int,int]
Move = Tuple[int,int,Elevator]
State = Tuple[int,Floors]
EMPTY_SLOT = 0
radioisotopes: Dict[str,int] = { }


def isGroupValid(group: Iterable[int]) -> bool:
    testGroup = list(group)
    generators = [ part for part in group if part > 0 ]
    for generator in generators:
        if -generator in testGroup:
            testGroup.remove(-generator)
            testGroup.remove(generator)
    if not testGroup:
        return True
    return any(map(lambda part: part > 0, testGroup)) ^ any(map(lambda part: part < 0, testGroup))


def isMoveValid(currentFloor: Floor, nextFloor: Floor, elevator: Elevator) -> bool:
    currentTestFloor = list(currentFloor)
    for part in elevator:
        if part in currentTestFloor:
            currentTestFloor.remove(part)
    nextTestFloor = list(nextFloor)
    for part in elevator:
        if part != EMPTY_SLOT:
            nextTestFloor.append(part)
    
    return isGroupValid(currentTestFloor) and  isGroupValid(nextTestFloor)


def makeMove(floors: Floors, move: Move) -> State:
    try: 
        floors = [ list(floor) for floor in floors ]
        currentFloor, nextFloor, parts = move
        for part in parts:
            if part != EMPTY_SLOT:
                floors[currentFloor].remove(part)
                floors[nextFloor].append(part)
        return nextFloor, floors
    except:
        raise Exception("failed to do move", floors, move)


def getValidDirectionalMoves(state: State, direction: int, possibleMovesGroups: List[Elevator]):
    currentFloor, floors = state
    nextFloor = currentFloor + direction
    validMoves = []

    if nextFloor == 0:
        if not len(floors[nextFloor]):
            return []
    if nextFloor == 1 and not (len(floors[1]) or len(floors[0])):
        return []

    if 0 <= nextFloor < 4:
        for moveGroup in sorted(possibleMovesGroups, key=lambda group: abs(group[0]) + abs(group[1])):
            if isMoveValid(floors[currentFloor], floors[nextFloor], moveGroup):
                validMoves.append((currentFloor, nextFloor, moveGroup))
    return sorted(validMoves, key=lambda move: (abs(move[2][0]), abs(move[2][1])))


def pruneMoves(moves: List[Move]) -> List[Move]:
    pairMoves = [ move for move in moves if move[2][0] == -move[2][1] ]
    if len(pairMoves) > 1:
        for pairMove in pairMoves[:-1]:
            moves.remove(pairMove)

    upstairsMoves = [ move for move in moves if move[0] < move[1] ]
    singleUpMoves = [ move for move in upstairsMoves if move[2][0] == EMPTY_SLOT or move[2][1] == EMPTY_SLOT ]
    if len(singleUpMoves) != len(upstairsMoves):
        for singleUpMove in singleUpMoves:
            moves.remove(singleUpMove)
    
    downstairsMoves = [ move for move in moves if move[0] > move[1] ]
    pairDownstairsMoves = [ move for move in downstairsMoves if move[2][0] != EMPTY_SLOT and move[2][1] != EMPTY_SLOT ]
    if len(pairDownstairsMoves) != len(downstairsMoves):
        for pairDownstairsMove in pairDownstairsMoves:
            moves.remove(pairDownstairsMove)
    
    return moves


def getValidMoves(state: State) -> List[Move]:
    currentFloor, floors = state
    possibleMoveGroups = list(filter(isGroupValid, combinations(floors[currentFloor] + [EMPTY_SLOT], 2)))
    validMoves: List[Move] = getValidDirectionalMoves(state, 1, possibleMoveGroups) \
         + getValidDirectionalMoves(state, -1, possibleMoveGroups)
    return pruneMoves(validMoves)


def getFloorStateRepresentation(floor: Floor) -> str:
    return "".join(map(str,sorted(floor)))


def getStateRepresentation(state: State):
    currentFloor, floors = state
    radios: Dict[int,str] = {}
    nextLetter = ord("A")
    groups = []
    for floor in floors:
        group = []
        for part in floor:
            number = abs(part)
            if number not in radios:
                radios[number] = chr(nextLetter)
                nextLetter += 1
            letter = radios[number]
            group.append(letter if part > 0 else letter.lower())
        groups.append(group)

    return "|".join([ str(currentFloor) , *map(lambda group: "".join(sorted(group)), groups) ])


def solve(floors: Floors) -> int:
    initialState: State = (0,floors)
    queue: List[Tuple[State,List[str]]] = [(initialState, [])]

    while queue:
        state, past = queue.pop()
        for move in getValidMoves(state):
            newState = makeMove(state[1], move)
            if newState[0] == 3 and len(newState[1][-1]) == len(radioisotopes) * 2:
                return len(past) + 1
            else:
                newStateRepresentation = getStateRepresentation(newState)
                if newStateRepresentation not in past:
                    newPast = list(past)
                    newPast.append(newStateRepresentation)
                    queue.append((newState, newPast))
    raise Exception("Solution not found")


def part1(floors: Floors) -> int:
    return solve(floors)


lineRegex = re.compile(r"a (?P<radioisotope>\w+)(?P<part>-compatible microchip| generator)")
def parseLine(line: str) -> List[int]:
    result: List[int] = []
    for match in lineRegex.finditer(line):
        radioisotope = match.group("radioisotope")
        if not radioisotopes:
            radioisotopes[radioisotope] = 1
        elif radioisotope not in radioisotopes:
            radioisotopes[radioisotope] = max(radioisotopes.values()) + 1
        value = radioisotopes[radioisotope]
        result.append(value if "generator" in match.group("part") else -value)
    return result


PART2_EXTRA = "a elerium generator, a elerium-compatible microchip, a dilithium generator, a dilithium-compatible microchip"
def part2(floors: Floors):
    floors[0] += parseLine(PART2_EXTRA)
    return solve(floors)


def getInput(filePath: str) -> Floors:
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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()