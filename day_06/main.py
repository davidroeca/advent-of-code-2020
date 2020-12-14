import io
from typing import Iterator, List

SAMPLE_INPUTS_STR = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""


def get_sample_inputs():
    return io.StringIO(SAMPLE_INPUTS_STR)


def gen_group_answers(file_obj: io.TextIOBase) -> Iterator[List[str]]:
    next_answers: List[str] = []
    for line_raw in file_obj:
        line = line_raw.strip()
        if not line:
            if next_answers:
                yield next_answers
                next_answers = []
        else:
            next_answers.append(line)
    if next_answers:
        yield next_answers


def solve_part_1(file_obj: io.TextIOBase) -> int:
    total = 0
    for group_answers in gen_group_answers(file_obj):
        unique_answers = set(char for answer in group_answers for char in answer)
        total += len(unique_answers)
    return total

def solve_part_2(file_obj: io.TextIOBase) -> int:
    total = 0
    for group_answers in gen_group_answers(file_obj):
        first_answer = group_answers[0]
        consensus = set(first_answer)
        for answer in group_answers[1:]:
            consensus = consensus & set(answer)
        total += len(consensus)
    return total

def main():
    print("---Sample Part 1---")
    print(f"Answer: {solve_part_1(get_sample_inputs())}")
    print("---Actual Part 1---")
    with open("./input.txt") as f:
        print(f"Answer: {solve_part_1(f)}")
    print("---Sample Part 2---")
    print(f"Answer: {solve_part_2(get_sample_inputs())}")
    print("---Actual Part 2---")
    with open("./input.txt") as f:
        print(f"Answer: {solve_part_2(f)}")


if __name__ == "__main__":
    main()
