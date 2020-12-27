from __future__ import annotations
import io
from itertools import chain
from typing import Dict, List, Set, Deque, Iterable

_SAMPLE_INPUT_STR = """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""


def get_sample_inputs() -> io.StringIO:
    return io.StringIO(_SAMPLE_INPUT_STR)


DEFAULT_SEAMONSTER = [
    [
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
        False,
    ],
    [
        True,
        False,
        False,
        False,
        False,
        True,
        True,
        False,
        False,
        False,
        False,
        True,
        True,
        False,
        False,
        False,
        False,
        True,
        True,
        True,
    ],
    [
        False,
        True,
        False,
        False,
        True,
        False,
        False,
        True,
        False,
        False,
        True,
        False,
        False,
        True,
        False,
        False,
        True,
        False,
        False,
        False,
    ],
]


class TileContainer:
    internal_list: List[List[bool]]

    @property
    def top(self) -> List[bool]:
        return self.internal_list[0]

    @property
    def bottom(self) -> List[bool]:
        return self.internal_list[-1]

    @property
    def left(self) -> List[bool]:
        return [row[0] for row in self.internal_list]

    @property
    def right(self) -> List[bool]:
        return [row[-1] for row in self.internal_list]

    def rotate_clockwise(self) -> None:
        self.internal_list = [list(reversed(col)) for col in zip(*self.internal_list)]

    def flip_horizontal(self) -> None:
        self.internal_list = [list(reversed(col)) for col in self.internal_list]

    def flip_vertical(self) -> None:
        self.internal_list = list(reversed(self.internal_list))


class Seamonster(TileContainer):
    def __init__(self, internal_list: Optional[List[List[bool]]] = None) -> None:
        if internal_list is None:
            self.internal_list = DEFAULT_SEAMONSTER

    def overlaps(self, sub_picture: List[List[bool]]) -> int:
        count = 0
        for j, row in enumerate(self.internal_list):
            for i, col in enumerate(row):
                if col and not sub_picture[j][i]:
                    return False
        return True

    def count_in_picture(self, picture: List[List[bool]]) -> int:
        height = len(self.internal_list)
        width = len(self.internal_list[0])
        count = 0
        i = 0
        j = 0
        while j < len(picture) - height:
            if self.overlaps([row[i : i + width] for row in picture[j : j + height]]):
                count += 1
            i += 1
            if i >= len(picture[0]) - width:
                j += 1
                i = 0
        return count


class Tile(TileContainer):
    def __init__(self, tile_id: int) -> None:
        self.tile_id = tile_id
        self.internal_list: List[List[bool]] = []

    def process_line(self, line: str) -> None:
        self.internal_list.append([c == "#" for c in line])

    def validate(self) -> None:
        if len(self.top) != len(self.bottom) or len(self.left) != len(self.right):
            raise ValueError("All sides must be equal")


def iter_tiles(file_obj: io.TextIOBase) -> Iterable[Tile]:
    stripped_lines = (line.strip() for line in file_obj)
    actual_lines = (line for line in stripped_lines if line)
    tile = None
    for line in actual_lines:
        if line.startswith("Tile"):
            if tile is not None:
                tile.validate()
                yield tile
            tile_id = line.replace("Tile", "").replace(":", "")
            tile = Tile(tile_id=int(tile_id))
        else:
            tile.process_line(line)
    tile.validate()
    yield tile


def check_insertion(
    tile: Tile,
    left_tile: Optional[Tile] = None,
    right_tile: Optional[Tile] = None,
    top_tile: Optional[Tile] = None,
    bottom_tile: Optional[Tile] = None,
) -> bool:
    if (
        left_tile is None
        and right_tile is None
        and top_tile is None
        and bottom_tile is None
    ):
        return False
    return (
        (left_tile is None or left_tile.right == tile.left)
        and (right_tile is None or right_tile.left == tile.right)
        and (top_tile is None or top_tile.bottom == tile.top)
        and (bottom_tile is None or bottom_tile.top == tile.bottom)
    )


def add_single_tile_orientation_to_grid(
    tile: Tile, grid: List[List[Optional[Tile]]]
) -> bool:
    # Handle top row
    for col_index, bottom_tile in enumerate(grid[0]):
        if check_insertion(tile, bottom_tile=bottom_tile):
            grid.insert(
                0, [tile if col_index == i else None for i in range(len(grid[0]))]
            )
            return True
    # Handle bottom row
    for col_index, top_tile in enumerate(grid[-1]):
        if check_insertion(tile, top_tile=top_tile):
            grid.append(
                [tile if col_index == i else None for i in range(len(grid[-1]))]
            )
            return True
    num_rows = len(grid)
    for row_index, row in enumerate(grid):
        # Handle left column
        right_tile = row[0]
        if check_insertion(tile, right_tile=right_tile):
            for index_to_update, row_to_update in enumerate(grid):
                if row_index == index_to_update:
                    row_to_update.insert(0, tile)
                else:
                    row_to_update.insert(0, None)
            return True
        # Handle right column side
        right_index = len(row) - 1
        if check_insertion(
            tile,
            left_tile=row[right_index],
            top_tile=None if row_index == 0 else grid[row_index - 1][right_index],
            bottom_tile=(
                None if row_index == num_rows - 1 else grid[row_index + 1][right_index]
            ),
        ):
            for index_to_update, row_to_update in enumerate(grid):
                if index_to_update == row_index:
                    row_to_update.append(tile)
                else:
                    row_to_update.append(None)
            return True
        # Handle hole in middle
        for col_index, slot in enumerate(row):
            if slot is None:
                left_tile = None if col_index == 0 else row[col_index - 1]
                right_tile = None if col_index == len(row) - 1 else row[col_index + 1]
                top_tile = None if row_index == 0 else grid[row_index - 1][col_index]
                bottom_tile = (
                    None
                    if row_index == num_rows - 1
                    else grid[row_index + 1][col_index]
                )
                if check_insertion(
                    tile,
                    left_tile=left_tile,
                    right_tile=right_tile,
                    top_tile=top_tile,
                    bottom_tile=bottom_tile,
                ):
                    row[col_index] = tile
                    return True
    return False


def add_rotations_to_grid(tile: Tile, grid: List[List[Optional[Tile]]]) -> bool:
    if add_single_tile_orientation_to_grid(tile, grid):
        return True
    tile.rotate_clockwise()
    if add_single_tile_orientation_to_grid(tile, grid):
        return True
    tile.rotate_clockwise()
    if add_single_tile_orientation_to_grid(tile, grid):
        return True
    tile.rotate_clockwise()
    if add_single_tile_orientation_to_grid(tile, grid):
        return True
    return False


def add_to_grid(tile: Tile, grid: List[List[Optional[Tile]]]) -> bool:
    if add_rotations_to_grid(tile, grid):
        return True
    tile.flip_horizontal()
    if add_rotations_to_grid(tile, grid):
        return True
    tile.flip_vertical()
    if add_rotations_to_grid(tile, grid):
        return True
    tile.flip_horizontal()
    if add_rotations_to_grid(tile, grid):
        return True
    return False


def create_grid(file_obj: io.TextIOBase) -> List[List[Tile]]:
    tiles = Deque(iter_tiles(file_obj))
    grid: List[List[Optional[Tile]]] = [[tiles.pop()]]
    while tiles:
        tile = tiles.pop()
        if not add_to_grid(tile, grid):
            tiles.appendleft(tile)
    return [[item for item in row if item is not None] for row in grid]


def solve_part1(file_obj: io.TextIOBase) -> int:
    grid = create_grid(file_obj)
    return (
        grid[0][0].tile_id
        * grid[0][-1].tile_id
        * grid[-1][0].tile_id
        * grid[-1][-1].tile_id
    )


def count_seamonster_rotations_in_picture(
    seamonster: Seamonster, picture: List[List[bool]]
) -> int:
    count = max(0, seamonster.count_in_picture(picture))
    seamonster.rotate_clockwise()
    count = max(count, seamonster.count_in_picture(picture))
    seamonster.rotate_clockwise()
    count = max(count, seamonster.count_in_picture(picture))
    seamonster.rotate_clockwise()
    count = max(count, seamonster.count_in_picture(picture))
    return count


def count_seamonsters_in_picture(
    seamonster: Seamonster, picture: List[List[bool]]
) -> int:
    count = max(0, count_seamonster_rotations_in_picture(seamonster, picture))
    seamonster.flip_horizontal()
    count = max(count, count_seamonster_rotations_in_picture(seamonster, picture))
    seamonster.flip_vertical()
    count = max(count, count_seamonster_rotations_in_picture(seamonster, picture))
    seamonster.flip_horizontal()
    count = max(count, count_seamonster_rotations_in_picture(seamonster, picture))
    return count


def solve_part2(file_obj: io.TextIOBase):
    grid = create_grid(file_obj)
    picture = []
    for tile_row in grid:
        piece_iter = (
            [row[1:-1] for row in tile.internal_list[1:-1]] for tile in tile_row
        )
        rows = [list(chain.from_iterable(item)) for item in zip(*piece_iter)]
        picture.extend(rows)
    seamonster = Seamonster()
    count = count_seamonsters_in_picture(seamonster, picture)
    total_trues = sum(1 for row in picture for item in row if item)
    return total_trues - count * sum(
        1 for row in seamonster.internal_list for item in row if item
    )


def main():
    print("---Sample inputs---")
    print(f"Product: {solve_part1(get_sample_inputs())}")
    print("---Actual inputs---")
    with open("./inputs.txt") as f:
        print(f"Product: {solve_part1(f)}")
    print("---Sample inputs Part 2---")
    print(f"Product: {solve_part2(get_sample_inputs())}")
    print("---Actual inputs Part 2---")
    with open("./inputs.txt") as f:
        print(f"Product: {solve_part2(f)}")


if __name__ == "__main__":
    main()
