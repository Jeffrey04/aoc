from funcparserlib.lexer import Token

from aoc2024_d3_python.day3 import (
    ExprCondition,
    ExprMul,
    SpecGen,
    SpecMul,
    evaluate_skip_condition,
    evaluate_with_condition,
    parse,
    parser_mul,
    tokenize,
    tokenize_mul,
)


def test_tokenizer() -> None:
    input = "mul(44,46)"
    expected = (Token(SpecGen.INS_MUL.name, "mul(44,46)"),)

    assert tokenize(input) == expected

    input = "do()"
    expected = (Token(SpecGen.INS_DO.name, "do()"),)

    assert tokenize(input) == expected

    input = "don't()"
    expected = (Token(SpecGen.INS_DONT.name, "don't()"),)

    assert tokenize(input) == expected

    input = "mul ( 2 , 4 )"
    expected = ()

    assert tokenize(input) == expected


def test_tokenizer_binary() -> None:
    input = "mul(44,46)"
    expected = (
        Token(SpecMul.OP.name, "mul"),
        Token(SpecMul.LPAREN.name, "("),
        Token(SpecMul.NUMBER.name, "44"),
        Token(SpecMul.COMMA.name, ","),
        Token(SpecMul.NUMBER.name, "46"),
        Token(SpecMul.RPAREN.name, ")"),
    )

    assert tokenize_mul(input) == expected


def test_parser_mul() -> None:
    input = (
        Token(SpecMul.OP.name, "mul"),
        Token(SpecMul.LPAREN.name, "("),
        Token(SpecMul.NUMBER.name, "44"),
        Token(SpecMul.COMMA.name, ","),
        Token(SpecMul.NUMBER.name, "46"),
        Token(SpecMul.RPAREN.name, ")"),
    )
    expected = ExprMul(44, 46)

    assert parser_mul(input) == expected


def test_parse() -> None:
    input = "mul(44,46)"
    expected = (ExprMul(44, 46),)

    assert parse(tokenize(input)) == expected

    input = ("mul(4*", "mul(4*", "mul(4*", "mul ( 2 , 4 )")
    expected = ()

    for case in input:
        assert parse(tokenize(case)) == expected

    input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    expected = (
        ExprMul(2, 4),
        ExprMul(5, 5),
        ExprMul(11, 8),
        ExprMul(8, 5),
    )

    assert parse(tokenize(input)) == expected

    input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    expected = (
        ExprMul(2, 4),
        ExprCondition(False),
        ExprMul(5, 5),
        ExprMul(11, 8),
        ExprCondition(True),
        ExprMul(8, 5),
    )

    assert parse(tokenize(input)) == expected


def test_evaluate_skip_condition():
    input = (ExprMul(44, 46),)
    expected = 2024

    assert evaluate_skip_condition(input) == expected

    input = (
        ExprMul(2, 4),
        ExprMul(5, 5),
        ExprMul(11, 8),
        ExprMul(8, 5),
    )
    expected = 161

    assert evaluate_skip_condition(input) == expected


def test_evaluate_with_condition():
    input = (
        ExprMul(2, 4),
        ExprCondition(False),
        ExprMul(5, 5),
        ExprMul(11, 8),
        ExprCondition(True),
        ExprMul(8, 5),
    )
    expected = 48

    assert evaluate_with_condition(input) == expected
