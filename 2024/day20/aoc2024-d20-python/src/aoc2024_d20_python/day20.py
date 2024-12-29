from collections.abc import Generator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from functools import partial
from itertools import product
from queue import PriorityQueue
from sys import stdin

import structlog

logger = structlog.get_logger()

CHEAT_MAX_TIME = 20


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


def check_wall_can_pass_through(race_track: RaceTrack, wall: Point) -> bool:
    return all(
        check_point_is_in_track(race_track, neighbour)
        and isinstance(race_track.tiles.get(neighbour, Track()), Track)
        for neighbour in (
            Point(wall.x, wall.y + 1),
            Point(wall.x, wall.y - 1),
        )
    ) or all(
        check_point_is_in_track(race_track, neighbour)
        and isinstance(race_track.tiles.get(neighbour, Track()), Track)
        for neighbour in (
            Point(wall.x + 1, wall.y),
            Point(wall.x - 1, wall.y),
        )
    )


def check_wall_is_facing_track(race_track: RaceTrack, wall: Point) -> bool:
    return any(
        isinstance(race_track.tiles.get(neighbour, Track()), Track)
        for neighbour in find_neighbour(race_track, wall)
    )


def check_wall_pair_is_accessible(
    race_track: RaceTrack, start: Point, end: Point
) -> bool:
    if start == end:
        return check_wall_can_pass_through(race_track, start)
    else:
        return get_pair_distance(start, end) <= (CHEAT_MAX_TIME - 2) and (
            check_wall_is_facing_track(race_track, start)
            and check_wall_is_facing_track(race_track, end)
        )


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


def find_best_track_time(
    race_track: RaceTrack, start: Point | None = None, end: Point | None = None
) -> int:
    open = PriorityQueue()
    open.put(Node(0, start or race_track.start))
    visited = {}

    while not open.empty():
        current = open.get()

        if current.point == (end or race_track.end):
            return current.time
        elif visited.get(current.point, False):
            continue

        visited[current.point] = True

        if (
            not isinstance(race_track.tiles.get(current.point, Track()), Wall)
            or current.point == start
        ):
            for point in find_neighbour(race_track, current.point):
                open.put(Node(current.time + 1, point))

    raise Exception("There is no path")


def find_best_wall_time(race_track: RaceTrack, start: Point, end: Point) -> int:
    """
    NOTE: (time + 2) is the time needed to disable collision
    """
    open = PriorityQueue()
    open.put(Node(0, start))
    visited = {}

    while not open.empty():
        current = open.get()

        if current.point == end:
            return current.time
        elif visited.get(current.point, False):
            continue

        visited[current.point] = True

        if current.time >= (CHEAT_MAX_TIME - 2):
            continue
        elif isinstance(race_track.tiles.get(current.point, Track()), Wall):
            for point in find_neighbour(race_track, current.point):
                open.put(Node(current.time + 1, point))

    raise Exception("There is no path")


def find_time_saved(
    wall_pair: tuple[Point, Point], race_track: RaceTrack, best_time: int
) -> tuple[tuple[Point, Point], int] | None:
    start, end = wall_pair
    try:
        time = (
            find_best_wall_time(race_track, start, end)
            + find_best_track_time(race_track, race_track.start, start)
            + find_best_track_time(race_track, end, race_track.end)
        )
    except Exception:
        return None

    if time < best_time:
        return (wall_pair, best_time - time)

    return None


def get_pair_distance(start: Point, end: Point) -> int:
    return abs(start.x - end.x) + abs(start.y - end.y)


def find_time_cheated(
    race_track: RaceTrack, best_time: int
) -> tuple[tuple[Point, int], ...]:
    wall_pairs = tuple(
        (wall, wall)
        for wall in race_track.tiles.keys()
        if check_wall_can_pass_through(race_track, wall)
    )

    if len(wall_pairs) < 100:
        return tuple(
            (start, time_saved)
            for (start, _), time_saved in filter(
                None,
                (
                    find_time_saved(wall_pair, race_track, best_time)
                    for wall_pair in wall_pairs
                ),
            )
        )
    else:
        with ProcessPoolExecutor() as executor:
            return tuple(
                (start, time_saved)
                for (start, _), time_saved in filter(
                    None,
                    executor.map(
                        partial(
                            find_time_saved, race_track=race_track, best_time=best_time
                        ),
                        wall_pairs,
                        chunksize=100,
                    ),
                )
            )


def find_time_cheated_new_rule(
    race_track: RaceTrack, best_time: int
) -> tuple[tuple[tuple[Point, Point], int], ...]:
    wall_pairs = tuple(
        pair
        for pair in product(race_track.tiles.keys(), repeat=2)
        if check_wall_pair_is_accessible(race_track, *pair)
    )

    if len(wall_pairs) < 10000:
        return tuple(
            filter(
                None,
                (
                    find_time_saved(
                        wall_pair,  # type: ignore
                        race_track,
                        best_time,
                    )
                    for wall_pair in wall_pairs
                ),
            )
        )
    else:
        with ProcessPoolExecutor() as executor:
            return tuple(
                filter(
                    None,
                    executor.map(
                        partial(
                            find_time_saved, race_track=race_track, best_time=best_time
                        ),
                        wall_pairs,
                        chunksize=100,
                    ),
                )
            )


def part1(input: str) -> int:
    race_track = parse(input)

    return len(
        tuple(
            time_saved
            for _, time_saved in find_time_cheated(
                race_track, find_best_track_time(race_track)
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
                race_track, find_best_track_time(race_track)
            )
            if time_saved >= 100
        )
    )


def main() -> None:
    input = stdin.read()

    # print("PYTHON:", part1(input), part2(input))
    print("PYTHON:", part2(input))


if __name__ == "__main__":
    main()
