import enum
from typing import List


SAMPLE_INPUTS = """
..##.........##.........##.........##.........##.........##.......
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#
"""

with open("./input.txt") as f:
    ACTUAL_INPUTS = f.read()


class Square(enum.Enum):
    empty = enum.auto()
    tree = enum.auto()


def row_char_to_square(char: str) -> Square:
    if char == "#":
        return Square.tree
    elif char == ".":
        return Square.empty
    raise ValueError(f"Unknown character {char}")


def render_row(raw_row_str: str) -> List[Square]:
    return [row_char_to_square(char) for char in raw_row_str.strip()]


def input_str_to_rows(input_str: str) -> List[List[Square]]:
    return [render_row(raw_line) for raw_line in input_str.strip().split("\n")]


def general_solution(rows: List[List[Square]], *, right: int, down: int) -> int:
    row_index = 0
    col_index = 0
    num_trees = 0
    while row_index < len(rows) - 1:
        row_index += down
        col_index += right
        row = rows[row_index]
        # % handles the pacman effect here
        square = row[col_index % len(row)]
        if square == Square.tree:
            num_trees += 1
    return num_trees


def part1_solution(input_str: str) -> int:
    rows = input_str_to_rows(input_str)
    return general_solution(rows, right=3, down=1)


def part2_solution(input_str: str) -> int:
    rows = input_str_to_rows(input_str)
    return (
        general_solution(rows, right=1, down=1)
        * general_solution(rows, right=3, down=1)
        * general_solution(rows, right=5, down=1)
        * general_solution(rows, right=7, down=1)
        * general_solution(rows, right=1, down=2)
    )


def main() -> None:
    print("---Sample Part 1---")
    print(f"{part1_solution(SAMPLE_INPUTS)} trees encountered")
    print("---Actual Part 1---")
    print(f"{part1_solution(ACTUAL_INPUTS)} trees encountered")
    print("---Sample Part 2---")
    print(f"{part2_solution(SAMPLE_INPUTS)} trees encountered")
    print("---Actual Part 2---")
    print(f"{part2_solution(ACTUAL_INPUTS)} trees encountered")


if __name__ == "__main__":
    main()
