import re
from dataclasses import dataclass, field, is_dataclass, make_dataclass
from functools import reduce
from queue import PriorityQueue
from re import I
from sys import stdin

import structlog
from cytoolz.functoolz import memoize

logger = structlog.get_logger()


@dataclass(order=True)
class Node:
    cost: int
    towel: str = field(compare=False)
    progress: str = field(compare=False)


def parse(input: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    def reducer(
        current: tuple[tuple[str, ...], tuple[str, ...]], incoming: str
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        towels, patterns = current

        if "," in incoming:
            return towels + tuple(
                towel.strip() for towel in incoming.split(",")
            ), patterns

        else:
            return towels, patterns + (incoming.strip(),)

    return reduce(reducer, filter(None, input.strip().splitlines()), ((), ()))


@memoize
def combo_count(combinations, candidates: tuple[str, ...], nest: int = 0) -> int:
    assert is_dataclass(combinations)

    return reduce(
        lambda current, incoming: current
        + (
            combo_count(
                combinations,
                tuple(
                    child.split(";")[0]
                    for child in getattr(combinations, match.group(1))
                ),
                nest + 1,
            )
            if (match := re.match(r"\{(\w+)\}", incoming))
            else 1
        ),
        candidates,
        0,
    )


def pattern_match(towels: tuple[str, ...], pattern: str) -> dict[str, set[str]] | None:
    open = PriorityQueue()
    visited = {}
    combinations: dict[str, set[str]] = {}

    for towel in towels:
        if pattern.startswith(towel):
            combinations[towel] = {
                towel,
            }
            open.put(Node(len(combinations[towel]), towel, towel))

    while not open.empty():
        current = open.get()

        if current.progress == pattern or visited.get(
            (current.progress, current.towel)
        ):
            continue

        visited[(current.progress, current.towel)] = True

        for towel in towels:
            progress_incoming = current.progress + towel

            if pattern.startswith(progress_incoming):
                combinations[progress_incoming] = combinations.get(
                    progress_incoming, set()
                ).union({f"{{{current.progress}}};{towel}"})
                open.put(
                    Node(len(combinations[progress_incoming]), towel, progress_incoming)
                )

    return combinations if pattern in combinations else None


def part1(input) -> int:
    towels, patterns = parse(input)

    return len(
        tuple(filter(None, (pattern_match(towels, pattern) for pattern in patterns)))
    )


def part2(input) -> int:
    towels, patterns = parse(input)

    return sum(
        combo_count(
            make_dataclass(
                "combo", ((key, int) for key in combinations.keys()), frozen=True
            )(**{key: tuple(value) for key, value in combinations.items()}),
            tuple(combinations[pattern]),
        )
        for pattern, combinations in {
            pattern: pattern_match(towels, pattern) for pattern in patterns
        }.items()
        if combinations
    )


def main() -> None:
    input = stdin.read()

    # 235175479402719 too low
    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
