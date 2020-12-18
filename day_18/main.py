import io
import re
from typing import Optional, List

_SAMPLE_INPUT_STR = """
1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
"""


def get_sample_inputs() -> io.StringIO:
    return io.StringIO(_SAMPLE_INPUT_STR)


NUM_CHARS = set(str(i) for i in range(10))
OP_PLUS = "+"
OP_MULT = "*"
OPS = (OP_PLUS, OP_MULT)


def find_next_relevant_operator(line: str, start: int, stop: int) -> int:
    paren_nesting = 0
    for i in range(start, stop + 1):
        if line[i] == "(":
            paren_nesting += 1
        if line[i] == ")":
            paren_nesting -= 1
        if paren_nesting == 0 and line[i] in OPS:
            return i
    return None


def operate_part1(left: int, right: int, operator: str) -> int:
    if operator == OP_PLUS:
        return left + right
    elif operator == OP_MULT:
        return left * right
    raise ValueError(f"Invalid operator: {operator}")


def clean_line(line: str):
    cleaned = re.sub(r"\s+", "", line)
    if not re.match(r"^[0-9+-/*()]+$", cleaned):
        raise ValueError("Invalid line")
    return cleaned


def resolve_sub_line_part1(
    line: str, start: Optional[int] = None, stop: Optional[int] = None
) -> int:
    if start is None:
        start = 0
    if stop is None:
        stop = len(line) - 1
    value = 0
    prev_operator = OP_PLUS
    while (
        current_operator_index := find_next_relevant_operator(line, start, stop)
    ) is not None:
        next_value = resolve_sub_line_part1(line, start, current_operator_index - 1)
        value = operate_part1(value, next_value, prev_operator)
        prev_operator = line[current_operator_index]
        start = current_operator_index + 1
    final_value: int
    if line[start] == "(" and line[stop] == ")":
        final_value = resolve_sub_line_part1(line, start + 1, stop - 1)
    else:
        final_value = int(line[start : stop + 1])
    return operate_part2(value, final_value, prev_operator)


def solve_part1(file_obj: io.TextIOBase) -> int:
    stripped_lines = (line.strip() for line in file_obj)
    raw_lines = (line for line in stripped_lines if line)
    s = 0
    for raw_line in raw_lines:
        line = clean_line(raw_line)
        computed = resolve_sub_line_part1(line)
        print(f"{line}={computed}")
        s += computed
    return s

def operate_part2(left: int, right: int, operator: str, mults: List[int]) -> int:
    if operator == OP_PLUS:
        return left + right
    elif operator == OP_MULT:
        mults.append(left)
        return right
    raise ValueError(f"Invalid operator: {operator}")


def resolve_sub_line_part2(
    line: str, start: Optional[int] = None, stop: Optional[int] = None
) -> int:
    if start is None:
        start = 0
    if stop is None:
        stop = len(line) - 1
    value = 1
    prev_operator = OP_MULT
    # Save every multiplication in a list
    mults = []
    while (
        current_operator_index := find_next_relevant_operator(line, start, stop)
    ) is not None:
        next_value = resolve_sub_line_part2(line, start, current_operator_index - 1)
        old_value = value
        value = operate_part2(value, next_value, prev_operator, mults)
        prev_operator = line[current_operator_index]
        start = current_operator_index + 1
    final_value: int
    if line[start] == "(" and line[stop] == ")":
        final_value = resolve_sub_line_part2(line, start + 1, stop - 1)
    else:
        final_value = int(line[start : stop + 1])
    final_result = operate_part2(value, final_value, prev_operator, mults)
    for mult in mults:
        final_result *= mult
    return final_result


def solve_part2(file_obj: io.TextIOBase) -> int:
    stripped_lines = (line.strip() for line in file_obj)
    raw_lines = (line for line in stripped_lines if line)
    s = 0
    for raw_line in raw_lines:
        line = clean_line(raw_line)
        computed = resolve_sub_line_part2(line)
        print(f"{line}={computed}")
        s += computed
    return s



def main():
    # print(f"Sample: {solve_part1(get_sample_inputs())}")
    # with open("./inputs.txt") as f:
        # print(f"Actual: {solve_part1(f)}")
    print(f"Sample: {solve_part2(get_sample_inputs())}")
    with open("./inputs.txt") as f:
        print(f"Actual: {solve_part2(f)}")


if __name__ == "__main__":
    main()
