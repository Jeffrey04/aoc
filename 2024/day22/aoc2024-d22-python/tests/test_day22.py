from aoc2024_d22_python.day22 import input_mix, input_prune, part2, random_next, repeat


def test_random_next() -> None:
    input = 123
    expected = 15887950

    assert random_next(input) == expected


def test_input_mix() -> None:
    input = (42, lambda _: 15)
    expected = 37

    assert input_mix(*input) == expected


def test_input_prune() -> None:
    input = 100000000
    expected = 16113920

    assert input_prune(input) == expected


def test_repeat() -> None:
    next_repeated = repeat(random_next, 2000)

    input = 1
    expected = 8685429

    assert next_repeated(input) == expected


def test_part2() -> None:
    input = """
1
2
3
2024
"""
    expected = 23

    assert part2(input) == expected
