from aoc2015_d1_python.day1 import part1, part2, step


def test_step() -> None:
    input = (0, "(")
    expected = 1

    assert step(*input) == expected


def test_part1() -> None:
    input = ("(())", "(())")
    expected = 0

    for case in input:
        assert part1(case) == expected

    input = ("(((", "(((", "))(((((")
    expected = 3

    for case in input:
        assert part1(case) == expected

    input = ("())", "))(")
    expected = -1

    for case in input:
        assert part1(case) == expected

    input = (")))", ")())())")
    expected = -3

    for case in input:
        assert part1(case) == expected


def test_part2() -> None:
    input = ")"
    expected = 1

    for case in input:
        assert part2(input) == expected

    input = "()())"
    expected = 5

    for case in input:
        assert part2(input) == expected
