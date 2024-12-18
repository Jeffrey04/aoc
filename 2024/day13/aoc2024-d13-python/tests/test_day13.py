from aoc2024_d13_python.day13 import find, parse, part1

input = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def test_parse() -> None:
    expected = (
        ({(94, 34): 3, (22, 67): 1}, (8400, 5400)),
        ({(26, 66): 3, (67, 21): 1}, (12748, 12176)),
        ({(17, 86): 3, (84, 37): 1}, (7870, 6450)),
        ({(69, 23): 3, (27, 71): 1}, (18641, 10279)),
    )

    assert parse(input) == expected


def test_find() -> None:
    input = ({(94, 34): 3, (22, 67): 1}, (8400, 5400))
    result = {(94, 34): 80, (22, 67): 40}

    assert find(*input) == result


def test_part1() -> None:
    expected = 480

    assert part1(input) == expected
