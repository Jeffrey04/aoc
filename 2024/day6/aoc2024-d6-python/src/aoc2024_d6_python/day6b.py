from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from sys import stdin


class Rotation:
    c0r0: int
    c1r0: int
    c0r1: int
    c1r1: int


@dataclass(frozen=True)
class RotateRight(Rotation):
    c0r0: int = 0
    c1r0: int = 1
    c0r1: int = -1
    c1r1: int = 0


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, direction: Direction) -> Point:
        return Point(self.x + direction.x, self.y + direction.y)


@dataclass
class Direction:
    x: int
    y: int

    def __mul__(self, rotation: Rotation) -> Direction:
        return Direction(
            self.x * rotation.c0r0 + self.y * rotation.c0r1,
            self.x * rotation.c1r0 + self.y * rotation.c1r1,
        )


class Symbol(Enum):
    Guard = "^"
    Obstruction = "#"


@dataclass
class Space:
    pass


@dataclass
class Guard:
    pass


@dataclass
class Obstruction:
    pass


DIRECTION_DEFAULT = Direction(0, -1)
ROTATION_DEFAULT = RotateRight()


@dataclass
class Board:
    tiles: dict[Point, Space | Guard | Obstruction]
    width: int
    height: int


def check_is_in_board(board: Board, point: Point) -> bool:
    return not (
        point.x < 0 or point.y < 0 or point.x >= board.width or point.y >= board.height
    )


def check_is_passable(board: Board, point: Point) -> bool:
    return not isinstance(board.tiles.get(point, Space()), Obstruction)


def check_is_passable_with_new_object(
    board: Board, new_obstacle: Point, point: Point
) -> bool:
    return check_is_passable(board, point) and point != new_obstacle


def guard_rotate(direction: Direction, rotation: Rotation) -> Direction:
    return direction * rotation


def guard_move(
    board: Board, guard: Point, direction: Direction, rotation: Rotation
) -> tuple[Direction, Point]:
    result = ()
    destination = guard + direction

    match check_is_passable(board, destination):
        case True:
            result = direction, destination

        case False:
            result = guard_rotate(direction, rotation), guard

    return result


def guard_move_with_new_obstacle(
    board: Board,
    new_obstacle: Point,
    guard: Point,
    direction: Direction,
    rotation: Rotation,
) -> tuple[Direction, Point]:
    result = ()
    destination = guard + direction

    match check_is_passable_with_new_object(board, new_obstacle, destination):
        case True:
            result = direction, destination

        case False:
            result = guard_rotate(direction, rotation), guard

    return result


def finder(board: tuple[str, ...], symbol: Symbol) -> Generator[Point, None, None]:
    return (
        Point(x, y)
        for y, row in enumerate(board)
        for x, item in enumerate(tuple(row))
        if item == symbol.value
    )


def parse(input: str) -> tuple[Board, Point]:
    board = tuple(input.strip().splitlines())

    return (
        Board(
            {point: Obstruction() for point in finder(board, Symbol.Obstruction)},
            len(board[0]),
            len(board),
        ),
        next(finder(board, Symbol.Guard)),
    )


def get_visited_tiles(
    board: Board,
    guard: Point,
    rotation: Rotation,
    direction: Direction = DIRECTION_DEFAULT,
) -> dict[Point, bool]:
    tiles = {guard: True}

    while check_is_in_board(board, guard):
        direction, guard = guard_move(board, guard, direction, rotation)

        tiles[guard] = True

    # last tile is outside of the board
    del tiles[guard]

    return tiles


def part1(input: str) -> int:
    return len(get_visited_tiles(*parse(input), rotation=RotateRight()))


def part2(input: str) -> int:
    board, guard = parse(input)

    tiles = get_visited_tiles(board, guard, rotation=RotateRight())
    del tiles[guard]

    return len(
        tuple(
            filter(
                None,
                (
                    check_is_loopable(tile, board, guard, RotateRight())
                    for tile in tiles
                ),
            )
        )
    )


def check_is_loopable(
    new_obstacle: Point,
    board: Board,
    guard: Point,
    rotation: Rotation,
    direction=DIRECTION_DEFAULT,
) -> bool:
    result = False

    steps = dict()

    while check_is_in_board(board, guard):
        direction, guard_new = guard_move_with_new_obstacle(
            board,
            new_obstacle,
            guard,
            direction,
            rotation,
        )

        step = (guard, guard_new)
        guard = guard_new

        if step[0] == step[1]:
            continue
        elif steps.get(step, False):
            # condition 2: if current step was attempted, it is a loop
            result = True
            break

        steps[step] = True

    return result


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
