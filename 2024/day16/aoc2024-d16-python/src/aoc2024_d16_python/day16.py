from __future__ import annotations

from collections.abc import Generator
from ctypes.wintypes import POINT
from dataclasses import dataclass
from enum import Enum
from sys import stdin

import structlog
from cytoolz.dicttoolz import dissoc, merge, merge_with

logger = structlog.get_logger()

type Trail = dict[Point | Rotation, int]


@dataclass(frozen=True)
class Direction:
    x: int
    y: int

    def __mul__(self, rotation: Rotation) -> Direction:
        return Direction(
            self.x * rotation.c0r0 + self.y * rotation.c1r0,
            self.x * rotation.c1r0 + self.y * rotation.c1r1,
        )


class Rotation:
    c0r0: int
    c1r0: int
    c0r1: int
    c1r1: int


@dataclass(frozen=True)
class RotateLeft(Rotation):
    c0r0: int = 0
    c1r0: int = -1
    c0r1: int = 1
    c1r1: int = 0


@dataclass(frozen=True)
class RotateRight(Rotation):
    c0r0: int = 0
    c1r0: int = 1
    c0r1: int = -1
    c1r1: int = 0


class Symbol(Enum):
    Start = "S"
    End = "E"
    Wall = "#"
    Space = "."
    Step = "@"


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, direction: Direction) -> Point:
        return Point(self.x + direction.x, self.y + direction.y)


@dataclass
class Wall:
    pass


@dataclass
class Space:
    pass


@dataclass
class Maze:
    start: Point
    end: Point
    tiles: dict[Point, Wall | Space]
    width: int
    height: int


DIRECTION_START = Direction(1, 0)


def parse(input: str) -> tuple[Maze, Point]:
    maze = tuple(input.strip().splitlines())
    start = next(search(maze, Symbol.Start))

    return Maze(
        start,
        next(search(maze, Symbol.End)),
        {point: Wall() for point in search(maze, Symbol.Wall)},
        len(maze[0]),
        len(maze),
    ), start


def search(input: tuple[str, ...], symbol: Symbol) -> Generator[Point, None, None]:
    return (
        Point(x, y)
        for y, row in enumerate(input)
        for x, item in enumerate(row)
        if item == symbol.value
    )


def check_is_not_hitting_wall(maze: Maze, point: Point) -> bool:
    return not isinstance(maze.tiles.get(point, Space()), Wall)


def check_can_progress(maze: Maze, trail: Trail, point: Point) -> bool:
    return check_is_not_hitting_wall(maze, point) and point not in trail


def rotate(direction: Direction, rotation: Rotation) -> Direction:
    return direction * rotation


def find_path(
    maze: Maze, reindeer: Point, direction_default: Direction = DIRECTION_START
) -> Generator[Trail, None, None]:
    candidates: list[tuple[Trail, Point, Direction]] = [
        (
            {reindeer: 1},
            reindeer,
            direction_default,
        )
    ]

    while True:
        try:
            trail_current, point_current, direction_current = candidates.pop(0)
        except IndexError:
            break

        if point_current == maze.end:
            yield trail_current

        point_incoming = point_current + direction_current

        if check_can_progress(maze, trail_current, point_incoming):
            candidates.insert(
                0,
                (
                    merge(trail_current, {point_incoming: 1}),
                    point_incoming,
                    direction_current,
                ),
            )

        for rotation in (RotateLeft(), RotateRight()):
            direction_rotated = rotate(direction_current, rotation)
            point_incoming = point_current + direction_rotated

            if check_can_progress(maze, trail_current, point_incoming):
                candidates.append(
                    (
                        merge_with(
                            sum, trail_current, {rotation: 1, point_incoming: 1}
                        ),
                        point_incoming,
                        direction_rotated,
                    )
                )


def score(trail: Trail) -> int:
    return sum(
        count * (1000 if isinstance(item, Rotation) else 1)
        for item, count in trail.items()
    )


def part1(input: str) -> int:
    maze, reindeer = parse(input)

    return next(score(dissoc(trail, reindeer)) for trail in find_path(maze, reindeer))


def visualize(maze: Maze, trail: Trail) -> str:
    return "\n".join(
        "".join(
            visualize_tile(maze, Point(x, y), trail)
            # fmt: skip
            for x in range(maze.width)
        )
        for y in range(maze.height)
    )


def visualize_tile(maze: Maze, point: Point, trail: Trail) -> str:
    if point == maze.start:
        return f"[green]{Symbol.Start.value}[/green]"
    elif point == maze.end:
        return f"[red]{Symbol.End.value}[/red]"
    elif point in trail:
        return f"[yellow]{Symbol.Step.value}[/yellow]"
    else:
        match maze.tiles.get(point, Space()):
            case Wall():
                return f"[blue]{Symbol.Wall.value}[/blue]"

            case Space():
                return f"[white]{Symbol.Space.value}[/white]"

            case _:
                raise Exception("Undefined behavior")


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input))


if __name__ == "__main__":
    main()
