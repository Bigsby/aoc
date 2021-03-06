#! /usr/bin/python3

import sys
import os
import time
from typing import Callable, Dict, List, Tuple, Union
import re

SCALAR, WIRE = "scalar", "wire"
INPUT, NOT, BINARY = "input", "not", "binary"


class Operand():
    def __init__(self, value: str):
        try:
            self.type = SCALAR
            self.scalar = int(value)
        except:
            self.type = WIRE
            self.wire: str = value


class Connection():
    def __init__(self, operation: Union[str, None], type: str, operand1: str, operand2: Union[str, None], target: str):
        self.operation = operation
        self.type = type
        self.operand1 = Operand(operand1)
        self.operand2 = Operand(operand2) if operand2 else None
        self.target = target


BINARY_OPERATIONS: Dict[str, Callable[[int, int], int]] = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "LSHIFT": lambda x, y: x << y,
    "RSHIFT": lambda x, y: x >> y
}
class Circuit():
    def __init__(self, connections: List[Connection]):
        self.connections = connections
        self.solutions: Dict[str, int] = {}

    def get_connection_from_target(self, target: str) -> Connection:
        return next(filter(lambda conn: conn.target == target, self.connections))

    def get_value_from_operand(self, operand: Operand) -> int:
        if operand.type == SCALAR:
            return operand.scalar
        return self.get_value_from_connection(self.get_connection_from_target(operand.wire))

    def get_value_from_binary_connection(self, connection: Connection) -> int:
        if connection.operation and connection.operand2:
            operation = BINARY_OPERATIONS[connection.operation]
            return operation(self.get_value_from_operand(connection.operand1), self.get_value_from_operand(connection.operand2))
        raise Exception("Operation no defined in connection")

    def calculate_value_for_connection(self, connection: Connection) -> int:
        if connection.type == INPUT:
            return self.get_value_from_operand(connection.operand1)
        if connection.type == NOT:
            return ~self.get_value_from_operand(connection.operand1)
        if connection.type == BINARY:
            return self.get_value_from_binary_connection(connection)
        raise Exception("Unknown operation:", connection)

    def get_value_from_connection(self, connection: Connection) -> int:
        if connection.target in self.solutions:
            return self.solutions[connection.target]
        result = self.calculate_value_for_connection(connection)
        self.solutions[connection.target] = result
        return result

    def solve_for(self, target: str, initialState: Dict[str, int] = {}) -> int:
        self.solutions = initialState
        return self.get_value_from_connection(self.get_connection_from_target(target))


def solve(circuit: Circuit) -> Tuple[int, int]:
    starting_target = "a"
    part1 = circuit.solve_for(starting_target)
    part2 = circuit.solve_for(starting_target, {"b": part1})
    return part1, part2


source_target_regex = re.compile(r"^(.*)\s->\s(\w+)$")
input_regex = re.compile(r"^[^\s]+$")
unary_regex = re.compile(r"NOT\s(\w+)$")
binary_regex = re.compile(r"^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)")
def process_line(line: str) -> Connection:
    source_target_match = source_target_regex.match(line)
    if source_target_match:
        source, target = source_target_match.group(1, 2)
        if input_regex.match(source):
            return Connection(None, INPUT, source, None, target)
        unary_match = unary_regex.match(source)
        if unary_match:
            return Connection(None, NOT, unary_match.group(1), None, target)
        binary_match = binary_regex.match(source)
        if binary_match:
            return Connection(binary_match.group(2), BINARY, binary_match.group(1), binary_match.group(3), target)
        raise Exception("Unrecognized operation:", source)
    else:
        raise Exception("Unrecognized operation line:", line)


def get_input(file_path: str) -> Circuit:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return Circuit([process_line(line) for line in file.readlines()])


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
