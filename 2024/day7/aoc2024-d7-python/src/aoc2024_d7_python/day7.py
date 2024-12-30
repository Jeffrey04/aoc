import operator
from collections.abc import Callable
from itertools import product
from math import floor, log10
from sys import stdin

from toolz.functoolz import thread_first


def calculate(
    funcs: tuple[Callable[[int, int], int], ...], operands: tuple[int, ...]
) -> int:
    assert len(operands) - len(funcs) == 1

    return thread_first(operands[0], *(zip(funcs, operands[1:])))  # type: ignore


def check_can_calibrate(
    expected: int,
    operands: tuple[int, ...],
    funcs: tuple[Callable[[int, int], int], ...],
) -> bool:
    return next(
        filter(
            None,
            (
                calculate(funcs, operands) == expected
                for funcs in product(funcs, repeat=len(operands) - 1)
            ),
        ),
        False,
    )


def parse(input: str) -> tuple[tuple[int, tuple[int, ...]], ...]:
    return tuple(
        parse_line(*line.strip().split(":")) for line in input.strip().splitlines()
    )


def parse_line(expected: str, operands: str) -> tuple[int, tuple[int, ...]]:
    return int(expected), tuple(int(item) for item in operands.strip().split(" "))


def evaluate(
    input_parsed: tuple[tuple[int, tuple[int, ...]], ...],
    funcs: tuple[Callable[[int, int], int], ...],
):
    return sum(
        expected
        for expected, operands in input_parsed
        if check_can_calibrate(expected, operands, funcs)
    )


def part1(input: str) -> int:
    return evaluate(parse(input), (operator.mul, operator.add))


def int_concat(alpha: int, beta: int) -> int:
    return alpha * (10 ** floor(log10(beta) + 1)) + beta


def part2(input: str) -> int:
    return evaluate(parse(input), (operator.mul, operator.add, int_concat))


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
