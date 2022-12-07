from aoc2022_d3_python.day3 import (
    find_common,
    find_priority,
    find_sum_badge,
    find_sum_common,
    split_groups,
    split_rucksack,
)

test_input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()


def test_split_rucksack() -> None:
    items = test_input.split("\n")

    assert ("vJrwpWtwJgWr", "hcsFMMfFFhFp") == split_rucksack(items[0])
    assert ("jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL") == split_rucksack(items[1])
    assert ("PmmdzqPrV", "vPwwTWBwg") == split_rucksack(items[2])
    assert ("wMqvLMZHhHMvwLH", "jbvcjnnSBnvTQFn") == split_rucksack(items[3])
    assert ("ttgJtRGJ", "QctTZtZT") == split_rucksack(items[4])
    assert ("CrZsJsPPZsGz", "wwsLwLmpwMDw") == split_rucksack(items[5])


def test_find_common() -> None:
    rucksacks = [split_rucksack(rucksack) for rucksack in test_input.split("\n")]

    assert "p" == find_common(rucksacks[0])
    assert "L" == find_common(rucksacks[1])
    assert "P" == find_common(rucksacks[2])
    assert "v" == find_common(rucksacks[3])
    assert "t" == find_common(rucksacks[4])
    assert "s" == find_common(rucksacks[5])


def test_find_priority() -> None:
    assert 16 == find_priority("p")
    assert 38 == find_priority("L")
    assert 42 == find_priority("P")
    assert 22 == find_priority("v")
    assert 20 == find_priority("t")
    assert 19 == find_priority("s")

    assert 18 == find_priority("r")
    assert 52 == find_priority("Z")


def test_find_sum_common() -> None:
    assert 157 == find_sum_common(test_input)


def test_find_group() -> None:
    rucksacks_raw = tuple(test_input.split("\n"))

    groups = rucksacks_raw[:3], rucksacks_raw[3:]

    assert groups == split_groups(test_input)


def test_find_common_badge() -> None:
    rucksack_raw_groups = split_groups(test_input)

    assert "r" == find_common(rucksack_raw_groups[0])
    assert "Z" == find_common(rucksack_raw_groups[1])


def test_find_common_badge_sum() -> None:
    assert 70 == find_sum_badge(test_input)
