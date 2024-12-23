from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from math import inf
from operator import attrgetter
from sys import stdin

from cytoolz.dicttoolz import merge, merge_with

type Trail = dict[Point | Rotation, int]

COST_FORWARD = 1
COST_ROTATE = 1000


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


@dataclass
class Node:
    direction: Direction
    point: Point
    g: int
    h: int
    trail: Trail

    @property
    def f(self) -> int:
        return self.g + self.h


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


def check_can_progress(
    maze: Maze,
    visited: dict[tuple[Direction, Point], int],
    unvisited: dict[tuple[Direction, Point], int],
    direction: Direction,
    point: Point,
    cost: int,
) -> bool:
    return (
        check_is_not_hitting_wall(maze, point)
        and (direction, point) not in visited
        and unvisited.get((direction, point), inf) >= cost
    )


def distance_to_end(maze: Maze, point: Point) -> int:
    # manhattan distance
    return abs(maze.end.x - point.x) + abs(maze.end.y - point.y)
    # euclidean distance
    # return (maze.end.x - point.x) ** 2 + (maze.end.y - point.y) ** 2


def find_astar(
    maze: Maze, reindeer: Point, direction_default: Direction = DIRECTION_START
) -> Generator[tuple[int, Trail], None, None]:
    # https://www.datacamp.com/tutorial/a-star-algorithm
    open_list: dict[tuple[Direction, Point], Node] = {
        (direction_default, reindeer): Node(
            direction_default,
            reindeer,
            0,
            distance_to_end(maze, reindeer),
            {reindeer: 1},
        )
    }
    closed_list: dict[tuple[Direction, Point], Node] = {}

    while True:
        try:
            current = next(
                node
                for _, node in open_list.items()
                if node.f == min(map(attrgetter("f"), open_list.values()))
            )
        except StopIteration:
            break

        if current.point == maze.end:
            yield current.g, current.trail

        del open_list[(current.direction, current.point)]
        closed_list[(current.direction, current.point)] = current

        # case forward
        point_incoming = current.point + current.direction
        cost_incoming = current.g + COST_FORWARD

        if (
            check_is_not_hitting_wall(maze, point_incoming)
            and (current.direction, point_incoming) not in closed_list
            and (
                (current.direction, point_incoming) not in open_list
                or cost_incoming < open_list[(current.direction, point_incoming)].g
            )
        ):
            open_list[(current.direction, point_incoming)] = Node(
                current.direction,
                point_incoming,
                cost_incoming,
                distance_to_end(maze, point_incoming),
                merge(current.trail, {point_incoming: 1}),
            )

        # case rotate
        for rotation in (RotateLeft(), RotateRight()):
            direction_rotated = current.direction * rotation
            point_incoming = current.point + direction_rotated
            cost_incoming = current.g + COST_FORWARD + COST_ROTATE

            if (
                check_is_not_hitting_wall(maze, point_incoming)
                and (direction_rotated, point_incoming) not in closed_list
                and (
                    (direction_rotated, point_incoming) not in open_list
                    or cost_incoming < open_list[(direction_rotated, point_incoming)].g
                )
            ):
                open_list[(direction_rotated, point_incoming)] = Node(
                    direction_rotated,
                    point_incoming,
                    cost_incoming,
                    distance_to_end(maze, point_incoming),
                    merge_with(sum, current.trail, {rotation: 1, point_incoming: 1}),
                )


def find_djikstra(
    maze: Maze, reindeer: Point, direction_default: Direction = DIRECTION_START
) -> Generator[tuple[int, list[Trail]], None, None]:
    # https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
    unvisited: dict[tuple[Direction, Point], int] = {(direction_default, reindeer): 0}
    visited: dict[tuple[Direction, Point], int] = {}
    point_trail: dict[tuple[Point, int], list[Trail]] = {(reindeer, 0): [{reindeer: 1}]}

    while True:
        try:
            direction_current, point_current, cost_current = next(
                (direction, point, value)
                for (direction, point), value in unvisited.items()
                if value == min(unvisited.values())
            )
        except StopIteration:
            break

        if point_current == maze.end:
            yield (
                unvisited[(direction_current, point_current)],
                point_trail[(point_current, cost_current)],
            )

        point_incoming = point_current + direction_current
        cost_incoming = cost_current + COST_FORWARD

        # update forward
        if check_can_progress(
            maze, visited, unvisited, direction_current, point_incoming, cost_incoming
        ):
            unvisited[(direction_current, point_incoming)] = cost_incoming

            point_trail[(point_incoming, cost_incoming)] = point_trail.get(
                (point_incoming, cost_incoming), []
            )
            point_trail[(point_incoming, cost_incoming)].extend(
                [
                    merge(trail, {point_incoming: 1})
                    for trail in point_trail.get((point_current, cost_current), [])
                ]
            )

        # update rotate
        for rotation in (RotateLeft(), RotateRight()):
            direction_rotated = direction_current * rotation
            point_incoming = point_current + direction_rotated
            cost_incoming = cost_current + COST_FORWARD + COST_ROTATE

            if check_can_progress(
                maze,
                visited,
                unvisited,
                direction_rotated,
                point_incoming,
                cost_incoming,
            ):
                unvisited[(direction_rotated, point_incoming)] = cost_incoming

                point_trail[(point_incoming, cost_incoming)] = point_trail.get(
                    (point_incoming, cost_incoming), []
                )
                point_trail[(point_incoming, cost_incoming)].extend(
                    [
                        merge_with(
                            sum,
                            trail,
                            {point_incoming: 1, rotation: 1},
                        )
                        for trail in point_trail.get((point_current, cost_current), [])
                    ]
                )

        visited[(direction_current, point_current)] = cost_current
        del unvisited[(direction_current, point_current)]


def part1(input: str) -> int:
    return next(find_astar(*parse(input)))[0]


def part2(input: str) -> int:
    results = tuple(find_djikstra(*parse(input)))

    return len(
        set(
            item
            for cost, trails in results
            for trail in trails
            for item in trail.keys()
            if (cost == min(score for score, _ in results)) and isinstance(item, Point)
        )
    )

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

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
