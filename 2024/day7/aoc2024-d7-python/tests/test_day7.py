import operator

from aoc2024_d7_python.day7 import (
    calculate,
    check_can_calibrate,
    int_concat,
    parse,
    part1,
    part2,
)

input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

funcs = (int_concat, operator.mul, operator.add)


def test_calculate() -> None:
    input = ((operator.mul,), (10, 19))
    expected = 190

    assert calculate(*input) == expected

    input = ((operator.mul, operator.add), (81, 40, 27))
    expected = 3267

    assert calculate(*input) == expected  # type: ignore


def test_can_calibrate() -> None:
    input = (190, (10, 19))
    expected = True

    assert check_can_calibrate(*input, funcs) == expected

    input = (3267, (81, 40, 27))
    expected = True

    assert check_can_calibrate(*input, funcs) == expected

    input = (292, (11, 6, 16, 20))
    expected = True

    assert check_can_calibrate(*input, funcs) == expected

    input = (83, (17, 5))
    expected = False

    assert check_can_calibrate(*input, funcs) == expected

    # part 2
    input = (156, (15, 6))
    expected = True

    assert check_can_calibrate(*input, funcs) == expected

    input = (7290, (6, 8, 6, 15))
    expected = True

    assert check_can_calibrate(*input, funcs) == expected

    input = (192, (17, 8, 14))
    input = (7290, (6, 8, 6, 15))
    expected = True

    assert check_can_calibrate(*input, funcs) == expected


def test_parse() -> None:
    expected = (
        (190, (10, 19)),
        (3267, (81, 40, 27)),
        (83, (17, 5)),
        (156, (15, 6)),
        (7290, (6, 8, 6, 15)),
        (161011, (16, 10, 13)),
        (192, (17, 8, 14)),
        (21037, (9, 7, 18, 13)),
        (292, (11, 6, 16, 20)),
    )

    assert parse(input) == expected


def test_part1() -> None:
    expected = 3749

    assert part1(input) == expected


def test_part2() -> None:
    expected = 11387

    assert part2(input) == expected
