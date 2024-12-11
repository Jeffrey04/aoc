from functools import reduce
from itertools import chain, repeat
from math import floor, log10
from sys import stdin
from typing import Any, Callable, Generator

from toolz import merge_with, pipe


def to_tuple(func) -> Callable[..., Any]:
    def inner(*arg, **kwargs) -> Any:
        return (func(*arg, **kwargs),)

    return inner


def len_digit(number: int) -> int:
    return floor(log10(number) + 1)


@to_tuple
def stone_increment(stone: int) -> int:
    assert stone == 0

    return 1


def stone_split(stone: int) -> tuple[int, int]:
    assert len_digit(stone) % 2 == 0

    return (
        int(stone / (10 ** (len_digit(stone) / 2))),
        int(stone % (10 ** (len_digit(stone) / 2))),
    )


@to_tuple
def stone_multiply(stone: int) -> int:
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


def blink(stones: tuple[int, ...], iterations: int = 1) -> Generator[int, None, None]:
    return reduce(
        lambda current, _: chain.from_iterable(
            stone_transform(stone) for stone in current
        ),
        range(iterations),
        stones,  # type: ignore
    )


def blink_to_count(stones: tuple[int, ...], iterations: int = 1) -> int:
    return sum(
        pipe(
            {stone: 1 for stone in stones},
            *repeat(blink_get_index, iterations),
        ).values()
    )


def blink_get_index(current: dict[int, int]) -> dict[int, int]:
    return merge_with(
        sum,
        *(
            {stone: count_current}
            for stone_current, count_current in current.items()
            for stone in stone_transform(stone_current)
        ),
    )


def parse(input: str) -> tuple[int, ...]:
    return tuple(int(item) for item in input.strip().split(" "))


def part1(input: str) -> int:
    return len(tuple(blink(parse(input), 25)))


def part2(input: str) -> int:
    return blink_to_count(parse(input), 75)


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
