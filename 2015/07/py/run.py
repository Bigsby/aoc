#! /usr/bin/python3

import sys, os, time
from typing import Callable, Dict, List, Tuple, Union
import re

SCALAR, WIRE = "scalar", "wire"
INPUT, UNARY, BINARY = "input", "unary", "binary"


class Operand():
    def __init__(self, value: str):
        try:
            self.type = SCALAR
            self.scalar = int(value)
        except:
            self.type = WIRE
            self.wire:str = value


class Connection():
    def __init__(self, operation: Union[str,None], type: str, operand1: str, operand2: Union[str,None], target: str):
        self.operation = operation
        self.type = type
        self.operand1 = Operand(operand1)
        self.operand2 = Operand(operand2) if operand2 else None
        self.target = target

BINARY_OPERATIONS: Dict[str,Callable[[int,int],int]] = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "LSHIFT": lambda x, y: x << y,
        "RSHIFT": lambda x, y: x >> y
}
class Circuit():
    def __init__(self, connections: List[Connection]):
        self.connections = connections
        self.solutions: Dict[str,int] = {}

    def getConnectionFromTarget(self, target: str) -> Connection:
        return next(filter(lambda conn: conn.target == target, self.connections))

    def getValueFromOperand(self, operand: Operand) -> int:
        if operand.type == SCALAR:
            return operand.scalar
        return self.getValueFromConnection(self.getConnectionFromTarget(operand.wire))
    
    def getValueFromBinaryConnection(self, connection: Connection) -> int:
        if connection.operation and connection.operand2:
            operation = BINARY_OPERATIONS[connection.operation]
            return operation(self.getValueFromOperand(connection.operand1), self.getValueFromOperand(connection.operand2))
        raise Exception("Operation no defined in connection")

    def calculateValueForConnection(self, connection: Connection) -> int:
        if connection.type == INPUT:
            return self.getValueFromOperand(connection.operand1)
        if connection.type == UNARY:
            return ~self.getValueFromOperand(connection.operand1)
        if connection.type == BINARY:
            return self.getValueFromBinaryConnection(connection)
        raise Exception("Unknown operation:", connection)

    def getValueFromConnection(self, connection: Connection) -> int:
        if connection.target in self.solutions:
            return self.solutions[connection.target]
        result = self.calculateValueForConnection(connection)
        self.solutions[connection.target] = result
        return result

    def solveFor(self, target: str, initialState: Dict[str,int] = {}) -> int:
        self.solutions = initialState
        return self.getValueFromConnection(self.getConnectionFromTarget(target))


MAX_VALUE = 1 << 17
def solve(circuit: Circuit) -> Tuple[int,int]:
    startingTarget = "a"
    part1 = circuit.solveFor(startingTarget)
    part2 = circuit.solveFor(startingTarget, { "b": part1 })
    return part1 if part1 >= 0 else part1 + MAX_VALUE, part2 if part2 >= 0 else part2 + MAX_VALUE


sourceTargetRegex = re.compile(r"^(.*)\s->\s(\w+)$")
inputRegex = re.compile(r"^[^\s]+$")
unaryRegex = re.compile(r"NOT\s(\w+)$")
binaryRegex = re.compile(r"^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)")
def processLine(line: str) -> Connection:
    sourceTargetMatch = sourceTargetRegex.match(line)
    if sourceTargetMatch:
        source, target = sourceTargetMatch.group(1, 2)
        if inputRegex.match(source):
            return Connection(None, INPUT, source, None, target)
        unaryMatch = unaryRegex.match(source)
        if unaryMatch:
            return Connection(None, UNARY, unaryMatch.group(1), None, target)
        binaryMatch = binaryRegex.match(source)
        if binaryMatch:
            return Connection(binaryMatch.group(2), BINARY, binaryMatch.group(1), binaryMatch.group(3), target)
        raise Exception("Unrecognized operation:", source)
    else:
        raise Exception("Unrecognized operation line:", line)


def getInput(filePath: str) -> Circuit:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return Circuit([ processLine(line) for line in file.readlines() ])


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()