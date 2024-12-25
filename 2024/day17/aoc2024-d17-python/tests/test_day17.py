from aoc2024_d17_python.day17 import (
    Computer,
    Program,
    evaluate,
    evaluate_loop,
    parse,
    parse_program,
    part1,
    part2,
)

input = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""


def test_parse() -> None:
    expected = Computer(729, 0, 0, Program((0, 1, 5, 4, 3, 0)))

    assert parse(input) == expected


def test_parse_program() -> None:
    input = "0,1,2,3"
    expected = Program((0, 1, 2, 3))

    assert parse_program(input) == expected


def test_evaluate() -> None:
    input = Computer(0, 0, 9, parse_program("2,6"))
    expected = 1

    assert evaluate(input).B == expected


def test_evaluate_loop() -> None:
    input = Computer(0, 0, 9, parse_program("2,6"))
    expected = 1

    assert evaluate_loop(input).B == expected

    input = Computer(10, 0, 0, parse_program("5,0,5,1,5,4"))
    expected = (0, 1, 2)

    assert evaluate_loop(input).OUTPUT == expected

    input = Computer(2024, 0, 0, parse_program("0,1,5,4,3,0"))
    expected_OUTPUT = (4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0)
    expected_A = 0
    result = evaluate_loop(input)

    assert result.OUTPUT == expected_OUTPUT
    assert result.A == expected_A

    input = Computer(0, 29, 0, parse_program("1,7"))
    expected = 26

    assert evaluate_loop(input).B == expected

    input = Computer(0, 2024, 43690, parse_program("4,0"))
    expected = 44354

    assert evaluate_loop(input).B == expected


def test_part1() -> None:
    expected = "4,6,3,5,6,3,5,2,1,0"

    assert part1(input) == expected

    input2 = """
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
    expected = "0,3,5,4,3,0"

    assert part1(input2) == expected


def test_part2() -> None:
    input = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
    expected = 117440

    assert part2(input) == expected
