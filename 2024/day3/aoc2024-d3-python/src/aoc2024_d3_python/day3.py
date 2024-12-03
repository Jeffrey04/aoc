import operator
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from sys import stdin
from typing import Callable

from funcparserlib.lexer import Token, TokenSpec, make_tokenizer
from funcparserlib.parser import NoParseError, tok


class SpecName(Enum):
    INS_DONT = auto()
    INS_DO = auto()
    INS_MUL = auto()
    INT = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    GIBBERISH = auto()


@dataclass
class BinaryExpression:
    op: Callable[[int, int], int]
    alpha: int
    beta: int

    def evaluate(self) -> int:
        return self.op(self.alpha, self.beta)

    def __str__(self) -> str:
        return f"mul({self.alpha},{self.beta})"


@dataclass
class Condition:
    can_proceed: bool


def tokenize(input: str) -> tuple[Token, ...]:
    tokenizer = make_tokenizer(
        [
            TokenSpec(SpecName.INS_DONT.name, r"don\'t"),
            TokenSpec(SpecName.INS_DO.name, r"do"),
            TokenSpec(SpecName.INS_MUL.name, r"mul"),
            TokenSpec(SpecName.INT.name, r"\d{1,3}"),
            TokenSpec(SpecName.LPAREN.name, r"\("),
            TokenSpec(SpecName.RPAREN.name, r"\)"),
            TokenSpec(SpecName.COMMA.name, r"\,"),
            TokenSpec(SpecName.GIBBERISH.name, r"."),
        ]
    )

    return tuple(tokenizer(input))


def parse(tokens: tuple[Token, ...]) -> list[BinaryExpression]:
    result = []

    number = tok(SpecName.INT.name) >> int
    mul = tok(SpecName.INS_MUL.name) >> (lambda _: operator.mul)

    binary_components = [
        mul,
        tok(SpecName.LPAREN.name),
        number,
        tok(SpecName.COMMA.name),
        number,
        tok(SpecName.RPAREN.name),
    ]
    binary = reduce(operator.add, binary_components) >> (
        lambda expr: BinaryExpression(expr[0], expr[2], expr[4])
    )

    condition_component = [
        (tok(SpecName.INS_DO.name) >> (lambda _: True))
        | (tok(SpecName.INS_DONT.name) >> (lambda _: False)),
        tok(SpecName.LPAREN.name),
        tok(SpecName.RPAREN.name),
    ]
    condition = reduce(operator.add, condition_component) >> (
        lambda expr: Condition(expr[0])
    )

    grammar = condition | binary

    current = 0
    while True:
        try:
            if current >= len(tokens):
                break

            instruction = grammar.parse(tokens[current:])
            result.append(instruction)

            match instruction:
                case BinaryExpression():
                    current += len(binary_components)

                case Condition():
                    current += len(condition_component)

        except NoParseError:
            current += 1

    return result


def evaluate_skip_condition(expressions: list[BinaryExpression]) -> int:
    return reduce(
        operator.add,
        (
            expression.evaluate()
            for expression in expressions
            if isinstance(expression, BinaryExpression)
        ),
    )


def evaluate_with_condition(expressions: list[BinaryExpression]) -> int:
    def reducer(
        current: tuple[bool, int], incoming: BinaryExpression | Condition
    ) -> tuple[bool, int]:
        condition, result = current

        match incoming:
            case BinaryExpression():
                return (
                    condition,
                    (result + incoming.evaluate()) if condition else result,
                )

            case Condition():
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
