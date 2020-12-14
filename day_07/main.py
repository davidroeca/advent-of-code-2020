import io
import re
from typing import Dict, List, Iterator, NamedTuple, Set, Tuple

_SAMPLE_INPUT_STR = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""


def get_sample_inputs() -> io.StringIO:
    return io.StringIO(_SAMPLE_INPUT_STR)


_SAMPLE_2_INPUT_STR = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""


def get_sample_2_inputs() -> io.StringIO:
    return io.StringIO(_SAMPLE_2_INPUT_STR)


class BagSpec(NamedTuple):
    count: int
    name: str


def parse_bag_item(bag_item_raw: str) -> BagSpec:
    bag_item_clean = bag_item_raw.strip()
    name_search = re.search(r"[A-Za-z][A-Za-z ]* bags?$", bag_item_clean)
    if not name_search:
        raise ValueError(f'Error parsing bag name for "{bag_item_raw}"')
    name = re.sub(r" bags?$", "", name_search.group(0))
    count_match = re.match(r"^[1-9][0-9]*", bag_item_clean)
    if not count_match:
        raise ValueError(f'Error parsing number of bags for "{bag_item_raw}"')
    count = int(count_match.group(0))
    return BagSpec(count=count, name=name)


def parse_line(line: str) -> Tuple[str, List[BagSpec]]:
    split_line = line.split(" bags contain ")
    assert len(split_line) == 2, 'One and only one "bags contain" clause per line'
    [name_raw, bag_spec_raw] = split_line
    name = name_raw.strip()
    bag_spec_str = bag_spec_raw.strip().strip(".")
    # Handle the empty bag case
    if bag_spec_str == "no other bags":
        return name, []
    bag_spec_list = [parse_bag_item(bag_item) for bag_item in bag_spec_str.split(",")]
    return name, bag_spec_list


def bag_spec_iter(file_obj: io.TextIOBase) -> Iterator[Tuple[str, List[BagSpec]]]:
    for line_raw in file_obj:
        line = line_raw.strip()
        if line:
            yield parse_line(line)


def construct_bag_dict(file_obj: io.TextIOBase) -> Dict[str, List[BagSpec]]:
    return {name: bag_spec for name, bag_spec in bag_spec_iter(file_obj)}


def search_bag_part1(
    bag_name: str,
    bag_dict: Dict[str, List[BagSpec]],
    seen: Set[str],
    contains_desired_bag: Set[str],
    desired_bag_name: str,
) -> None:
    # Don't repeat a previous search
    if bag_name in seen:
        return
    # Bags don't contain themselves
    if bag_name == desired_bag_name:
        seen.add(bag_name)
        return
    contents = bag_dict[bag_name]
    for bag_spec in contents:
        # Handle if bag has already been seen
        # Handle fresh search
        if bag_spec.name not in seen:
            search_bag_part1(
                bag_spec.name, bag_dict, seen, contains_desired_bag, desired_bag_name
            )
        if bag_spec.name == desired_bag_name or bag_spec.name in contains_desired_bag:
            contains_desired_bag.add(bag_name)
            break
    seen.add(bag_name)


def solve_part1(file_obj: io.TextIOBase) -> Set[str]:
    seen: Set[str] = set()
    contains_shiny_bag: Set[str] = set()
    bag_dict = construct_bag_dict(file_obj)
    for name in bag_dict:
        search_bag_part1(name, bag_dict, seen, contains_shiny_bag, "shiny gold")
    return contains_shiny_bag


def count_bags_in_name(
    bag_name: str,
    bag_dict: Dict[str, List[BagSpec]],
    saved_counts: Dict[str, int],
) -> None:
    if bag_name in saved_counts:
        return
    bag_specs = bag_dict[bag_name]
    total = 0
    for bag_spec in bag_specs:
        if bag_spec.name not in saved_counts:
            count_bags_in_name(bag_spec.name, bag_dict, saved_counts)
        count_in_bag = saved_counts[bag_spec.name]
        total += bag_spec.count * (count_in_bag + 1)
    saved_counts[bag_name] = total


def solve_part2(file_obj: io.TextIOBase) -> int:
    saved_counts: Dict[str, int] = {}
    bag_dict = construct_bag_dict(file_obj)
    count_bags_in_name("shiny gold", bag_dict, saved_counts)
    return saved_counts["shiny gold"]


def main():
    print("---Sample Part 1---")
    print(f"{len(solve_part1(get_sample_inputs()))} bag types contain shiny gold")
    print("---Actual Part 1---")
    with open("./input.txt") as f:
        print(f"{len(solve_part1(f))} bag types contain shiny gold")
    print("---Sample Part 2---")
    print(f"{solve_part2(get_sample_inputs())} bag types contain shiny gold")
    print("---Sample 2 Part 2---")
    print(f"{solve_part2(get_sample_2_inputs())} bag types contain shiny gold")
    print("---Actual Part 2---")
    with open("./input.txt") as f:
        print(f"{solve_part2(f)} bag types contain shiny gold")


if __name__ == "__main__":
    main()
