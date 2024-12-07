import operator
from collections.abc import Callable
from itertools import product
from sys import stdin

from toolz import thread_first


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
        (
            True
            for funcs in product(funcs, repeat=len(operands) - 1)
            if calculate(funcs, operands) == expected
        ),
        False,
    )


def parse(input: str) -> tuple[tuple[int, tuple[int, ...]], ...]:
    return tuple(
        parse_line(*line.strip().split(":")) for line in input.strip().splitlines()
    )


def parse_line(expected: str, operands: str) -> tuple[int, tuple[int, ...]]:
    return int(expected), tuple(int(item) for item in operands.strip().split(" "))


def part1(input: str) -> int:
    return sum(
        expected
        for expected, operands in parse(input)
        if check_can_calibrate(expected, operands, (operator.mul, operator.add))
    )


def int_concat(alpha: int, beta: int) -> int:
    return int(f"{alpha}{beta}")


def part2(input: str) -> int:
    return sum(
        expected
        for expected, operands in parse(input)
        if check_can_calibrate(
            expected, operands, (int_concat, operator.mul, operator.add)
        )
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
