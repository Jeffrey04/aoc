import pytest

from aoc2024_d5_python.day5 import (
    check_pages,
    check_pair,
    get_middle,
    move,
    parse,
    part1,
    part2,
    sort_pages,
)

input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def test_parse():
    input = """
47|53
97|13

75,29,13
61,13,29
"""
    expected = ((47, 53), (97, 13)), ((75, 29, 13), (61, 13, 29))

    assert parse(input) == expected


def test_check_pair() -> None:
    rules = ((75, 47), (75, 61), (75, 53), (75, 29))
    input = (75, 47)
    expected = True

    assert check_pair(rules, *input) == expected

    rules = ((97, 75),)
    input = (75, 97)
    expected = False

    assert check_pair(rules, *input) == expected


def test_check_pages() -> None:
    rules = (
        (75, 47),
        (75, 61),
        (75, 53),
        (75, 29),
        (47, 61),
        (47, 53),
        (47, 29),
        (61, 53),
        (61, 29),
        (97, 75),
    )

    input = (75, 47, 61, 53, 29)
    expected = True

    assert check_pages(rules, input) == expected

    input = (75, 97, 47, 61, 53)
    expected = False
    assert check_pages(rules, input) == expected


def test_get_middle() -> None:
    input = (75, 47, 61, 53, 29)
    expected = 61

    assert get_middle(input) == expected


def test_part1() -> None:
    expected = 143

    assert part1(input) == expected


def test_move() -> None:
    items = (75, 97, 47, 61, 53)
    input = (0, 1)
    expected = (97, 75, 47, 61, 53)

    assert move(items, *input) == expected

    input = (0, 2)
    expected = (47, 75, 97, 61, 53)

    assert move(items, *input) == expected

    with pytest.raises(AssertionError):
        input = (2, 0)

        assert move(items, *input)


def test_sort_pages() -> None:
    input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

1, 2
"""
    rules, _ = parse(input)

    input = (75, 97, 47, 61, 53)
    expected = (97, 75, 47, 61, 53)

    assert sort_pages(rules, input) == expected

    input = (61, 13, 29)
    expected = (61, 29, 13)

    assert sort_pages(rules, input) == expected

    input = (97, 13, 75, 29, 47)
    expected = (97, 75, 47, 29, 13)

    assert sort_pages(rules, input) == expected


def test_part2() -> None:
    expected = 123

    assert part2(input) == expected
