#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List
from enum import Enum

class PacketTypes(Enum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    Literal = 4
    Greater = 5
    Less = 6
    Equal = 7

Input = str
Packet = Tuple[int, PacketTypes, int, List["Packet"]]


def get_n_bits(message: str, count: int) -> Tuple[int, str]:
    return int(message[:count], 2), message[count:]


def get_sub_packets(message: str) -> Tuple[List[Packet], str]:
    length_id, message = get_n_bits(message, 1)
    sub_packets: List[Packet] = []
    if length_id:
        packet_count, message = get_n_bits(message, 11)
        for _ in range(packet_count):
            sub_packet, message = get_packet(message)
            sub_packets.append(sub_packet)
    else:
        sub_packets_length, message = get_n_bits(message, 15)
        starting_length = len(message)
        while starting_length - len(message) < sub_packets_length:
            sub_packet, message = get_packet(message)
            sub_packets.append(sub_packet)
    return sub_packets, message
    

def get_packet(message: str) -> Tuple[Packet, str]:
    version, message = get_n_bits(message, 3)
    type, message = get_n_bits(message, 3)
    if type == 4:
        value = 0
        while True:
            not_final, message = get_n_bits(message, 1)
            partial, message = get_n_bits(message, 4)
            value = (value << 4) + partial
            if not not_final:
                break
        return (version, PacketTypes(type), value, []), message
    else:
        sub_packets, message = get_sub_packets(message)
        return (version, PacketTypes(type), 0, sub_packets), message
    

def get_packet_value(packet: Packet) -> int:
    _, type, value, sub_packets = packet
    if type == PacketTypes.Literal:
        return value
    if type == PacketTypes.Sum:
        value = 0
        for sub_packet in sub_packets:
            value += get_packet_value(sub_packet)
        return value
    if type == PacketTypes.Product:
        value = 1
        for sub_packet in sub_packets:
            value *= get_packet_value(sub_packet)
        return value
    if type == PacketTypes.Minimum:
        value = sys.maxsize
        for sub_packet in sub_packets:
            sub_packet_value = get_packet_value(sub_packet)
            value = value if value < sub_packet_value else sub_packet_value
        return value
    if type == PacketTypes.Maximum:
        value = 0
        for sub_packet in sub_packets:
            sub_packet_value = get_packet_value(sub_packet)
            value = value if value > sub_packet_value else sub_packet_value
        return value
    if type == PacketTypes.Greater:
        return 1 if get_packet_value(sub_packets[0]) > get_packet_value(sub_packets[1]) else 0
    if type == PacketTypes.Less:
        return 1 if get_packet_value(sub_packets[0]) < get_packet_value(sub_packets[1]) else 0
    if type == PacketTypes.Equal:
        return 1 if get_packet_value(sub_packets[0]) == get_packet_value(sub_packets[1]) else 0
    raise Exception(f"Unknow type {type}")


def get_packet_version_sum(packet: Packet) -> int:
    version, _, _, sub_packets = packet
    for sub_packet in sub_packets:
        version += get_packet_version_sum(sub_packet)
    return version


def solve(message: Input) -> Tuple[int,int]:
    packet, message = get_packet(message)
    return get_packet_version_sum(packet), get_packet_value(packet)


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        contents = file.read().strip()
        message = ""
        for index in range(0, len(contents) - 1, 2):
            message += f"{int(contents[index:index + 2], 16):08b}"
        return message


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
