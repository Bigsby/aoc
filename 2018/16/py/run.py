#! /usr/bin/python3

import sys
import os
import time
import re
from typing import Dict, List, Set, Tuple

Registers = Tuple[int, int, int, int]
Operation = Tuple[int, int, int, int]
Record = Tuple[Registers, Operation, Registers]
MNEMONICS = [
    "addr", "addi",
    "mulr", "muli",
    "banr", "bani",
    "borr", "bori",
    "setr", "seti",
    "gtir", "gtri", "gtrr",
    "eqir", "eqri", "eqrr"
]


def runOperation(registers: Registers, operation: Operation, mnemonic: str) -> Registers:
    _, A, B, C = operation
    result = list(registers)
    value = -1
    if mnemonic == "addr":
        value = registers[A] + registers[B]
    elif mnemonic == "addi":
        value = registers[A] + B
    elif mnemonic == "mulr":
        value = registers[A] * registers[B]
    elif mnemonic == "muli":
        value = registers[A] * B
    elif mnemonic == "banr":
        value = registers[A] & registers[B]
    elif mnemonic == "bani":
        value = registers[A] & B
    elif mnemonic == "borr":
        value = registers[A] | registers[B]
    elif mnemonic == "bori":
        value = registers[A] | B
    elif mnemonic == "setr":
        value = registers[A]
    elif mnemonic == "seti":
        value = A
    elif mnemonic == "gtir":
        value = 1 if A > registers[B] else 0
    elif mnemonic == "gtri":
        value = 1 if registers[A] > B else 0
    elif mnemonic == "gtrr":
        value = 1 if registers[A] > registers[B] else 0
    elif mnemonic == "eqir":
        value = 1 if A == registers[B] else 0
    elif mnemonic == "eqri":
        value = 1 if registers[A] == B else 0
    elif mnemonic == "eqrr":
        value = 1 if registers[A] == registers[B] else 0
    result[C] = value
    return tuple(result)


def testRecord(before: Registers, operation: Operation, after: Registers, opCodes: Dict[str, Set[int]]) -> int:
    count = 0
    opCode, *_ = operation
    for mnenomic in MNEMONICS:
        if after == runOperation(before, operation, mnenomic):
            if -opCode not in opCodes[mnenomic]:
                opCodes[mnenomic].add(opCode)
            count += 1
        elif opCode in opCodes[mnenomic]:
            opCodes[mnenomic].remove(opCode)
            opCodes[mnenomic].add(-opCode)
    return count


def solve(puzzleInput: Tuple[List[Record], List[Operation]]) -> Tuple[int, int]:
    records, program = puzzleInput
    opCodes = {mnemonic: set() for mnemonic in MNEMONICS}
    threeOrMore = 0
    for before, operation, after in records:
        if testRecord(before, operation, after, opCodes) >= 3:
            threeOrMore += 1
    for mnemonic, valid in opCodes.items():
        opCodes[mnemonic] = {op for op in valid if op >= 0}
    while any(len(valid) > 1 for valid in opCodes.values()):
        singleValid = [next(iter(valid))
                       for valid in opCodes.values() if len(valid) == 1]
        for _, valid in opCodes.items():
            if len(valid) > 1:
                for single in singleValid:
                    if single in valid:
                        valid.remove(single)
    ops = {next(iter(valid)): mnemonic for mnemonic, valid in opCodes.items()}
    registers = (0, 0, 0, 0)
    for op in program:
        registers = runOperation(registers, op, ops[op[0]])
    return threeOrMore, registers[0]


recordRegex = re.compile(
    r"Before: \[(?P<b0>\d+), (?P<b1>\d+), (?P<b2>\d+), (?P<b3>\d+)]\n(?P<opCode>\d+) (?P<A>\d) (?P<B>\d) (?P<C>\d)\nAfter:  \[(?P<a0>\d+), (?P<a1>\d+), (?P<a2>\d+), (?P<a3>\d+)]")
operationRegex = re.compile(r"(?P<opCode>\d+) (?P<A>\d) (?P<B>\d) (?P<C>\d)")


def getInput(filePath: str) -> Tuple[List[Record], List[Operation]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        recordsText, programText = file.read().split("\n\n\n\n")
        records: List[Record] = []
        for match in recordRegex.finditer(recordsText):
            records.append((
                (int(match.group("b0")), int(match.group("b1")),
                 int(match.group("b2")), int(match.group("b3"))),
                (int(match.group("opCode")), int(match.group("A")),
                 int(match.group("B")), int(match.group("C"))),
                (int(match.group("a0")), int(match.group("a1")),
                 int(match.group("a2")), int(match.group("a3")))
            ))
        operations: List[Operation] = []
        for match in operationRegex.finditer(programText):
            operations.append((int(match.group("opCode")), int(
                match.group("A")), int(match.group("B")), int(match.group("C"))))
        return records, operations


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
