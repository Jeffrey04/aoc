from collections.abc import Generator
from dataclasses import dataclass, field
from functools import reduce
from queue import PriorityQueue
from sys import stdin

import structlog
from cytoolz.dicttoolz import merge

type Trail = dict[Point, int]

logger = structlog.get_logger()


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x},{self.y}"


@dataclass
class Corrupted:
    pass


@dataclass
class Safe:
    pass


@dataclass
class Memory:
    end: Point
    bytes: tuple[Point, ...]
    start: Point = Point(0, 0)


@dataclass
class Node:
    g: int
    h: int
    point: Point

    @property
    def f(self) -> int:
        return self.g + self.h


@dataclass(order=True)
class PNode:
    priority: int
    node: Node = field(compare=False)


def parse(input: str, end: Point) -> Memory:
    return Memory(
        end,
        tuple(
            Point(*[int(item) for item in line.split(",")])
            for idx, line in enumerate(input.strip().splitlines())
        ),
    )


def get_corrupted_map(
    memory: Memory, fallen_count: int
) -> dict[Point, Safe | Corrupted]:
    return {
        point: Corrupted()
        for idx, point in enumerate(memory.bytes)
        if idx < fallen_count
    }


def visualize(
    memory: Memory,
    corrupted_map: dict[Point, Safe | Corrupted],
    trail: Trail | None = None,
) -> str:
    return "\n".join(
        "".join(
            visualize_byte(Point(x, y), trail, corrupted_map)
            for x in range(memory.end.x + 1)
        )
        for y in range(memory.end.y + 1)
    )


def visualize_byte(
    point: Point,
    trail: Trail | None,
    corrupted_map: dict[Point, Safe | Corrupted],
) -> str:
    byte = corrupted_map.get(point, Safe())
    if trail and trail.get(point, 0) != 0:
        return "O"
    elif isinstance(byte, Safe):
        return "."
    elif isinstance(byte, Corrupted):
        return "#"
    else:
        raise Exception("undefined")


def find_neighbours(memory: Memory, point: Point) -> Generator[Point, None, None]:
    return (
        point
        for point in (
            Point(point.x, point.y - 1),
            Point(point.x, point.y + 1),
            Point(point.x - 1, point.y),
            Point(point.x + 1, point.y),
        )
        if 0 <= point.x <= memory.end.x and 0 <= point.y <= memory.end.y
    )


def distance_to_end(memory: Memory, point: Point) -> int:
    return abs(memory.end.x - point.x) + abs(memory.end.y - point.y)


def find_route(
    memory: Memory, corrupted_map: dict[Point, Safe | Corrupted]
) -> tuple[int, Trail]:
    open = PriorityQueue()
    start = Node(0, distance_to_end(memory, memory.start), memory.start)
    open.put(PNode(start.f, start))
    visited: dict[Point, bool] = {}
    trail: dict[Point, Trail] = {memory.start: {memory.start: 1}}

    while not open.empty():
        current = open.get().node

        if current.point == memory.end:
            return current.g, trail[current.point]
        elif current.point in visited:
            continue

        visited[current.point] = True

        if not isinstance(corrupted_map.get(current.point, Safe()), Corrupted):
            for neighbour in find_neighbours(memory, current.point):
                trail[neighbour] = merge(trail[current.point], {neighbour: 1})

                incoming = Node(
                    current.g + 1, distance_to_end(memory, neighbour), neighbour
                )
                open.put(PNode(incoming.f, incoming))

    raise Exception("path is not found")


def part1(input: str, end: Point, fallen_count: int) -> int:
    memory = parse(input, end)
    return find_route(memory, get_corrupted_map(memory, fallen_count))[0]


def part2(input: str, end: Point) -> str:
    memory = parse(input, end)
    _, trail = find_route(memory, get_corrupted_map(memory, 0))

    for idx, point in enumerate(memory.bytes):
        if point in trail:
            try:
                _, trail = find_route(memory, get_corrupted_map(memory, idx + 1))
            except Exception:
                return str(point)


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input, Point(70, 70), 1024), part2(input, Point(70, 70)))


if __name__ == "__main__":
    main()
