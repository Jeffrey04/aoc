from collections.abc import Callable, Iterator, Sequence
from functools import reduce
from itertools import pairwise
from sys import stdin

from cytoolz.functoolz import compose, memoize
from cytoolz.itertoolz import last, sliding_window


def repeat(func: Callable[[int], int], iterations: int) -> Callable[[int], int]:
    assert iterations > 1

    return compose(*((func,) * iterations))


def iterate(func: Callable[[int], int], input: int, iterations: int) -> Iterator[int]:
    for _ in range(iterations):
        yield (input := func(input))


def get_ones(secret_number: int) -> int:
    return secret_number % 10


@memoize
def random_next(secret_number: int) -> int:
    mix_prune = compose(input_prune, input_mix)
    return mix_prune(
        mix_prune(
            mix_prune(secret_number, lambda item: item << 6),
            lambda item: item >> 5,
        ),
        lambda item: item << 11,
    )


def input_mix(secret_number: int, operation: Callable[[int], int]) -> int:
    return operation(secret_number) ^ secret_number


def input_prune(secret_number: int) -> int:
    return secret_number & (2**24 - 1)


def parse(input: str) -> Iterator[int]:
    return (int(line) for line in input.strip().splitlines())


def part1(input: str) -> int:
    repeated = repeat(random_next, 2000)

    return sum(repeated(secret_number) for secret_number in parse(input))


def ones_get_diff(ones: dict[int, tuple[int, ...]]) -> dict[int, Iterator[int]]:
    return {
        secret_number: ((a - b) for (a, b) in pairwise(values))
        for secret_number, values in ones.items()
    }


def part2(input: str) -> int:
    prices = {
        secret_number: tuple(
            get_ones(next_number)
            for next_number in iterate(random_next, secret_number, 2000)
        )
        for secret_number in parse(input)
    }

    sequence_set = set()
    sequence_to_price = []
    for secret_number, values in ones_get_diff(prices).items():
        result = {}

        for seq, price in tuple(
            zip(sliding_window(4, values), prices[secret_number][4:])
        )[::-1]:
            sequence_set.add(seq)

            if seq in result:
                continue

            result[seq] = price

        sequence_to_price.append(result)

    return max(
        *(
            sum(sequence.get(seq, 0) for sequence in sequence_to_price)
            for seq in sequence_set
        )
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
