from typing import List, Iterator, Tuple

SAMPLE_INPUTS = [
    1721,
    979,
    366,
    299,
    675,
    1456,
]

with open("./input.txt") as f:
    ACTUAL_INPUTS = [int(line.strip()) for line in f]


def gen_two_entries_sum_2020(inputs: List[int]) -> Iterator[Tuple[int, int]]:
    sorted_inputs = sorted(inputs)
    length = len(sorted_inputs)
    i = 0
    while i < length - 2 and sorted_inputs[i] <= 2020 / 2:
        for j in range(i + 1, length):
            vi = sorted_inputs[i]
            vj = sorted_inputs[j]
            sum_vals = vi + vj
            if sum_vals == 2020:
                yield vi, vj
            elif sum_vals > 2020:
                break
        i += 1


def print_part_1_solution(inputs: List[int]) -> None:
    for vi, vj in gen_two_entries_sum_2020(inputs):
        print(f"{vi} * {vj} = {vi * vj}")


def gen_three_entries_sum_2020(inputs: List[int]) -> Iterator[Tuple[int, int]]:
    sorted_inputs = sorted(inputs)
    length = len(sorted_inputs)
    i = 0
    while i < length - 2 and sorted_inputs[i] <= 2020 / 2:
        for j in range(i + 1, length):
            should_break = False
            for k in range(j + 1, length):
                vi = sorted_inputs[i]
                vj = sorted_inputs[j]
                vk = sorted_inputs[k]
                sum_vals = vi + vj + vk
                if sum_vals == 2020:
                    yield vi, vj, vk
                elif sum_vals > 2020:
                    should_break = True
                    break
            if should_break:
                break
        i += 1

def print_part_2_solution(inputs: List[int]) -> None:
    for vi, vj, vk in gen_three_entries_sum_2020(inputs):
        print(f"{vi} * {vj} * {vk} = {vi * vj * vk}")

def main() -> None:
    print("---Samples Part 1---")
    print_part_1_solution(SAMPLE_INPUTS)
    print("---Actual Part 1---")
    print_part_1_solution(ACTUAL_INPUTS)
    print("---Samples Part 2---")
    print_part_2_solution(SAMPLE_INPUTS)
    print("---Actual Part 2---")
    print_part_2_solution(ACTUAL_INPUTS)


if __name__ == "__main__":
    main()
