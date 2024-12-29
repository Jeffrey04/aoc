from collections import Counter
from collections.abc import Generator
from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
from sys import stdin

import structlog
from cytoolz.dicttoolz import merge

logger = structlog.get_logger()


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
    cheat_wall: Point | None = field(compare=False, default=None)
    trail: dict[Point, bool] = field(compare=False, default=lambda: {})  # type: ignore


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


def find_neighbours_safe(
    race_track: RaceTrack, point: Point
) -> Generator[tuple[int, Point], None, None]:
    return (
        (1, neighbour)
        for neighbour in (
            Point(point.x + 1, point.y),
            Point(point.x - 1, point.y),
            Point(point.x, point.y + 1),
            Point(point.x, point.y - 1),
        )
        if check_point_is_in_track(race_track, neighbour)
    )


def find_neighbours_cheat(
    race_track: RaceTrack, point: Point
) -> Generator[tuple[int, Point, Point], None, None]:
    return (
        (2, mid, neighbour)
        for mid, neighbour in (
            (Point(point.x + 1, point.y), Point(point.x + 2, point.y)),
            (Point(point.x - 1, point.y), Point(point.x - 2, point.y)),
            (Point(point.x, point.y + 1), Point(point.x, point.y + 2)),
            (Point(point.x, point.y - 1), Point(point.x, point.y - 2)),
        )
        if check_point_is_in_track(race_track, neighbour)
        and isinstance(race_track.tiles.get(mid, Track()), Wall)
    )


def find_time_shortest(race_track: RaceTrack, end_point: Point) -> int:
    open = PriorityQueue()
    open.put(Node(0, race_track.start))
    visited = {}

    while not open.empty():
        current = open.get()

        if current.point == race_track.end:
            return current.time
        elif visited.get(current.point, False):
            continue

        visited[current.point] = True

        if not isinstance(race_track.tiles.get(current.point, Track()), Wall):
            for time, point in find_neighbours_safe(race_track, current.point):
                open.put(Node(current.time + time, point))

    raise Exception("There is no path")


def find_time_cheated(race_track: RaceTrack, best_time: int) -> dict[Point, int]:
    open = PriorityQueue()
    open.put(Node(0, race_track.start, None, {race_track.start: True}))
    result = {}
    visited = {}
    debug_count = 1

    while not open.empty():
        current = open.get()
        debug_count -= 1
        # logger.info("progress", result=sum(result.values()), candidates=debug_count)

        if visited.get((current.point, current.cheat_wall), False):
            continue

        visited[(current.point, current.cheat_wall)] = True

        if current.cheat_wall is not None and current.point == race_track.end:
            result[current.cheat_wall] = best_time - current.time
            continue

        if not isinstance(race_track.tiles.get(current.point, Track()), Wall):
            for time, point in find_neighbours_safe(race_track, current.point):
                debug_count += 1
                open.put(
                    Node(
                        current.time + time,
                        point,
                        current.cheat_wall,
                        merge(current.trail, {point: True}),
                    )
                )

            if current.cheat_wall is None:
                for time, wall, point in find_neighbours_cheat(
                    race_track, current.point
                ):
                    debug_count += 1
                    open.put(
                        Node(
                            current.time + time,
                            point,
                            wall,
                            merge(current.trail, {wall: True, point: True}),
                        )
                    )

    return result


def part1(input: str) -> Counter[int]:
    race_track = parse(input)

    return Counter(
        value
        for value in find_time_cheated(
            race_track, find_time_shortest(race_track)
        ).values()
        if value >= 100
    )


def visualize(race_track: RaceTrack, wall: Point, trail) -> str:
    return "\n".join(
        "".join(
            visualize_tile(race_track, Point(x, y), wall, trail)
            # fmt: skip
            for x in range(race_track.width)
        )
        for y in range(race_track.height)
    )


def visualize_tile(race_track: RaceTrack, point: Point, wall: Point, trail) -> str:
    if point == wall:
        return "@"
    elif point in trail:
        return "%"
    else:
        match race_track.tiles.get(point, Track()):
            case Wall():
                return "#"

            case Track():
                return "."

            case _:
                raise Exception("Undefined behavior")


def main():
    input = stdin.read()

    print("PYTHON:", part1(input))


if __name__ == "__main__":
    main()
