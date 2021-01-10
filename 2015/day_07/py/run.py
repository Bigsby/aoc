#! /usr/bin/python3

import sys, os, time
from typing import Callable, Dict, List, Union
import re


class Operand():
    def __init__(self, value):
        try:
            self.type = "scalar"
            self.scalar = int(value)
        except:
            self.type = "wire"
            self.wire:str = value


class Connection():
    def __init__(self, operation: Union[str,None], type: str, operand1: str, operand2: Union[str,None], target: str):
        self.operation = operation
        self.type = type
        self.operand1 = Operand(operand1)
        self.operand2 = Operand(operand2)
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

    def getConnectionFromTarget(self, target: Union[str,int]) -> Connection:
        return next(filter(lambda conn: conn.target == target, self.connections))

    def getConnectionFromOperand(self, operand: Operand) -> Union[Connection,None]:
        if operand and operand.type == "wire":
            return self.getConnectionFromTarget(operand.wire)
        return None

    def getValueFromOperand(self, operand: Operand) -> int:
        if operand.type == "scalar":
            return operand.scalar
        return self.getValueFromConnection(self.getConnectionFromTarget(operand.wire))
    
    def getValueFromBinaryConneciton(self, connection: Connection) -> int:
        if connection.operation:
            operation = BINARY_OPERATIONS[connection.operation]
            return operation(self.getValueFromOperand(connection.operand1), self.getValueFromOperand(connection.operand2))
        raise Exception("Operation no defined in connection")

    def getNewValueForConnection(self, connection: Connection):
        if connection.type == "input":
            return self.getValueFromOperand(connection.operand1)
        if connection.type == "unary":
            return ~self.getValueFromOperand(connection.operand1)
        if connection.type == "binary":
            return self.getValueFromBinaryConneciton(connection)
        raise Exception("Unknown operation:", connection)

    def getValueFromConnection(self, connection: Connection) -> int:
        if connection.target in self.solutions:
            return self.solutions[connection.target]
        result = self.getNewValueForConnection(connection)
        self.solutions[connection.target] = result
        return result

    def solveFor(self, target: str, initialState: Dict[str,int] = {}) -> int:
        self.solutions = initialState
        return self.getValueFromConnection(self.getConnectionFromTarget(target))


def runCode(circuit: Circuit, rerunB: bool = False) -> int:
    startingTarget = "a"
    maxValue = pow(2, 16)
    result = circuit.solveFor(startingTarget)

    if rerunB:
        solutions = { "b": result }
        result = circuit.solveFor(startingTarget, solutions)    

    if result < 0:
        result += maxValue
    return result


def part1(circuit: Circuit) -> int:
    return runCode(circuit)


def part2(circuit: Circuit) -> int:
    return runCode(circuit, True)


sourceTargetRegex = re.compile(r"^(.*)\s->\s(\w+)$")
inputRegex = re.compile(r"^[^\s]+$")
unaryRegex = re.compile(r"NOT\s(\w+)$")
binaryRegex = re.compile(r"^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)")
def processLine(line: str) -> Connection:
    sourceTargetMatch = sourceTargetRegex.match(line)
    if sourceTargetMatch:
        source, target = sourceTargetMatch.group(1, 2)
        if inputRegex.match(source):
            return Connection(None, "input", source, None, target)
        unaryMatch = unaryRegex.match(source)
        if unaryMatch:
            return Connection("NOT", "unary", unaryMatch.group(1), None, target)
        binaryMatch = binaryRegex.match(source)
        if binaryMatch:
            return Connection(binaryMatch.group(2), "binary", binaryMatch.group(1), binaryMatch.group(3), target)
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