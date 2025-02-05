import operator
from dataclasses import dataclass
from enum import Enum
from sys import stdin
from typing import Callable, Literal, Sequence

type StateValue = Literal[0, 1]
type State = dict[str, StateValue]


class Number(Enum):
    X = "x"
    Y = "y"
    Z = "z"


class Separator(Enum):
    State = ":"
    Gate = "->"


class Gates(Enum):
    AND = "AND"
    XOR = "XOR"
    OR = "OR"


@dataclass
class Instruction:
    alpha: str
    beta: str
    output: str
    gate: Callable[[StateValue, StateValue], StateValue]


def parse(input: str) -> tuple[State, Sequence[Instruction]]:
    state = {}
    instructions = ()

    for line in input.strip().splitlines():
        if Separator.State.value in line:
            key, value = line.split(Separator.State.value)
            state[key.strip()] = int(value)

        elif Separator.Gate.value in line:
            instructions += (parse_instruction(line),)

    return state, instructions


def parse_instruction(line: str) -> Instruction:
    gate = None

    tokens = line.split(" ")

    match tokens:
        case tokens if Gates.AND.value in tokens:
            gate = operator.and_

        case tokens if Gates.XOR.value in tokens:
            gate = operator.xor

        case tokens if Gates.OR.value in tokens:
            gate = operator.or_

        case _:
            raise Exception("Unknown line")

    return Instruction(tokens[0], tokens[2], tokens[4], gate)


def evaluate(
    state: State, instructions: Sequence[Instruction]
) -> tuple[State, Sequence[Instruction]]:
    unevaluated = ()

    for instruction in instructions:
        try:
            state[instruction.output] = evaluate_instruction(state, instruction)
        except KeyError:
            unevaluated += (instruction,)

    return state, unevaluated


def evaluate_instruction(state: State, instruction: Instruction) -> StateValue:
    return instruction.gate(state[instruction.alpha], state[instruction.beta])


def evaluate_loop(state: State, instructions: Sequence[Instruction]) -> State:
    while instructions:
        state, instructions = evaluate(state, instructions)

    return state


def fetch(state: State, number: Number) -> Sequence[tuple[str, StateValue]]:
    keys = sorted((key for key in state.keys() if key.startswith(number.value)))

    return tuple((key, state[key]) for key in keys)


def convert(number: Sequence[tuple[str, StateValue]]) -> int:
    return sum(value * (2**pow) for pow, (_, value) in enumerate(number))


def part1(input: str) -> int:
    return convert(fetch(evaluate_loop(*parse(input)), Number.Z))


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input))


if __name__ == "__main__":
    main()
