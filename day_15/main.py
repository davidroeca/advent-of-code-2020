from typing import Iterable, List, TypeVar

SAMPLE_INPUT_ARRAYS = [
    # Samples
    # [0, 3, 6],
    [1, 3, 2],
    [2, 1, 3],
    [1, 2, 3],
    [2, 3, 1],
    [3, 2, 1],
    [3, 1, 2],
    # Puzzle
    [9, 6, 0, 10, 18, 2, 1],
]

T = TypeVar("T")


def rev_iter(items: List[T], skip_last=0) -> Iterable[T]:
    length = len(items)
    for i in range(length - skip_last):
        yield items[length - skip_last - 1 - i]


def find_nth_number(history_in: List[int], n: int) -> int:
    next_value = history_in[-1]
    history = {value: index for index, value in enumerate(history_in[:-1], start=1)}
    # THe last iteration saves next_value which is the nth value since the last
    # iteration is n-1
    for i in range(len(history_in), n):
        previous_index = history.get(next_value)
        history[next_value] = i
        next_value = 0 if previous_index is None else i - previous_index
    return next_value


def find_2020th_number(history_in: List[int]) -> int:
    return find_nth_number(history_in, 2020)


def main():
    for sample_input in SAMPLE_INPUT_ARRAYS:
        print(find_2020th_number(sample_input))
    for sample_input in SAMPLE_INPUT_ARRAYS:
        print(find_nth_number(sample_input, 30000000))


if __name__ == "__main__":
    main()
