from funcparserlib.lexer import Token

from aoc2019_d2_python.day2 import (
    Add,
    IntSpec,
    Mul,
    evaluate,
    parse_memory,
    parser_generate,
    tokenize,
)


def test_tokenize() -> None:
    input = "1,0,0,3,99"
    expected = (
        Token(IntSpec.INT.name, "1"),
        Token(IntSpec.INT.name, "0"),
        Token(IntSpec.INT.name, "0"),
        Token(IntSpec.INT.name, "3"),
        Token(IntSpec.INT.name, "99"),
    )

    assert tokenize(input) == expected


def test_parse() -> None:
    parser = parser_generate()

    input = (
        Token(IntSpec.INT.name, "1"),
        Token(IntSpec.INT.name, "10"),
        Token(IntSpec.INT.name, "20"),
        Token(IntSpec.INT.name, "30"),
    )
    expected = Add(1, 10, 20, 30, 4)

    assert parser.parse(input) == expected

    input = (
        Token(IntSpec.INT.name, "2"),
        Token(IntSpec.INT.name, "10"),
        Token(IntSpec.INT.name, "20"),
        Token(IntSpec.INT.name, "30"),
    )
    expected = Mul(2, 10, 20, 30, 4)

    assert parser.parse(input) == expected


def test_evaluate() -> None:
    input = "1,0,0,0,99"
    expected = "2,0,0,0,99"

    assert evaluate(parser_generate(), tokenize(input)) == parse_memory(
        tokenize(expected)
    )

    input = "2,3,0,3,99"
    expected = "2,3,0,6,99"

    assert evaluate(parser_generate(), tokenize(input)) == parse_memory(
        tokenize(expected)
    )

    input = "2,4,4,5,99,0"
    expected = "2,4,4,5,99,9801"

    assert evaluate(parser_generate(), tokenize(input)) == parse_memory(
        tokenize(expected)
    )

    input = "1,1,1,4,99,5,6,0,99"
    expected = "30,1,1,4,2,5,6,0,99"

    assert evaluate(parser_generate(), tokenize(input)) == parse_memory(
        tokenize(expected)
    )
