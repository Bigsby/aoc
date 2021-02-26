#! /usr/bin/python3

import sys, os, time
from typing import Iterable, List, Tuple
import re, math

Registers = List[int]
Operation = Tuple[str,int,int,int]


def runOperation(registers: Registers, operation: Operation) -> Registers:
    mnemonic, A, B, C = operation
    result = list(registers)
    value = -1
    if   mnemonic == "addr": value = registers[A] + registers[B]
    elif mnemonic == "addi": value = registers[A] + B
    elif mnemonic == "mulr": value = registers[A] * registers[B]
    elif mnemonic == "muli": value = registers[A] * B
    elif mnemonic == "banr": value = registers[A] & registers[B]
    elif mnemonic == "bani": value = registers[A] & B
    elif mnemonic == "borr": value = registers[A] | registers[B]
    elif mnemonic == "bori": value = registers[A] | B
    elif mnemonic == "setr": value = registers[A]
    elif mnemonic == "seti": value = A
    elif mnemonic == "gtir": value = 1 if A > registers[B] else 0
    elif mnemonic == "gtri": value = 1 if registers[A] > B else 0
    elif mnemonic == "gtrr": value = 1 if registers[A] > registers[B] else 0
    elif mnemonic == "eqir": value = 1 if A == registers[B] else 0
    elif mnemonic == "eqri": value = 1 if registers[A] == B else 0
    elif mnemonic == "eqrr": value = 1 if registers[A] == registers[B] else 0 
    result[C] = value
    return result


def part1(data: Tuple[int,List[Operation]]) -> int:
    ip, operations = data
    registers = [0 for _ in range(6)]
    while registers[ip] < len(operations):
        registers = runOperation(registers, operations[registers[ip]])
        registers[ip] += 1
    return registers[0]


def getDivisors(number: int) -> Iterable[int]:
    large_divisors = []
    for i in range(1, int(math.sqrt(number) + 1)):
        if number % i == 0:
            yield i
            if i*i != number:
                large_divisors.append(number // i)
    for divisor in reversed(large_divisors):
        yield divisor
    

VALUE_REGISTER = {
    4: 1,
    3: 2
}
def part2(data: Tuple[int,List[Operation]]) -> int:
    ip, operations = data
    registers = [0 for _ in range(6)]
    registers[0] = 1
    while registers[ip] != 1:
        registers = runOperation(registers, operations[registers[ip]])
        registers[ip] += 1
    return sum(getDivisors(registers[VALUE_REGISTER[ip]]))


def solve(data: Tuple[int,List[Operation]]) -> Tuple[int,int]:
    return (
        part1(data),
        part2(data)
    )


operationRegex = re.compile(r"^(?P<mnemonic>\w+) (?P<A>\d+) (?P<B>\d+) (?P<C>\d+)$")
def getInput(filePath: str) -> Tuple[int,List[Operation]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        lines = file.readlines()
        ip = int(lines[0].split(" ")[1])
        operations = []
        for line in lines[1:]:
            match = operationRegex.match(line)
            if match:
                operations.append((match.group("mnemonic"), int(match.group("A")), int(match.group("B")), int(match.group("C"))))
        return ip, operations


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