from collections.abc import Generator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from functools import partial
from itertools import combinations
from queue import PriorityQueue
from sys import stdin

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


def find_best_track(
    race_track: RaceTrack, start: Point | None = None, end: Point | None = None
) -> tuple[int, Trail]:
    open = PriorityQueue()
    open.put(Node(0, start or race_track.start, (start or race_track.start,)))
    visited = {}

    while not open.empty():
        current = open.get()

        if current.point == (end or race_track.end):
            return current.time, current.trail
        elif visited.get(current.point, False):
            continue

        visited[current.point] = True

        if not isinstance(race_track.tiles.get(current.point, Track()), Wall):
            for point in find_neighbour(race_track, current.point):
                open.put(Node(current.time + 1, point, current.trail + (point,)))

    raise Exception("There is no path")


def find_track_time(race_track: RaceTrack) -> int:
    # FIXME still needed?
    return race_track.width * race_track.height - len(race_track.tiles) - 1


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
        if isinstance(race_track.tiles.get(point, Track()), Track)
    )


def find_time_cheated(
    race_track: RaceTrack, best_time: int, trail: Trail
) -> Generator[tuple[tuple[Point, Point], int], None, None]:
    return filter(
        None,
        (
            find_time_saved(track_pair, race_track=race_track, best_time=best_time)
            for track_pair in (
                (start, end, CHEAT_OLD_TIME)
                for (start, end) in combinations(trail, 2)
                if get_pair_distance(start, end) == CHEAT_OLD_TIME
            )
        ),
    )  # type: ignore


def find_time_saved(
    track_pair: tuple[Point, Point, int], race_track: RaceTrack, best_time: int
) -> tuple[tuple[Point, Point], int] | None:
    start, end, distance = track_pair

    time_save = find_best_track(race_track, start, end)[0] - distance

    if time_save > 0:
        return (start, end), time_save

    return None


def find_time_cheated_new_rule(
    race_track: RaceTrack, best_time: int, trail: Trail
) -> Generator[tuple[tuple[Point, Point], int], None, None]:
    with ProcessPoolExecutor() as executor:
        return filter(
            None,
            executor.map(
                partial(find_time_saved, race_track=race_track, best_time=best_time),
                (
                    (start, end, distance)
                    for start, end, distance in (
                        (start, end, get_pair_distance(start, end))
                        for (start, end) in combinations(trail, 2)
                    )
                    if distance <= CHEAT_MAX_TIME
                ),
                chunksize=1000,
            ),
        )  # type: ignore


def part1(input: str) -> int:
    race_track = parse(input)

    return len(
        tuple(
            time_saved
            for _, time_saved in find_time_cheated(
                race_track, *find_best_track(race_track)
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
                race_track, *find_best_track(race_track)
            )
            if time_saved >= 100
        )
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
