from collections.abc import Generator, Iterator
from dataclasses import dataclass, field
from enum import Enum
from itertools import combinations
from queue import PriorityQueue
from sys import stdin
from typing import Type

import structlog

logger = structlog.get_logger()

CHEAT_OLD_TIME = 2
CHEAT_MAX_TIME = 20

type Trail = tuple[Point, ...]


class Symbol(Enum):
    Wall = "#"
    Start = "S"
    End = "E"


@dataclass
class Wall:
    pass


@dataclass
class Track:
    pass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(order=True)
class Node:
    time: int
    point: Point = field(compare=False)
    trail: Trail = field(compare=False)


@dataclass
class RaceTrack:
    tiles: dict[Point, Track | Wall]
    start: Point
    end: Point
    width: int
    height: int


def parse(input: str) -> RaceTrack:
    board = tuple(input.strip().splitlines())

    return RaceTrack(
        {point: Wall() for point in search(board, Symbol.Wall)},
        next(search(board, Symbol.Start)),
        next(search(board, Symbol.End)),
        len(board[0]),
        len(board),
    )


def search(input: tuple[str, ...], symbol: Symbol) -> Generator[Point, None, None]:
    return (
        Point(x, y)
        for y, row in enumerate(input)
        for x, item in enumerate(row)
        if item == symbol.value
    )


def check_point_is_in_track(race_track: RaceTrack, point: Point) -> bool:
    return 0 <= point.x < race_track.width and 0 <= point.y < race_track.height


def check_point_is_type(race_track: RaceTrack, point: Point, cls: Type) -> bool:
    return isinstance(race_track.tiles.get(point, Track()), cls)


def find_neighbour(race_track: RaceTrack, point: Point) -> Generator[Point, None, None]:
    return (
        neighbour
        for neighbour in (
            Point(point.x + 1, point.y),
            Point(point.x - 1, point.y),
            Point(point.x, point.y + 1),
            Point(point.x, point.y - 1),
        )
        if check_point_is_in_track(race_track, neighbour)
    )


def find_best_track(race_track: RaceTrack) -> Trail:
    result = (race_track.start,)

    while True:
        if result[-1] == race_track.end:
            break

        result += (
            next(
                neighbour
                for neighbour in find_neighbour(race_track, result[-1])
                if check_point_is_type(race_track, neighbour, Track)
                and (neighbour != result[-2] if len(result) > 1 else True)
            ),
        )

    return result


def get_pair_distance(start: Point, end: Point) -> int:
    return abs(start.x - end.x) + abs(start.y - end.y)


def get_tracks(race_track: RaceTrack) -> Generator[Point, None, None]:
    return (
        point
        for point in (
            Point(x, y)
            for x in range(race_track.width)
            for y in range(race_track.height)
        )
        if check_point_is_type(race_track, point, Track)
    )


def find_time_cheated(
    race_track: RaceTrack, trail: Trail
) -> Iterator[tuple[tuple[Point, Point], int]]:
    return filter(
        lambda item: item[-1] != 0,
        (
            ((trail[start_idx], trail[end_idx]), (end_idx - start_idx) - CHEAT_OLD_TIME)
            for (start_idx, end_idx) in combinations(range(len(trail)), 2)
            if get_pair_distance(trail[start_idx], trail[end_idx]) == CHEAT_OLD_TIME
        ),
    )


def find_time_cheated_new_rule(
    race_track: RaceTrack, trail: Trail
) -> Iterator[tuple[tuple[Point, Point], int]]:
    return filter(
        lambda item: item[-1] != 0,
        (
            (
                (trail[start_idx], trail[end_idx]),
                (end_idx - start_idx)
                - get_pair_distance(trail[start_idx], trail[end_idx]),
            )
            for (start_idx, end_idx) in combinations(range(len(trail)), 2)
            if get_pair_distance(trail[start_idx], trail[end_idx]) <= CHEAT_MAX_TIME
        ),
    )  # type: ignore


def part1(input: str) -> int:
    race_track = parse(input)

    return len(
        tuple(
            time_saved
            for _, time_saved in find_time_cheated(
                race_track, find_best_track(race_track)
            )
            if time_saved >= 100
        )
    )


def part2(input: str) -> int:
    race_track = parse(input)

    return len(
        tuple(
            time_saved
            for _, time_saved in find_time_cheated_new_rule(
                race_track, find_best_track(race_track)
            )
            if time_saved >= 100
        )
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
