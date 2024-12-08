from curses.ascii import isalnum
from dataclasses import dataclass
from functools import partial
from itertools import chain, combinations, count
from operator import itemgetter
from sys import stdin

from toolz import groupby, itemmap


@dataclass
class Antenna:
    x: int
    y: int


@dataclass
class AntennaPair:
    alpha: Antenna
    beta: Antenna

    def diff(self) -> tuple[int, int]:
        return (
            self.beta.x - self.alpha.x,
            self.beta.y - self.alpha.y,
        )


def parse(input: str) -> tuple[tuple[int, int], dict[str, tuple[Antenna, ...]]]:
    lines = input.strip().splitlines()

    return (len(lines[0]), len(lines)), itemmap(
        lambda kvpair: (kvpair[0], tuple(point for _, point in kvpair[1])),
        groupby(
            itemgetter(0),
            (
                (item, Antenna(x, y))
                for y, row in enumerate(lines)
                for x, item in enumerate(row)
                if isalnum(item)
            ),
        ),
    )


def pair_antennas(*antennas: Antenna) -> tuple[AntennaPair, ...]:
    return tuple(AntennaPair(*pair) for pair in combinations(antennas, 2))


def find_antinodes(
    pair: AntennaPair, map_size: tuple[int, int], multiplier: int = 1
) -> tuple[tuple[int, int], ...]:
    diff = tuple(item * multiplier for item in pair.diff())

    return tuple(
        filter(
            partial(check_is_in_map, map_size=map_size),
            (
                (pair.alpha.x - diff[0], pair.alpha.y - diff[1]),
                (pair.beta.x + diff[0], pair.beta.y + diff[1]),
            ),
        )
    )


def populate_antinodes(
    pair: AntennaPair, map_size: tuple[int, int]
) -> tuple[tuple[int, int], ...]:
    result = []

    for multiplier in count():
        antinodes = find_antinodes(pair, map_size, multiplier)

        if not antinodes:
            break

        result.extend(antinodes)

    return tuple(result)


def check_is_in_map(incoming: tuple[int, int], map_size: tuple[int, int]) -> bool:
    return 0 <= incoming[0] < map_size[0] and 0 <= incoming[1] < map_size[1]


def part1(input: str) -> int:
    size, antenna_map = parse(input)

    return len(
        set(
            chain.from_iterable(
                find_antinodes(pair, size)
                for antennas in antenna_map.values()
                for pair in pair_antennas(*antennas)
                if len(antennas) > 1
            )
        )
    )


def part2(input: str) -> int:
    size, antenna_map = parse(input)

    return len(
        set(
            chain.from_iterable(
                populate_antinodes(pair, size)
                for antennas in antenna_map.values()
                for pair in pair_antennas(*antennas)
                if len(antennas) > 1
            )
        )
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
