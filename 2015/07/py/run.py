#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Tuple
from enum import Enum
import re


class Operand():
    @staticmethod
    def parse(value: str) -> 'Operand':
        try:
            return Scalar(int(value))
        except:
            return Wire(value)


class Scalar(Operand):
    def __init__(self, value: int):
        self.value = value


class Wire(Operand):
    def __init__(self, source: str):
        self.source = source


class Operation(Enum):
    AND = 0,
    OR = 1,
    LSHIFT = 2,
    RSHIFT = 3,


class Connection():
    pass


class Input(Connection):
    def __init__(self, operand: Operand) -> None:
        self.operand = operand


class Not(Connection):
    def __init__(self, operand: Operand) -> None:
        self.operand = operand


class Binary(Connection):
    def __init__(self, operand1: Operand, operand2: Operand, operation: Operation):
        self.operand1 = operand1
        self.operand2 = operand2
        self.operation = operation


Connections = Dict[str, Connection]


class Circuit():
    def __init__(self, connections: Connections):
        self.connections = connections
        self.solutions: Dict[str, int] = {}

    def get_value_from_operand(self, operand: Operand) -> int:
        if isinstance(operand, Scalar):
            return operand.value
        if isinstance(operand, Wire):
            return self.get_value_from_connection(operand.source)
        raise Exception(f"Unknown operand '{operand}'")

    def get_value_from_binary_connection(self, connection: Binary) -> int:
        operand1 = self.get_value_from_operand(connection.operand1)
        operand2 = self.get_value_from_operand(connection.operand2)
        if connection.operation == Operation.AND:
            return operand1 & operand2
        if connection.operation == Operation.OR:
            return operand1 | operand2
        if connection.operation == Operation.LSHIFT:
            return operand1 << operand2
        if connection.operation == Operation.RSHIFT:
            return operand1 >> operand2
        raise Exception(
            f"Binary operation no defined in connection '{connection.operation}'")

    def calculate_value_for_connection(self, connection: Connection) -> int:
        if isinstance(connection, Input):
            return self.get_value_from_operand(connection.operand)
        if isinstance(connection, Not):
            return ~self.get_value_from_operand(connection.operand)
        if isinstance(connection, Binary):
            return self.get_value_from_binary_connection(connection)
        raise Exception("Unknown operation:", connection)

    def get_value_from_connection(self, target: str) -> int:
        if target in self.solutions:
            return self.solutions[target]
        result = self.calculate_value_for_connection(self.connections[target])
        self.solutions[target] = result
        return result

    def solve_for(self, target: str, initialState: Dict[str, int] = {}) -> int:
        self.solutions = initialState
        return self.get_value_from_connection(target)


def solve(circuit: Circuit) -> Tuple[int, int]:
    starting_target = "a"
    part1 = circuit.solve_for(starting_target)
    part2 = circuit.solve_for(starting_target, {"b": part1})
    return part1, part2


source_target_regex = re.compile(r"^(.*)\s->\s(\w+)$")
input_regex = re.compile(r"^[^\s]+$")
unary_regex = re.compile(r"NOT\s(\w+)$")
binary_regex = re.compile(r"^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)")


def process_line(line: str) -> Tuple[str, Connection]:
    source_target_match = source_target_regex.match(line)
    if source_target_match:
        source, target = source_target_match.group(1, 2)
        if input_regex.match(source):
            return (target, Input(Operand.parse(source)))
        unary_match = unary_regex.match(source)
        if unary_match:
            return (target, Not(Operand.parse(unary_match.group(1))))
        binary_match = binary_regex.match(source)
        if binary_match:
            return (target, Binary(Operand.parse(binary_match.group(1)), Operand.parse(binary_match.group(3)), Operation[binary_match.group(2)]))
        raise Exception("Unrecognized operation:", source)
    else:
        raise Exception("Unrecognized operation line:", line)


def get_input(file_path: str) -> Circuit:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return Circuit({target: connection for target, connection in map(lambda line: process_line(line), file.readlines())})


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
