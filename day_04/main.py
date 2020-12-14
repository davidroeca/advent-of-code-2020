import io
import re
from typing import NamedTuple, Iterable, Optional, Dict

_SAMPLE_INPUT_STR = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

SAMPLE_INPUTS = io.StringIO(_SAMPLE_INPUT_STR)


def convert_line_to_kvs_dict(line: str) -> Dict[str, str]:
    output: Dict[str, str] = {}
    for kv_raw in line.strip().split(" "):
        kv = kv_raw.strip()
        if kv:
            kv_split = kv.split(":")
            assert len(kv_split) == 2, f"{kv} must be a colon-separated pair"
            key = kv_split[0].strip()
            value = kv_split[1].strip()
            output[key] = value
    return output


def iter_passports(file_obj: io.TextIOBase) -> Iterable[Dict[str, str]]:
    """Note that in this implementation, the file should not start with any blank lines"""
    current_kvs: Dict[str, str] = {}
    for raw_line in file_obj:
        line = raw_line.strip()
        if line:
            current_kvs = {
                **current_kvs,
                **convert_line_to_kvs_dict(line),
            }
        elif current_kvs:
            yield current_kvs
            current_kvs = {}
    if current_kvs:
        yield current_kvs


def validate_passport_part_1(passport: Dict[str, str]) -> bool:
    return (
        "byr" in passport
        and "iyr" in passport
        and "eyr" in passport
        and "hgt" in passport
        and "hcl" in passport
        and "ecl" in passport
        and "pid" in passport
    )

def validate_passport_part_2(passport: Dict[str, str]) -> bool:
    if not validate_passport_part_1(passport):
        return False
    byr = passport["byr"]
    iyr = passport["iyr"]
    eyr = passport["eyr"]
    year_regex = re.compile(r"^[1-2][0-9]{3}$")
    if (
        not year_regex.match(byr)
        or not year_regex.match(iyr)
        or not year_regex.match(eyr)
    ):
        return False
    byr_int = int(byr)
    iyr_int = int(iyr)
    eyr_int = int(eyr)
    if byr_int < 1920 or byr_int > 2002:
        return False
    if iyr_int < 2010 or iyr_int > 2020:
        return False
    if eyr_int < 2020 or eyr_int > 2030:
        return False
    hgt = passport["hgt"]
    hgt_regex_cm = re.compile(r"^[1-9][0-9]*cm$")
    hgt_regex_in = re.compile(r"^[1-9][0-9]*in$")
    if hgt_regex_cm.match(hgt):
        hgt_int = int(hgt.rstrip("cm"))
        if hgt_int < 150 or hgt_int > 193:
            return False
    elif hgt_regex_in.match(hgt):
        hgt_int = int(hgt.rstrip("in"))
        if hgt_int < 59 or hgt_int > 76:
            return False
    else:
        return False
    hcl = passport["hcl"]
    hcl_regex = re.compile(r"^#[0-9a-zA-Z]{6}$")
    if not hcl_regex.match(hcl):
        return False
    ecl = passport["ecl"]
    valid_ecls = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    if ecl not in valid_ecls:
        return False
    pid = passport["pid"]
    pid_regex = re.compile(r"^[0-9]{9}$")
    return pid_regex.match(pid)


def solution_part1(file_obj: io.TextIOBase) -> int:
    return sum(
        1 for passport in iter_passports(file_obj) if validate_passport_part_1(passport)
    )

def solution_part2(file_obj: io.TextIOBase) -> int:
    return sum(
        1 for passport in iter_passports(file_obj) if validate_passport_part_2(passport)
    )


def main():
    print("---Sample Part 1---")
    print(f"{solution_part1(SAMPLE_INPUTS)} valid passports")
    print("---Actual Part 1---")
    with open("./input.txt") as input_file:
        print(f"{solution_part1(input_file)} valid passports")
    print("---Sample Part 2---")
    print(f"{solution_part2(SAMPLE_INPUTS)} valid passports")
    print("---Actual Part 2---")
    with open("./input.txt") as input_file:
        print(f"{solution_part2(input_file)} valid passports")


if __name__ == "__main__":
    main()
