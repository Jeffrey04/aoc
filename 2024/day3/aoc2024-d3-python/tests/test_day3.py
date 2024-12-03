import operator

from funcparserlib.lexer import Token

from aoc2024_d3_python.day3 import (
    BinaryExpression,
    Condition,
    SpecName,
    evaluate_skip_condition,
    evaluate_with_condition,
    parse,
    tokenize,
)


def test_tokenizer() -> None:
    input = "mul(44,46)"
    expected = (
        Token(SpecName.INS_MUL.name, "mul"),
        Token(SpecName.LPAREN.name, "("),
        Token(SpecName.INT.name, "44"),
        Token(SpecName.COMMA.name, ","),
        Token(SpecName.INT.name, "46"),
        Token(SpecName.RPAREN.name, ")"),
    )

    assert tokenize(input) == expected

    input = "mul ( 2 , 4 )"
    expected = (
        Token(SpecName.INS_MUL.name, "mul"),
        Token(SpecName.GIBBERISH.name, " "),
        Token(SpecName.LPAREN.name, "("),
        Token(SpecName.GIBBERISH.name, " "),
        Token(SpecName.INT.name, "2"),
        Token(SpecName.GIBBERISH.name, " "),
        Token(SpecName.COMMA.name, ","),
        Token(SpecName.GIBBERISH.name, " "),
        Token(SpecName.INT.name, "4"),
        Token(SpecName.GIBBERISH.name, " "),
        Token(SpecName.RPAREN.name, ")"),
    )

    assert tokenize(input) == expected


def test_parser() -> None:
    input = "mul(44,46)"
    expected = [BinaryExpression(operator.mul, 44, 46)]

    assert parse(tokenize(input)) == expected

    input = ("mul(4*", "mul(4*", "mul(4*", "mul ( 2 , 4 )")
    expected = []

    for case in input:
        assert parse(tokenize(case)) == expected

    input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    expected = [
        BinaryExpression(operator.mul, 2, 4),
        BinaryExpression(operator.mul, 5, 5),
        BinaryExpression(operator.mul, 11, 8),
        BinaryExpression(operator.mul, 8, 5),
    ]

    assert parse(tokenize(input)) == expected


def test_evaluate_skip_condition():
    input = [BinaryExpression(operator.mul, 44, 46)]
    expected = 2024

    assert evaluate_skip_condition(input) == expected

    input = [
        BinaryExpression(operator.mul, 2, 4),
        BinaryExpression(operator.mul, 5, 5),
        BinaryExpression(operator.mul, 11, 8),
        BinaryExpression(operator.mul, 8, 5),
    ]
    expected = 161

    assert evaluate_skip_condition(input) == expected


def test_parser_part2():
    input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    expected = [
        BinaryExpression(operator.mul, 2, 4),
        Condition(False),
        BinaryExpression(operator.mul, 5, 5),
        BinaryExpression(operator.mul, 11, 8),
        Condition(True),
        BinaryExpression(operator.mul, 8, 5),
    ]

    assert parse(tokenize(input)) == expected


def test_evaluate_with_condition():
    input = [
        BinaryExpression(operator.mul, 2, 4),
        Condition(False),
        BinaryExpression(operator.mul, 5, 5),
        BinaryExpression(operator.mul, 11, 8),
        Condition(True),
        BinaryExpression(operator.mul, 8, 5),
    ]
    expected = 48

    assert evaluate_with_condition(input) == expected
