import math
from itertools import count
from typing import List, Optional, Tuple, Dict, Set, Iterable

# INPUT_SAMPLE = """
# 939
# 7,13,x,x,59,x,31,19
# """
INPUT_SAMPLE = """
939
1789,37,47,1889
"""

INPUT_ACTUAL = """
1000507
29,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,631,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,13,19,x,x,x,23,x,x,x,x,x,x,x,383,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,17
"""


def solve_part1(input_str: str):
    [earliest_time_str, buses_str] = input_str.strip().split("\n")
    earliest_time = int(earliest_time_str)
    iter_clean_bus = (bus.strip() for bus in buses_str.split(","))
    bus_ids = [int(bus) for bus in iter_clean_bus if bus != "x"]
    assert bus_ids, "There must be at least one bus id"
    min_bus_id = bus_ids[0]
    min_time = min_bus_id - earliest_time % min_bus_id
    for bus_id in bus_ids[1:]:
        time_to_wait = bus_id - earliest_time % bus_id
        if time_to_wait < min_time:
            min_time = time_to_wait
            min_bus_id = bus_id
    return min_time * min_bus_id


def iter_primes_until(num: int) -> Iterable[int]:
    primes = [True for true in range(num)]
    for i in range(2, math.ceil(math.sqrt(num)) + 1):
        if primes[i]:
            yield i
            j = i * i
            while j < num:
                if primes[j]:
                    primes[j] = False
                j += i


def iter_prime_factors(num: int) -> Iterable[int]:
    if num < 2:
        yield num
        return
    primes = [i for i in iter_primes_until(num)]
    remaining = num
    for prime in primes:
        while remaining % prime == 0:
            yield prime
            remaining = remaining // prime
        if remaining < 2:
            break
    if remaining >= 2:
        # It's actually a prime
        yield remaining



def solve_part2(input_str: str) -> int:
    [_, buses_str] = input_str.strip().split("\n")
    iter_clean_bus = (bus.strip() for bus in buses_str.split(","))
    bus_ids = [int(bus) if bus != "x" else 1 for bus in iter_clean_bus]
    assert bus_ids, "There must be at least one bus id"
    current_start_time = 0
    increment = 1
    while True:
        first_offset_index = -1
        for index, bus_id in enumerate(bus_ids):
            offset = (current_start_time + index) % bus_id
            if offset != 0:
                first_offset_index = index
                break
        if first_offset_index == -1:
            return current_start_time
        for i in range(first_offset_index):
            for prime_factor in iter_prime_factors(bus_ids[i]):
                if increment % prime_factor != 0:
                    increment *= prime_factor
        current_start_time += increment


def main():
    print("---Sample Part 1---")
    print(solve_part1(INPUT_SAMPLE))
    print("---Actual Part 1---")
    print(solve_part1(INPUT_ACTUAL))
    print("---Sample Part 2---")
    print(solve_part2(INPUT_SAMPLE))
    print("---Actual Part 2---")
    print(solve_part2(INPUT_ACTUAL))


if __name__ == "__main__":
    main()
