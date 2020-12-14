import io
import re
from typing import NamedTuple, List, Optional, Iterable


class BoardingPass(NamedTuple):
    row: int
    column: int
    seat_id: int


def binary_search_from_top_codes(
    top_code_list: List[bool], min_value: int, max_value: int
) -> int:
    if len(top_code_list) == 0:
        assert min_value == max_value, f"{min_value} should equal {max_value}"
        return min_value
    next_is_top = top_code_list[0]
    next_top_code_list = top_code_list[1:]
    num_values = max_value - min_value + 1
    new_num_values = num_values // 2
    if next_is_top:
        return binary_search_from_top_codes(
            next_top_code_list,
            min_value=min_value,
            max_value=min_value + new_num_values - 1,
        )
    return binary_search_from_top_codes(
        next_top_code_list, min_value=min_value + new_num_values, max_value=max_value
    )


BP_REGEX = re.compile(r"^[BF]{7}[LR]{3}$")


def decode_boarding_pass(raw_bp_str: str) -> BoardingPass:
    bp_str = raw_bp_str.strip()

    assert BP_REGEX.match(bp_str), "Invalid boarding pass"
    row_is_front_list = [row == "F" for row in raw_bp_str[:7]]
    col_is_left_list = [col == "L" for col in raw_bp_str[7:]]
    row = binary_search_from_top_codes(row_is_front_list, min_value=0, max_value=127)
    col = binary_search_from_top_codes(col_is_left_list, min_value=0, max_value=7)
    return BoardingPass(
        row=row,
        column=col,
        seat_id=row * 8 + col,
    )


def iter_boarding_passes(file_obj: io.TextIOBase) -> Iterable[BoardingPass]:
    for line in file_obj:
        yield decode_boarding_pass(line)


def find_highest_boarding_pass(file_obj: io.TextIOBase) -> BoardingPass:
    best_boarding_pass: Optional[BoardingPass] = None
    for boarding_pass in iter_boarding_passes(file_obj):
        if (
            best_boarding_pass is None
            or boarding_pass.seat_id > best_boarding_pass.seat_id
        ):
            best_boarding_pass = boarding_pass
    if best_boarding_pass is None:
        raise ValueError("No boarding pass found")
    return best_boarding_pass


def iter_missing_middle_seat_ids(file_obj: io.TextIOBase) -> BoardingPass:
    seen_seat_ids = set(bp.seat_id for bp in iter_boarding_passes(file_obj))
    for row in range(128):
        for col in range(8):
            seat_id = row * 8 + col
            if (
                seat_id not in seen_seat_ids
                and seat_id + 1 in seen_seat_ids
                and seat_id - 1 in seen_seat_ids
            ):
                yield seat_id


def main():
    print("---Part 1---")
    with open("./input.txt") as f:
        boarding_pass = find_highest_boarding_pass(f)
    print(
        f"Highest seat ID: {boarding_pass.seat_id}. Row: {boarding_pass.row}, Column: {boarding_pass.column}."
    )
    print("---Part 2---")
    print("All missing middle seat ids:")
    with open("./input.txt") as f:
        for missing_id in iter_missing_middle_seat_ids(f):
            print(missing_id)


if __name__ == "__main__":
    main()
