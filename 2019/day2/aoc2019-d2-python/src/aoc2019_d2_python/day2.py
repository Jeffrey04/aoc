import operator
from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from itertools import product
from operator import itemgetter
from sys import stdin

from funcparserlib.lexer import Token, TokenSpec, make_tokenizer
from funcparserlib.parser import Parser, finished, many, tok


class IntSpec(Enum):
    INT = auto()
    COMMA = auto()


class Op(ABC):
    code: int
    offset: int


@dataclass
class Add(Op):
    code: int
    alpha: int
    beta: int
    position: int
    offset: int

    def evaluate(self, memory: tuple[Token, ...]) -> tuple[Token, ...]:
        return memory_replace(
            memory,
            self.position,
            make_token_number(
                memory_get_number(memory, self.alpha)
                + memory_get_number(memory, self.beta),
            ),
        )


@dataclass
class Mul(Op):
    code: int
    alpha: int
    beta: int
    position: int
    offset: int

    def evaluate(self, memory: tuple[Token, ...]) -> tuple[Token, ...]:
        return memory_replace(
            memory,
            self.position,
            make_token_number(
                parse_number(memory[self.alpha]) * parse_number(memory[self.beta]),
            ),
        )


@dataclass
class Halt(Op):
    code: int
    offset: int

    def evaluate(self, memory: tuple[int, ...]) -> tuple[int, ...]:
        return memory


@dataclass
class Unknown(Op):
    code: int
    offset: int

    def evaluate(self, _) -> tuple[int, ...]:
        raise Exception("Something is wrong")


def make_token_number(number: int) -> Token:
    return Token(IntSpec.INT.name, str(number))


def tokenize(input: str) -> tuple[Token, ...]:
    tokenizer = make_tokenizer(
        [
            TokenSpec(IntSpec.INT.name, r"\d+"),
            TokenSpec(IntSpec.COMMA.name, r","),
        ]
    )

    return tuple(
        token for token in tokenizer(input) if token.type != IntSpec.COMMA.name
    )


def parser_generate() -> Parser:
    number = tok(IntSpec.INT.name) >> int

    add_components = (tok(IntSpec.INT.name, "1") >> int, number, number, number)
    add = reduce(operator.add, add_components) >> (
        lambda elem: Add(elem[0], elem[1], elem[2], elem[3], len(add_components))
    )

    mul_components = (tok(IntSpec.INT.name, "2") >> int, number, number, number)
    mul = reduce(operator.add, mul_components) >> (
        lambda elem: Mul(elem[0], elem[1], elem[2], elem[3], len(mul_components))
    )

    halt_components = (tok(IntSpec.INT.name, "99") >> int,)
    halt = reduce(operator.add, halt_components) >> (
        lambda code: Halt(code, len(halt_components))
    )

    error_components = (number,)
    error = reduce(operator.add, error_components) >> (
        lambda code: Unknown(code, len(error_components))
    )

    expr = add | mul | halt | error
    grammar = expr + many(number) + finished >> itemgetter(0)

    return grammar


def parse_memory(tokens: tuple[Token, ...]) -> tuple[int, ...]:
    number = tok(IntSpec.INT.name) >> int

    memory = many(number) + finished >> itemgetter(0)

    return memory.parse(tokens)


def parse_number(token: Token) -> int:
    number = tok(IntSpec.INT.name) >> int

    return number.parse((token,))


def memory_get_number(memory: tuple[Token, ...], position: int) -> int:
    return parse_number(memory[position])


def memory_replace(
    memory: tuple[Token, ...], position: int, token: Token
) -> tuple[Token, ...]:
    return (*memory[:position], token, *memory[position + 1 :])


def evaluate(parser: Parser, memory: tuple[Token, ...]) -> tuple[int, ...]:
    pointer = 0
    while True:
        if len(memory) <= pointer:
            break

        match expr := parser.parse(memory[pointer:]):
            case Add():
                memory = expr.evaluate(memory)
                pointer += expr.offset

            case Mul():
                memory = expr.evaluate(memory)
                pointer += expr.offset

            case Halt():
                break

            case Unknown():
                expr.evaluate(memory)

    return parse_memory(memory)


def part1(input: str) -> int:
    memory = tokenize(input.strip())

    return evaluate_overwritten(memory, 12, 2)


def part2(input: str) -> int:
    memory = tokenize(input.strip())

    return next(
        (100 * noun + verb)
        for noun in range(len(memory))
        for verb in range(len(memory))
        if (evaluate_overwritten(memory, noun, verb) == 19690720)
    )


def evaluate_overwritten(memory: tuple[Token, ...], noun: int, verb: int):
    return evaluate(
        parser_generate(),
        (
            memory[0],
            make_token_number(noun),
            make_token_number(verb),
            *memory[3:],
        ),
    )[0]


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
