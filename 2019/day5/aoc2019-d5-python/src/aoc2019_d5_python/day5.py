import operator
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from sys import stdin

from aoc2019_d2_python.day2 import Add, Halt, IntSpec, Mul, Op, Unknown
from funcparserlib.lexer import Token, TokenSpec, make_tokenizer
from funcparserlib.parser import finished, many, tok


class OpType(Enum):
    ADD = "01"
    MUL = "02"
    INPUT = "03"
    OUTPUT = "04"
    JUMP_IF_TRUE = "05"
    JUMP_IF_FALSE = "06"
    LESS_THAN = "07"
    EQUAL = "08"
    HALT = "99"
    UNKNOWN = None


class Mode(ABC):
    code: int
    value: int


@dataclass
class Position(Mode):
    code: int
    value: int


@dataclass
class Immediate(Mode):
    code: int
    value: int


@dataclass
class JumpIfTrue5(Op):
    code: int
    test: Mode
    pointer: Mode
    offset: int

    def evaluate(
        self, memory: tuple[int, ...], current: int
    ) -> tuple[tuple[int, ...], int]:
        match memory_get_value(memory, self.test) != 0:
            case True:
                return memory, memory_get_value(memory, self.pointer)

            case False:
                return memory, current + self.offset


@dataclass
class JumpIfFalse5(Op):
    code: int
    test: Mode
    pointer: Mode
    offset: int

    def evaluate(
        self, memory: tuple[int, ...], current: int
    ) -> tuple[tuple[int, ...], int]:
        match memory_get_value(memory, self.test) == 0:
            case True:
                return memory, memory_get_value(memory, self.pointer)

            case False:
                return memory, current + self.offset


@dataclass
class LessThan5(Op):
    code: int
    alpha: Mode
    beta: Mode
    position: int
    offset: int

    def evaluate(self, memory: tuple[int, ...]) -> tuple[int, ...]:
        match (
            memory_get_value(memory, self.alpha)  # fmt: skip
            < memory_get_value(memory, self.beta)
        ):
            case True:
                return memory_replace(memory, self.position, 1)

            case False:
                return memory_replace(memory, self.position, 0)


@dataclass
class Equal5(Op):
    code: int
    alpha: Mode
    beta: Mode
    position: int
    offset: int

    def evaluate(self, memory: tuple[int, ...]) -> tuple[int, ...]:
        match (
            memory_get_value(memory, self.alpha)  # fmt: skip
            == memory_get_value(memory, self.beta)
        ):
            case True:
                return memory_replace(memory, self.position, 1)

            case False:
                return memory_replace(memory, self.position, 0)


@dataclass
class Input5(Op):
    code: int
    position: int
    offset: int

    def evaluate(self, memory: tuple[int, ...], input: int) -> tuple[int, ...]:
        return memory_replace(memory, self.position, input)


@dataclass
class Output5(Op):
    code: int
    position: Mode
    offset: int

    def evaluate(self, memory: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
        return memory, memory_get_value(memory, self.position)


@dataclass
class Add5(Add):
    alpha: Mode
    beta: Mode
    position: int

    def evaluate(self, memory: tuple[int, ...]) -> tuple[int, ...]:
        return memory_replace(
            memory,
            self.position,
            memory_get_value(memory, self.alpha) + memory_get_value(memory, self.beta),
        )


@dataclass
class Mul5(Mul):
    alpha: Mode
    beta: Mode
    position: int

    def evaluate(self, memory: tuple[int, ...]) -> tuple[int, ...]:
        return memory_replace(
            memory,
            self.position,
            memory_get_value(memory, self.alpha) * memory_get_value(memory, self.beta),
        )


def tokenize(input: str) -> tuple[Token, ...]:
    tokenizer = make_tokenizer(
        [
            TokenSpec(IntSpec.INT.name, r"\-?\d+"),
            TokenSpec(IntSpec.COMMA.name, r","),
        ]
    )

    return tuple(
        token for token in tokenizer(input) if token.type != IntSpec.COMMA.name
    )


def memory_replace(
    memory: tuple[int, ...], position: int, value: int
) -> tuple[int, ...]:
    return (*memory[:position], value, *memory[position + 1 :])


def memory_create(tokens: tuple[Token, ...]) -> tuple[int, ...]:
    number = tok(IntSpec.INT.name) >> int

    memory = many(number) + finished >> operator.itemgetter(0)

    return memory.parse(tokens)


def memory_get_value(memory: tuple[int, ...], mode: Mode) -> int:
    match mode:
        case Position():
            return memory[mode.value]

        case Immediate():
            return mode.value


def parameter_get_mode(opcode: str, value: int, position: int) -> Mode:
    match int(opcode[-(3 + position)]):
        case 0:
            return Position(0, value)

        case 1:
            return Immediate(1, value)


def opcode_get_type(code: int) -> OpType:
    match str(code).zfill(5)[-2:]:
        case OpType.ADD.value:
            return OpType.ADD

        case OpType.MUL.value:
            return OpType.MUL

        case OpType.INPUT.value:
            return OpType.INPUT

        case OpType.OUTPUT.value:
            return OpType.OUTPUT

        case OpType.JUMP_IF_TRUE.value:
            return OpType.JUMP_IF_TRUE

        case OpType.JUMP_IF_FALSE.value:
            return OpType.JUMP_IF_FALSE

        case OpType.LESS_THAN.value:
            return OpType.LESS_THAN

        case OpType.EQUAL.value:
            return OpType.EQUAL

        case OpType.HALT.value:
            return OpType.HALT

        case _:
            return OpType.UNKNOWN


def opcode_pad(opcode: int, component_count: int) -> str:
    return str(opcode).zfill(component_count + 1)


def parse(memory: tuple[int, ...]) -> Op:
    match opcode_get_type(memory[0]):
        case OpType.ADD:
            components = memory[:4]
            opcode_padded = opcode_pad(components[0], len(components))
            return Add5(
                components[0],
                parameter_get_mode(opcode_padded, components[1], 0),
                parameter_get_mode(opcode_padded, components[2], 1),
                components[3],
                len(components),
            )

        case OpType.MUL:
            components = memory[:4]
            opcode_padded = opcode_pad(components[0], len(components))
            return Mul5(
                components[0],
                parameter_get_mode(opcode_padded, components[1], 0),
                parameter_get_mode(opcode_padded, components[2], 1),
                components[3],
                len(components),
            )

        case OpType.INPUT:
            components = memory[:2]
            return Input5(components[0], components[1], len(components))

        case OpType.OUTPUT:
            components = memory[:2]
            opcode_padded = opcode_pad(components[0], len(components))
            return Output5(
                components[0],
                parameter_get_mode(opcode_padded, components[1], 0),
                len(components),
            )

        case OpType.JUMP_IF_TRUE:
            components = memory[:3]
            opcode_padded = opcode_pad(components[0], len(components))
            return JumpIfTrue5(
                components[0],
                parameter_get_mode(opcode_padded, components[1], 0),
                parameter_get_mode(opcode_padded, components[2], 1),
                len(components),
            )

        case OpType.JUMP_IF_FALSE:
            components = memory[:3]
            opcode_padded = opcode_pad(components[0], len(components))
            return JumpIfFalse5(
                components[0],
                parameter_get_mode(opcode_padded, components[1], 0),
                parameter_get_mode(opcode_padded, components[2], 1),
                len(components),
            )

        case OpType.LESS_THAN:
            components = memory[:4]
            opcode_padded = opcode_pad(components[0], len(components))
            return LessThan5(
                components[0],
                parameter_get_mode(opcode_padded, components[1], 0),
                parameter_get_mode(opcode_padded, components[2], 1),
                components[3],
                len(components),
            )

        case OpType.EQUAL:
            components = memory[:4]
            opcode_padded = opcode_pad(components[0], len(components))
            return Equal5(
                components[0],
                parameter_get_mode(opcode_padded, components[1], 0),
                parameter_get_mode(opcode_padded, components[2], 1),
                components[3],
                len(components),
            )

        case OpType.HALT:
            components = memory[:1]
            return Halt(components[0], len(components))

        case OpType.UNKNOWN:
            components = memory[:1]
            return Unknown(components[0], len(components))


def evaluate(tokens: tuple[Token, ...], input: int) -> int:
    result = None

    memory = memory_create(tokens)
    pointer = 0

    while True:
        if len(memory) <= pointer:
            break

        match expr := parse(memory[pointer:]):
            case Add5() | Mul5() | LessThan5() | Equal5():
                memory = expr.evaluate(memory)
                pointer += expr.offset

            case Input5():
                memory = expr.evaluate(memory, input)
                pointer += expr.offset

            case Output5():
                memory, result = expr.evaluate(memory)
                pointer += expr.offset

            case JumpIfTrue5() | JumpIfFalse5():
                memory, pointer = expr.evaluate(memory, pointer)

            case Halt():
                break

            case Unknown():
                expr.evaluate(memory)

    assert isinstance(result, int)

    return result


def part1(input: str) -> int:
    return evaluate(tokenize(input.strip()), 1)


def part2(input: str) -> int:
    return evaluate(tokenize(input.strip()), 5)


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
