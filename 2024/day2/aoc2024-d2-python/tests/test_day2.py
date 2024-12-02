from aoc2024_d2_python.day2 import (
    check_diff,
    check_is_decreasing,
    check_is_increasing,
    check_safety,
    parse_line,
    safe_count,
    safe_count_with_dampener,
    sliding_window,
)

input = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def test_parse_line() -> None:
    expected = (
        (7, 6, 4, 2, 1),
        (1, 2, 7, 8, 9),
        (9, 7, 6, 2, 1),
        (1, 3, 2, 4, 5),
        (8, 6, 4, 4, 1),
        (1, 3, 6, 7, 9),
    )

    for idx, line in enumerate(input.strip().splitlines()):
        assert parse_line(line) == expected[idx]


def test_sliding_window() -> None:
    input = (7, 6, 4, 2, 1)
    expected = ((7, 6), (6, 4), (4, 2), (2, 1))

    assert sliding_window(input) == expected


def test_is_increasing() -> None:
    input_increasing = (1, 3, 6, 7, 9)
    input_decreasing = (7, 6, 4, 2, 1)

    assert check_is_increasing(sliding_window(input_increasing))
    assert check_is_increasing(sliding_window(input_decreasing)) is False


def test_is_decreasing() -> None:
    input_increasing = (1, 3, 6, 7, 9)
    input_decreasing = (7, 6, 4, 2, 1)

    assert check_is_decreasing(sliding_window(input_increasing)) is False
    assert check_is_decreasing(sliding_window(input_decreasing))


def test_check_diff() -> None:
    assert check_diff(7, 6)
    assert check_diff(2, 7) is False


def test_check_safety() -> None:
    expected = (True, False, False, False, False, True)

    for idx, line in enumerate(input.strip().splitlines()):
        pairs = sliding_window(parse_line(line))

        assert check_safety(pairs) == expected[idx]


def test_safe_count() -> None:
    assert safe_count(input) == 2


def test_safe_count_with_dampener() -> None:
    assert safe_count_with_dampener(input) == 4
