import io
import enum
from typing import Final, NamedTuple, Set, List, Optional

_SAMPLE_INPUT_STR = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""


def get_sample_inputs() -> io.TextIOBase:
    return io.StringIO(_SAMPLE_INPUT_STR)


class Operator(enum.Enum):
    nop = enum.auto()
    acc = enum.auto()
    jmp = enum.auto()


class Operation(NamedTuple):
    operator: Operator
    value: int


def parse_line(line: str) -> Operation:
    line_split = line.split(" ")
    assert len(line_split) == 2
    [op_str_raw, val_str] = line_split
    op_str = op_str_raw.strip()
    operator: Operator
    if op_str == "nop":
        operator = Operator.nop
    elif op_str == "acc":
        operator = Operator.acc
    if op_str == "jmp":
        operator = Operator.jmp
    return Operation(
        operator=operator,
        value=int(val_str),
    )


def parse_program(input_file: io.TextIOBase) -> List[Operation]:
    stripped_lines = (line.strip() for line in input_file)
    return [parse_line(line) for line in stripped_lines if line]


def accumulate_until_repeat(program: List[Operation]) -> int:
    acc = 0
    index = 0
    min_index: Final = 0
    max_index: Final = len(program) - 1
    visited: Set[int] = set()
    while index >= min_index and index <= max_index:
        if index in visited:
            break
        visited.add(index)
        operation = program[index]
        operator = operation.operator
        if operator == Operator.nop:
            index += 1
        elif operator == Operator.acc:
            index += 1
            acc += operation.value
        elif operator == Operator.jmp:
            index += operation.value
        else:
            raise ValueError("Unknown operator", operator)
    return acc


def solve_part1(input_file: io.TextIOBase) -> None:
    program = parse_program(input_file)
    print(f"acc at value {accumulate_until_repeat(program)} until end or until repeat")


def accumulate_and_remove_jmp(
    program: List[Operation], jmp_to_nop_index: int
) -> Optional[int]:
    acc = 0
    index = 0
    min_index: Final = 0
    max_index: Final = len(program) - 1
    visited: Set[str] = set()
    while index >= min_index and index <= max_index:
        if index in visited:
            acc = None
            break
        visited.add(index)
        operation = program[index]
        operator = operation.operator
        if operator == Operator.nop or index == jmp_to_nop_index:
            index += 1
        elif operator == Operator.acc:
            index += 1
            acc += operation.value
        elif operator == Operator.jmp:
            index += operation.value
        else:
            raise ValueError("Unknown operator", operator)
    return acc


def solve_part2(input_file):
    program = parse_program(input_file)
    jmp_indexes = [i for i, operation in enumerate(program) if operation.operator == Operator.jmp]
    for jmp_to_nop_index in jmp_indexes:
        result = accumulate_and_remove_jmp(program, jmp_to_nop_index)
        if result is not None:
            print(f"acc: {result} for line {jmp_to_nop_index+1}")


def main() -> None:
    solve_part1(get_sample_inputs())
    with open("./input.txt") as f:
        solve_part1(f)
    solve_part2(get_sample_inputs())
    with open("./input.txt") as f:
        solve_part2(f)


if __name__ == "__main__":
    main()
