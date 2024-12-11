import pytest

from aoc2024_d11_python.day11 import (
    blink,
    blink_to_count,
    part1,
    stone_increment,
    stone_multiply,
    stone_split,
)


def test_stone_increment() -> None:
    input = 0
    expected = (1,)

    assert stone_increment(input) == expected

    with pytest.raises(AssertionError):
        stone_increment(1)


def test_stone_split() -> None:
    input = 1000
    expected = (10, 0)

    assert stone_split(input) == expected

    with pytest.raises(AssertionError):
        stone_split(101)


def test_stone_multiply() -> None:
    input = 1
    expected = (2024,)

    assert stone_multiply(input) == expected


def test_blink() -> None:
    input = (0, 1, 10, 99, 999)
    expected = (1, 2024, 1, 0, 9, 9, 2021976)

    assert tuple(blink(input)) == expected

    input = (125, 17)

    expected = (253000, 1, 7)
    assert (input := tuple(blink(input))) == expected

    expected = (253, 0, 2024, 14168)
    assert (input := tuple(blink(input))) == expected

    expected = (512072, 1, 20, 24, 28676032)
    assert (input := tuple(blink(input))) == expected

    expected = (512, 72, 2024, 2, 0, 2, 4, 2867, 6032)
    assert (input := tuple(blink(input))) == expected

    expected = (1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32)
    assert (input := tuple(blink(input))) == expected

    expected = (
        2097446912,
        14168,
        4048,
        2,
        0,
        2,
        4,
        40,
        48,
        2024,
        40,
        48,
        80,
        96,
        2,
        8,
        6,
        7,
        6,
        0,
        3,
        2,
    )
    assert (input := tuple(blink(input))) == expected

    input2 = (125, 17)
    expected = 55312

    assert len(tuple(blink(input2, 25))) == expected

def test_blink_for_count():
    input = (125, 17)
    expected = 55312

    assert blink_to_count(input, 25) == expected


def test_part1() -> None:
    input = "125 17"
    expected = 55312

    assert part1(input) == expected