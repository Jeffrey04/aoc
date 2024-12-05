import operator
from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from operator import itemgetter
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
    offset: int


@dataclass
class Mul(Expr):
    alpha: int
    beta: int
    offset: int

    def evaluate(self) -> int:
        return self.alpha * self.beta

    def __str__(self) -> str:
        return f"mul({self.alpha},{self.beta})"


@dataclass
class Condition(Expr):
    can_proceed: bool
    offset: int


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


def parser_generate() -> Parser:
    number = tok_(Spec.NUMBER) >> int
    everything = (
        tok_(Spec.OP)
        | tok_(Spec.NUMBER)
        | tok_(Spec.LPAREN)
        | tok_(Spec.RPAREN)
        | tok_(Spec.COMMA)
        | tok_(Spec.GIBBERISH)
    )

    mul_components = (
        tok_(Spec.OP, "mul"),
        tok_(Spec.LPAREN),
        number,
        tok_(Spec.COMMA),
        number,
        tok_(Spec.RPAREN),
    )
    mul = reduce(operator.add, mul_components) >> (
        lambda elem: Mul(elem[2], elem[4], len(mul_components))
    )

    do_components = (
        tok_(Spec.OP, "do"),
        tok_(Spec.LPAREN),
        tok_(Spec.RPAREN),
    )
    do = reduce(operator.add, do_components) >> (
        lambda elem: Condition(True, len(do_components))
    )

    dont_components = (
        tok_(Spec.OP, "don't"),
        tok_(Spec.LPAREN),
        tok_(Spec.RPAREN),
    )
    dont = reduce(operator.add, dont_components) >> (
        lambda elem: Condition(False, len(dont_components))
    )

    expr = do | dont | mul

    return expr + many(everything) + finished >> itemgetter(0)


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
    result, pointer = [], token_lstrip(tokens, 0)

    while True:
        if pointer == len(tokens):
            break

        try:
            expr = parser.parse(tokens[pointer:])
            pointer = token_lstrip(tokens, pointer + expr.offset)
            result.append(expr)

        except NoParseError:
            pointer = token_lstrip(tokens, pointer + 1)

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
