from aoc2024_d3_python.day3b import (
    Condition,
    Mul,
    Spec,
    Token_,
    evaluate_skip_condition,
    evaluate_with_condition,
    parse,
    parser_generate,
    part1,
    part2,
    tokenize,
)


def test_tokenizer() -> None:
    input = "mul(44,46)"
    expected = (
        Token_(Spec.OP, "mul"),
        Token_(Spec.LPAREN, "("),
        Token_(Spec.NUMBER, "44"),
        Token_(Spec.COMMA, ","),
        Token_(Spec.NUMBER, "46"),
        Token_(Spec.RPAREN, ")"),
    )

    assert tokenize(input) == expected

    input = "do()"
    expected = (
        Token_(Spec.OP, "do"),
        Token_(Spec.LPAREN, "("),
        Token_(Spec.RPAREN, ")"),
    )

    assert tokenize(input) == expected

    input = "don't()"
    expected = (
        Token_(Spec.OP, "don't"),
        Token_(Spec.LPAREN, "("),
        Token_(Spec.RPAREN, ")"),
    )

    assert tokenize(input) == expected

    input = "mul(4*"
    expected = (
        Token_(Spec.OP, "mul"),
        Token_(Spec.LPAREN, "("),
        Token_(Spec.NUMBER, "4"),
        Token_(Spec.GIBBERISH, "*"),
    )

    assert tokenize(input) == expected

    input = "mul(6,9!"
    expected = (
        Token_(Spec.OP, "mul"),
        Token_(Spec.LPAREN, "("),
        Token_(Spec.NUMBER, "6"),
        Token_(Spec.COMMA, ","),
        Token_(Spec.NUMBER, "9"),
        Token_(Spec.GIBBERISH, "!"),
    )

    assert tokenize(input) == expected

    input = "?(12,34)"
    expected = (
        Token_(Spec.GIBBERISH, "?"),
        Token_(Spec.LPAREN, "("),
        Token_(Spec.NUMBER, "12"),
        Token_(Spec.COMMA, ","),
        Token_(Spec.NUMBER, "34"),
        Token_(Spec.RPAREN, ")"),
    )

    assert tokenize(input) == expected

    input = "mul ( 2 , 4 )"
    expected = (
        Token_(Spec.OP, "mul"),
        Token_(Spec.GIBBERISH, " "),
        Token_(Spec.LPAREN, "("),
        Token_(Spec.GIBBERISH, " "),
        Token_(Spec.NUMBER, "2"),
        Token_(Spec.GIBBERISH, " "),
        Token_(Spec.COMMA, ","),
        Token_(Spec.GIBBERISH, " "),
        Token_(Spec.NUMBER, "4"),
        Token_(Spec.GIBBERISH, " "),
        Token_(Spec.RPAREN, ")"),
    )

    assert tokenize(input) == expected


def test_parse_mul() -> None:
    parser = parser_generate()
    input = (
        Token_(Spec.OP, "mul"),
        Token_(Spec.LPAREN, "("),
        Token_(Spec.NUMBER, "44"),
        Token_(Spec.COMMA, ","),
        Token_(Spec.NUMBER, "46"),
        Token_(Spec.RPAREN, ")"),
    )
    expected = (Mul(44, 46), ())

    assert parser.parse(input) == expected


def test_parse() -> None:
    parser = parser_generate()

    input = "mul(44,46)"
    expected = (Mul(44, 46),)

    assert parse(parser, tokenize(input)) == expected

    input = ("mul(4*", "mul(4*", "mul(4*", "mul ( 2 , 4 )")
    expected = ()

    for case in input:
        assert parse(parser, tokenize(case)) == expected

    input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    expected = (
        Mul(2, 4),
        Mul(5, 5),
        Mul(11, 8),
        Mul(8, 5),
    )

    assert parse(parser, tokenize(input)) == expected

    input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    expected = (
        Mul(2, 4),
        Condition(False),
        Mul(5, 5),
        Mul(11, 8),
        Condition(True),
        Mul(8, 5),
    )

    assert parse(parser, tokenize(input)) == expected


def test_evaluate_skip_condition() -> None:
    input = (Mul(44, 46),)
    expected = 2024

    assert evaluate_skip_condition(input) == expected

    input = (
        Mul(2, 4),
        Mul(5, 5),
        Mul(11, 8),
        Mul(8, 5),
    )
    expected = 161

    assert evaluate_skip_condition(input) == expected


def test_part1() -> None:
    input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    expected = 161

    assert part1(input) == expected


def test_evaluate_with_condition():
    input = (
        Mul(2, 4),
        Condition(False),
        Mul(5, 5),
        Mul(11, 8),
        Condition(True),
        Mul(8, 5),
    )
    expected = 48

    assert evaluate_with_condition(input) == expected


def test_part2() -> None:
    input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    expected = 48

    assert part2(input) == expected
