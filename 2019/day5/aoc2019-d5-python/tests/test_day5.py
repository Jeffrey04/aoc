from aoc2019_d5_python.day5 import (
    Immediate,
    Mul5,
    OpType,
    Position,
    evaluate,
    memory_create,
    opcode_get_type,
    parameter_get_mode,
    parse,
    tokenize,
)


def test_opcode_get_type() -> None:
    input = 1002

    assert opcode_get_type(input) == OpType.MUL


def test_parameter_get_mode() -> None:
    input = ("01002", 4, 0)
    expected = Position(0, 4)

    assert parameter_get_mode(*input) == expected

    input = ("01002", 3, 1)
    expected = Immediate(1, 3)

    assert parameter_get_mode(*input) == expected

    input = ("01002", 4, 2)
    expected = Position(0, 4)

    assert parameter_get_mode(*input) == expected


def test_parse() -> None:
    input = "1002,4,3,4,33"
    expected = Mul5(
        1002,
        Position(0, 4),
        Immediate(1, 3),
        4,
        4,
    )
    assert parse(memory_create(tokenize(input))) == expected


def test_evaluate() -> None:
    input = "3,9,8,9,10,9,4,9,99,-1,8"

    assert evaluate(tokenize(input), 7) == 0
    assert evaluate(tokenize(input), 8) == 1
    assert evaluate(tokenize(input), 9) == 0

    input = "3,9,7,9,10,9,4,9,99,-1,8"

    assert evaluate(tokenize(input), 7) == 1
    assert evaluate(tokenize(input), 8) == 0
    assert evaluate(tokenize(input), 9) == 0

    input = "3,3,1108,-1,8,3,4,3,99"

    assert evaluate(tokenize(input), 7) == 0
    assert evaluate(tokenize(input), 8) == 1
    assert evaluate(tokenize(input), 9) == 0

    input = "3,3,1107,-1,8,3,4,3,99"

    assert evaluate(tokenize(input), 7) == 1
    assert evaluate(tokenize(input), 8) == 0
    assert evaluate(tokenize(input), 9) == 0

    input = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"

    assert evaluate(tokenize(input), -1) == 1
    assert evaluate(tokenize(input), 0) == 0
    assert evaluate(tokenize(input), 1) == 1

    input = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"

    assert evaluate(tokenize(input), -1) == 1
    assert evaluate(tokenize(input), 0) == 0
    assert evaluate(tokenize(input), 1) == 1

    input = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"

    assert evaluate(tokenize(input), 7) == 999
    assert evaluate(tokenize(input), 8) == 1000
    assert evaluate(tokenize(input), 9) == 1001
