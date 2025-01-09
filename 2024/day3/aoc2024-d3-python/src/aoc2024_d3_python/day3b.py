import operator
from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from sys import stdin
from typing import Any

from funcparserlib.lexer import Token, TokenSpec, make_tokenizer
from funcparserlib.parser import Parser, finished, many, tok


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
    tokenizer = make_tokenizer(
        [
            TokenSpec_(
                Spec.OP, r"mul(?=\(\d{1,3},\d{1,3}\))|do(?=\(\))|don\'t(?=\(\))"
            ),
            TokenSpec_(Spec.NUMBER, r"\d{1,3}"),
            TokenSpec_(Spec.LPAREN, r"\("),
            TokenSpec_(Spec.RPAREN, r"\)"),
            TokenSpec_(Spec.COMMA, r","),
            TokenSpec_(Spec.GIBBERISH, r"[\s\S]"),
        ]
    )

    return tuple(
        token for token in tokenizer(input) if token.type != Spec.GIBBERISH.name
    )


def parse(tokens: tuple[Token, ...]) -> tuple[Expr, ...]:
    number = tok_(Spec.NUMBER) >> int
    everything = (
        tok_(Spec.NUMBER) | tok_(Spec.LPAREN) | tok_(Spec.RPAREN) | tok_(Spec.COMMA)
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
    call = many(everything) + expr + many(everything) >> operator.itemgetter(1)

    program = many(call) + finished >> (lambda elem: tuple(elem[0]))

    return program.parse(tokens)


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
    return evaluate_skip_condition(parse(tokenize(input.strip())))


def part2(input: str) -> int:
    return evaluate_with_condition(parse(tokenize(input.strip())))


def main():
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
