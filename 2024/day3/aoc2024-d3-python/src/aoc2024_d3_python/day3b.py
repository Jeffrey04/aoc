import operator
from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from sys import stdin
from typing import Any

from funcparserlib.lexer import Token, TokenSpec, make_tokenizer
from funcparserlib.parser import NoParseError, Parser, finished, many, tok


class Spec(Enum):
    OP = auto()
    NUMBER = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    GIBBERISH = auto()


class Expr(ABC):
    pass


@dataclass
class Mul(Expr):
    alpha: int
    beta: int

    def evaluate(self) -> int:
        return self.alpha * self.beta

    def __str__(self) -> str:
        return f"mul({self.alpha},{self.beta})"


@dataclass
class Condition(Expr):
    can_proceed: bool


#
# Proxies
#
def Token_(name: Spec, *args: Any, **kwargs: Any) -> Token:
    return Token(name.name, *args, **kwargs)


def TokenSpec_(name: Spec, *args: Any, **kwargs: Any) -> TokenSpec:
    return TokenSpec(name.name, *args, **kwargs)


def tok_(name: Spec, *args: Any, **kwargs: Any) -> Parser[Token, str]:
    return tok(name.name, *args, **kwargs)


def tokenize(input: str) -> tuple[Token, ...]:
    def inner(current: list[Token], incoming: Token) -> list[Token]:
        if not current:
            current.append(incoming)
            return current

        match incoming.type:
            case Spec.GIBBERISH.name:
                if current[-1].type != incoming.type:
                    current.append(incoming)
                return current

            case _:
                current.append(incoming)
                return current

    tokenizer = make_tokenizer(
        [
            TokenSpec_(Spec.OP, r"mul|don\'t|do"),
            TokenSpec_(Spec.NUMBER, r"\d{1,3}"),
            TokenSpec_(Spec.LPAREN, r"\("),
            TokenSpec_(Spec.RPAREN, r"\)"),
            TokenSpec_(Spec.COMMA, r","),
            TokenSpec_(Spec.GIBBERISH, r"[\s\S]"),
        ]
    )

    return tuple(reduce(inner, tokenizer(input), []))


def parser_reflective(name: Spec) -> Parser:
    return tok_(name) >> (lambda value: Token_(name, value))


def parser_generate() -> Parser:
    number = tok_(Spec.NUMBER) >> int
    everything = (
        parser_reflective(Spec.OP)
        | parser_reflective(Spec.NUMBER)
        | parser_reflective(Spec.LPAREN)
        | parser_reflective(Spec.RPAREN)
        | parser_reflective(Spec.COMMA)
        | parser_reflective(Spec.GIBBERISH)
    )

    mul = (
        tok_(Spec.OP, "mul")
        + tok_(Spec.LPAREN)
        + number
        + tok_(Spec.COMMA)
        + number
        + tok_(Spec.RPAREN)
    ) >> (lambda elem: Mul(elem[2], elem[4]))

    do = (tok_(Spec.OP, "do") + tok_(Spec.LPAREN) + tok_(Spec.RPAREN)) >> (
        lambda elem: Condition(True)
    )

    dont = (tok_(Spec.OP, "don't") + tok_(Spec.LPAREN) + tok_(Spec.RPAREN)) >> (
        lambda elem: Condition(False)
    )

    expr = do | dont | mul

    return expr + many(everything) + finished >> (
        lambda elem: (elem[0], tuple(elem[1]))
    )


def token_lstrip(tokens: tuple[Token, ...], pointer: int) -> int:
    return next(
        (
            pointer + idx
            for idx, token in enumerate(tokens[pointer:])
            if token.type == Spec.OP.name
        ),
        len(tokens),
    )


def parse(parser: Parser, tokens: tuple[Token, ...]) -> tuple[Expr, ...]:
    result = []

    while tokens:
        try:
            expr, tokens = parser.parse(tokens)
            result.append(expr)

        except NoParseError:
            tokens = tokens[1:]

    return tuple(result)


def evaluate_skip_condition(expressions: tuple[Expr, ...]) -> int:
    return reduce(
        operator.add,
        (
            expression.evaluate()
            for expression in expressions
            if isinstance(expression, Mul)
        ),
    )


def evaluate_with_condition(expressions: tuple[Expr, ...]) -> int:
    def reducer(current: tuple[bool, int], incoming: Expr) -> tuple[bool, int]:
        condition, result = current

        match incoming:
            case Mul():
                return (
                    condition,
                    (result + incoming.evaluate()) if condition else result,
                )

            case Condition():
                return (incoming.can_proceed, result)

            case _:
                raise Exception("Unknown expression")

    return reduce(reducer, expressions, (True, 0))[-1]


def part1(input: str) -> int:
    return evaluate_skip_condition(parse(parser_generate(), tokenize(input.strip())))


def part2(input: str) -> int:
    return evaluate_with_condition(parse(parser_generate(), tokenize(input.strip())))


def main():
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
