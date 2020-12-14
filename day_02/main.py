from typing import NamedTuple, List, Iterator

SAMPLE_INPUTS = ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]
with open("./input.txt") as INPUTS_FILE:
    ACTUAL_INPUTS = [line.strip() for line in INPUTS_FILE]


class PasswordInput(NamedTuple):
    num1: int
    num2: int
    char: str
    password: str


def validate_part_1_password_input(password_input: PasswordInput) -> bool:
    count = sum(1 for c in password_input.password if c == password_input.char)
    return count >= password_input.num1 and count <= password_input.num2


def validate_part_2_password_input(password_input: PasswordInput) -> bool:
    password = password_input.password
    length = len(password)
    in_first_position = (
        password_input.num1 <= length
        and password[password_input.num1 - 1] == password_input.char
    )
    in_second_position = (
        password_input.num2 <= length
        and password[password_input.num2 - 1] == password_input.char
    )
    return (
        in_first_position
        and not in_second_position
        or in_second_position
        and not in_first_position
    )


def parse_password_input(raw_password_input: str) -> PasswordInput:
    input_split = raw_password_input.split(":")
    assert len(input_split) == 2, "Must be colon-separated password spec"
    [spec, password_unclean] = input_split
    spec_split = spec.split(" ")
    assert len(spec_split) == 2, "Left-hand side must be space separated spec"
    [num_spec, char_unclean] = spec_split
    char = char_unclean.strip()
    assert len(char) == 1, "char must be of length 1"
    num_spec_split = num_spec.split("-")
    assert len(num_spec_split) == 2, "There must be a max and min number separated by -"
    [num1_str, num2_str] = num_spec_split
    return PasswordInput(
        num1=int(num1_str.strip()),
        num2=int(num2_str.strip()),
        char=char,
        password=password_unclean.strip(),
    )


def gen_password_inputs(inputs: List[str]) -> Iterator[PasswordInput]:
    for input_str in inputs:
        yield parse_password_input(input_str)


def count_valid_part_1_password_policies(inputs: List[str]) -> int:
    return sum(
        1
        for password_input in gen_password_inputs(inputs)
        if validate_part_1_password_input(password_input)
    )


def count_valid_part_2_password_policies(inputs: List[str]) -> int:
    return sum(
        1
        for password_input in gen_password_inputs(inputs)
        if validate_part_2_password_input(password_input)
    )


def print_part_1_solution(inputs: List[str]) -> None:
    print(f"{count_valid_part_1_password_policies(inputs)} valid passwords")


def print_part_2_solution(inputs: List[str]) -> None:
    print(f"{count_valid_part_2_password_policies(inputs)} valid passwords")


def main() -> None:
    print("---Sample Part 1---")
    print_part_1_solution(SAMPLE_INPUTS)
    print("---Actual Part 1---")
    print_part_1_solution(ACTUAL_INPUTS)
    print("---Sample Part 2---")
    print_part_2_solution(SAMPLE_INPUTS)
    print("---Actual Part 2---")
    print_part_2_solution(ACTUAL_INPUTS)


if __name__ == "__main__":
    main()
