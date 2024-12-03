import operator
from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from sys import stdin
from typing import Any, Callable

from funcparserlib.lexer import Token, TokenSpec, make_tokenizer
from funcparserlib.parser import NoParseError, finished, many, tok


class SpecGen(Enum):
    INS_MUL = auto()
    INS_DO = auto()
    INS_DONT = auto()
    GIBBERISH = auto()


class SpecMul(Enum):
    OP = auto()
    LPAREN = auto()
    RPAREN = auto()
    NUMBER = auto()
    COMMA = auto()


class Expr(ABC):
    pass


@dataclass
class ExprMul(Expr):
    alpha: int
    beta: int

    def evaluate(self) -> int:
        return operator.mul(self.alpha, self.beta)

    def __str__(self) -> str:
        return f"mul({self.alpha},{self.beta})"


@dataclass
class ExprCondition(Expr):
    can_proceed: bool


def tokenize(input: str) -> tuple[Token, ...]:
    tokenizer = make_tokenizer(
        [
            TokenSpec(SpecGen.INS_DONT.name, r"don\'t\(\)"),
            TokenSpec(SpecGen.INS_DO.name, r"do\(\)"),
            TokenSpec(SpecGen.INS_MUL.name, r"mul\(\d{1,3},\d{1,3}\)"),
            TokenSpec(SpecGen.GIBBERISH.name, r"[\s\S]"),
        ]
    )

    return tuple(
        token for token in tokenizer(input) if token.type != SpecGen.GIBBERISH.name
    )


def tokenize_mul(input: str) -> tuple[Token, ...]:
    tokenizer = make_tokenizer(
        [
            TokenSpec(SpecMul.OP.name, r"mul"),
            TokenSpec(SpecMul.LPAREN.name, r"\("),
            TokenSpec(SpecMul.RPAREN.name, r"\)"),
            TokenSpec(SpecMul.COMMA.name, r","),
            TokenSpec(SpecMul.NUMBER.name, r"\d{1,3}"),
        ]
    )

    return tuple(tokenizer(input))


def parse(
    tokens: tuple[Token, ...],
) -> tuple[Expr, ...]:
    do = tok(SpecGen.INS_DO.name) >> (lambda _: ExprCondition(True))
    dont = tok(SpecGen.INS_DONT.name) >> (lambda _: ExprCondition(False))
    condition = do | dont

    mul = tok(SpecGen.INS_MUL.name) >> (lambda input: parser_mul(tokenize_mul(input)))

    program = many(mul | condition) + finished >> operator.itemgetter(0)

    return tuple(program.parse(tokens))


def parser_mul(tokens: tuple[Token, ...]) -> ExprMul:
    number = tok(SpecMul.NUMBER.name) >> int
    operation = (
        tok(SpecMul.OP.name)
        + tok(SpecMul.LPAREN.name)
        + number
        + tok(SpecMul.COMMA.name)
        + number
        + tok(SpecMul.RPAREN.name)
    ) >> (lambda elem: ExprMul(elem[2], elem[4]))
    expression = operation + finished >> operator.itemgetter(0)

    return expression.parse(tokens)


def evaluate_skip_condition(expressions: tuple[Expr, ...]) -> int:
    return reduce(
        operator.add,
        (
            expression.evaluate()
            for expression in expressions
            if isinstance(expression, ExprMul)
        ),
    )


def evaluate_with_condition(expressions: tuple[Expr, ...]) -> int:
    def reducer(
        current: tuple[bool, int], incoming: ExprMul | ExprCondition
    ) -> tuple[bool, int]:
        condition, result = current

        match incoming:
            case ExprMul():
                return (
                    condition,
                    (result + incoming.evaluate()) if condition else result,
                )

            case ExprCondition():
                return (incoming.can_proceed, result)

    return reduce(reducer, expressions, (True, 0))[-1]


def part1(input: str) -> int:
    return evaluate_skip_condition(parse(tokenize(input)))


def part2(input: str) -> int:
    return evaluate_with_condition(parse(tokenize(input)))


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
