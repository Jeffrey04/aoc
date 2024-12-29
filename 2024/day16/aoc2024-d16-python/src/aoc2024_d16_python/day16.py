from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
from sys import stdin

from cytoolz.dicttoolz import merge

type Trail = dict[Point, int]

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


@dataclass(order=True)
class Node2:
    cost: int
    direction: Direction = field(compare=False)
    point: Point = field(compare=False)


@dataclass(order=True)
class PNode:
    priority: int
    node: Node | Node2 = field(compare=False)


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


def distance_to_end(maze: Maze, point: Point) -> int:
    # manhattan distance
    return abs(maze.end.x - point.x) + abs(maze.end.y - point.y)
    # euclidean distance
    # return (maze.end.x - point.x) ** 2 + (maze.end.y - point.y) ** 2


def find_astar(
    maze: Maze, reindeer: Point, direction_default: Direction = DIRECTION_START
) -> tuple[int, Trail]:
    start = Node(
        direction_default, reindeer, 0, distance_to_end(maze, reindeer), {reindeer: 1}
    )
    open = PriorityQueue()
    open.put(PNode(start.f, start))
    closed: dict[tuple[Direction, Point], Node] = {}

    while not open.empty():
        current = open.get().node

        if current.point == maze.end:
            return current.g, current.trail
        elif (current.direction, current.point) in closed:
            continue

        closed[(current.direction, current.point)] = current

        if not isinstance(maze.tiles.get(current.point, Space()), Wall):
            nodes = (
                Node(
                    current.direction,
                    current.point + current.direction,
                    current.g + COST_FORWARD,
                    distance_to_end(maze, current.point + current.direction),
                    merge(current.trail, {(current.point + current.direction): 1}),
                ),
                Node(
                    current.direction * RotateLeft(),
                    current.point,
                    current.g + COST_ROTATE,
                    current.h,
                    current.trail,
                ),
                Node(
                    current.direction * RotateRight(),
                    current.point,
                    current.g + COST_ROTATE,
                    current.h,
                    current.trail,
                ),
            )
            for node in nodes:
                open.put(PNode(node.f, node))

    raise Exception("Route is not found")


def find_djikstra(
    maze: Maze, reindeer: Point, direction_default: Direction = DIRECTION_START
) -> tuple[int, list[Trail]]:
    open = PriorityQueue()
    open.put(Node2(0, direction_default, reindeer))
    closed: dict[tuple[Direction, Point], Node] = {}
    trails: dict[tuple[Direction, Point, int], list[Trail]] = {
        (direction_default, reindeer, 0): [{reindeer: 1}],
    }

    while not open.empty():
        current = open.get()

        if current.point == maze.end:
            return current.cost, trails[
                (current.direction, current.point, current.cost)
            ]
        elif (current.direction, current.point) in closed:
            continue

        closed[(current.direction, current.point)] = current

        if not isinstance(maze.tiles.get(current.point, Space()), Wall):
            nodes = (
                Node2(
                    current.cost + COST_FORWARD,
                    current.direction,
                    current.point + current.direction,
                ),
                Node2(
                    current.cost + COST_ROTATE,
                    current.direction * RotateLeft(),
                    current.point,
                ),
                Node2(
                    current.cost + COST_ROTATE,
                    current.direction * RotateRight(),
                    current.point,
                ),
            )
            for node in nodes:
                trails[(node.direction, node.point, node.cost)] = trails.get(
                    (node.direction, node.point, node.cost), []
                )
                trails[(node.direction, node.point, node.cost)].extend(
                    trails[(current.direction, current.point, current.cost)]
                    if current.direction != node.direction
                    else (
                        merge(trail, {node.point: 1})
                        for trail in trails.get(
                            (current.direction, current.point, current.cost), []
                        )
                    )
                )
                open.put(node)

    raise Exception("Route is not found")


def part1(input: str) -> int:
    return find_astar(*parse(input))[0]


def part2(input: str) -> int:
    return len(
        set(
            item
            for trail in find_djikstra(*parse(input))[-1]
            for item in trail.keys()
            if isinstance(item, Point)
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
