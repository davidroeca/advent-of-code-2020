import io
import re
from queue import Queue
from typing import Dict, Literal, Optional, Union, Tuple

BITS = 36
BinaryChar = Union[Literal["0"], Literal["1"]]
_SAMPLE_PART_1_INPUT_STRING = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""


def get_sample_part_1_inputs():
    return io.StringIO(_SAMPLE_PART_1_INPUT_STRING)

_SAMPLE_PART_2_INPUT_STRING = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

def get_sample_part_2_inputs():
    return io.StringIO(_SAMPLE_PART_2_INPUT_STRING)


def int_to_binary_string(num: int):
    return bin(num)[2:].zfill(BITS)


def iter_mask_update_indeces(mask: str) -> Tuple[int, BinaryChar]:
    if len(mask) != BITS:
        raise ValueError(f"Invalid mask '{mask}'")
    for i, char in enumerate(mask):
        if char in ("0", "1"):
            yield (i, char)
        elif char != "X":
            raise ValueError(f"Invalid character {char} in mask")


class MemoryBase:
    def __init__(self) -> None:
        # Initialize to entire pass-through mask
        self.mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.registers: Dict[int, int] = {}

    def get_sum_of_registers(self) -> int:
        return sum(self.registers.values())

    def set_mem_address(self, address: int, value: int):
        raise NotImplemented


class MemoryPart1(MemoryBase):
    def set_mem_address(self, address: int, value: int):
        val_bin = int_to_binary_string(value)
        new_bin_str = "".join(
            [
                char if self.mask[index] == "X" else self.mask[index]
                for index, char in enumerate(val_bin)
            ]
        )
        self.registers[address] = int(new_bin_str, 2)


class MemoryPart2(MemoryBase):
    def set_mem_address(self, address: int, value: int):
        address_bin = int_to_binary_string(address)
        address_scrambled = "".join(
            [
                char
                if self.mask[index] == "0"
                else "1"
                if self.mask[index] == "1"
                else "X"
                for index, char in enumerate(address_bin)
            ]
        )
        last_address_bit = address_scrambled[BITS - 1]
        address_candidates = (
            ["1", "0"] if last_address_bit == "X" else [last_address_bit]
        )
        for rev_index in range(BITS - 1):
            index = BITS - 2 - rev_index
            bit = address_scrambled[index]
            if bit == "X":
                address_candidates = [
                    *[candidate + "1" for candidate in address_candidates],
                    *[candidate + "0" for candidate in address_candidates],
                ]
            else:
                address_candidates = [
                    candidate + bit for candidate in address_candidates
                ]
        for address_candidate in address_candidates:
            self.registers[int(address_candidate, 2)] = value


def apply_line(line_raw: str, memory: MemoryBase):
    line = line_raw.strip()
    if not line:
        return
    mem_match = re.match(r"mem\[[1-9][0-9]*\]\s*=", line)
    if mem_match:
        mem_group_str = mem_match.group(0)
        mem_address_str = re.sub(r"(^mem\[|\]\s*=$)", "", mem_group_str)
        mem_address = int(mem_address_str)
        new_mem_value_str = re.sub(r"mem\[[1-9][0-9]*\]\s*=", "", line)
        new_mem_value = int(new_mem_value_str)
        memory.set_mem_address(mem_address, new_mem_value)
    elif re.match(r"mask\s*=", line):
        new_mask_raw = re.sub(r"^mask\s*=", "", line)
        new_mask = new_mask_raw.strip()
        memory.mask = new_mask
    else:
        raise ValueError(f'Invalid line "{line_raw}"')


def solve_part1(file_obj) -> int:
    memory = MemoryPart1()
    for line in file_obj:
        apply_line(line, memory)
    return memory.get_sum_of_registers()

def solve_part2(file_obj) -> int:
    memory = MemoryPart2()
    for line in file_obj:
        apply_line(line, memory)
    return memory.get_sum_of_registers()


def main():
    print("---Sample Part 1---")
    print(f"Total Sum: {solve_part1(get_sample_part_1_inputs())}")
    print("---Actual Part 1---")
    with open("./input.txt") as f:
        print(f"Total Sum: {solve_part1(f)}")
    print("---Sample Part 2---")
    print(f"Total Sum: {solve_part2(get_sample_part_2_inputs())}")
    print("---Actual Part 2---")
    with open("./input.txt") as f:
        print(f"Total Sum: {solve_part2(f)}")


if __name__ == "__main__":
    main()
