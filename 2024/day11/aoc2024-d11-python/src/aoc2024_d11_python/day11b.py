import sys
from functools import partial, reduce
from itertools import chain, repeat
from math import floor, log10
from sys import stdin
from typing import Any, Callable, Generator

from genstates import Machine
from toolz import merge_with, pipe


def check_is_zero() -> Callable[[int], bool]:
    return lambda value: value == 0


def check_is_split() -> Callable[[int], bool]:
    return lambda value: len_digit(value) % 2 == 0


def check_is_multiply() -> Callable[[int], bool]:
    return lambda value: not (check_is_split()(value) or check_is_zero()(value))


def to_tuple(func) -> Callable[..., Any]:
    def inner(*arg, **kwargs) -> Any:
        return (func(*arg, **kwargs),)

    return inner


def len_digit(number: int) -> int:
    return floor(log10(number) + 1)


@to_tuple
def stone_increment(_, stone: int) -> int:
    assert stone == 0

    return 1


def stone_split(_, stone: int) -> tuple[int, int]:
    assert len_digit(stone) % 2 == 0

    return (
        int(stone / (10 ** (len_digit(stone) / 2))),
        int(stone % (10 ** (len_digit(stone) / 2))),
    )


@to_tuple
def stone_multiply(_, stone: int) -> int:
    return stone * 2024


def stone_transform(stone: int) -> tuple[int, ...]:
    result = ()

    if stone == 0:
        result = stone_increment(stone)

    elif len_digit(stone) % 2 == 0:
        result = stone_split(stone)

    else:
        result = stone_multiply(stone)

    return result


def blink(
    stones: tuple[int, ...], fsm: Machine, iterations: int = 1
) -> Generator[int, None, None]:
    return pipe(
        stones,
        *repeat(
            lambda current: chain.from_iterable(
                fsm.progress(fsm.initial, stone).do_action(stone) for stone in current
            ),
            iterations,
        ),
    )  # type: ignore


def blink_to_count(stones: tuple[int, ...], fsm: Machine, iterations: int = 1) -> int:
    return sum(
        pipe(
            {stone: 1 for stone in stones},
            *repeat(partial(blink_get_index, fsm=fsm), iterations),
        ).values()
    )


def blink_get_index(current: dict[int, int], fsm: Machine) -> dict[int, int]:
    return merge_with(
        sum,
        *(
            {stone: count_current}
            for stone_current, count_current in current.items()
            for stone in fsm.progress(fsm.initial, stone_current).do_action(  # type: ignore
                stone_current
            )
        ),
    )


def parse(input: str) -> tuple[int, ...]:
    return tuple(int(item) for item in input.strip().split(" "))


def part1(input: str) -> int:
    return len(tuple(blink(parse(input), get_fsm(), 25)))


def part2(input: str) -> int:
    return blink_to_count(parse(input), get_fsm(), 75)


def get_fsm() -> Machine:
    return Machine(
        {
            "machine": {"initial_state": "start"},
            "states": {
                "start": {
                    "transitions": {
                        "to_increment": {
                            "rule": "(check_is_zero)",
                            "destination": "incremented",
                        },
                        "to_split": {
                            "rule": "(check_is_split)",
                            "destination": "split",
                        },
                        "to_multiplied": {
                            "rule": "(check_is_multiply)",
                            "destination": "multiplied",
                        },
                    }
                },
                "incremented": {"action": "stone_increment"},
                "split": {"action": "stone_split"},
                "multiplied": {"action": "stone_multiply"},
            },
        },
        sys.modules[__name__],
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
