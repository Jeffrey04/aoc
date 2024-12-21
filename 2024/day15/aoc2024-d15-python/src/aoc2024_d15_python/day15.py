from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from sys import stdin
from typing import Any, Generator, Literal

from cytoolz.dicttoolz import dissoc, merge


class Symbol(Enum):
    Robot = "@"
    Wall = "#"
    Box = "O"
    Up = "^"
    Down = "v"
    Left = "<"
    Right = ">"
    Space = "."
    LBox = "["
    RBox = "]"


type Move = Literal[Symbol.Up, Symbol.Down, Symbol.Left, Symbol.Right]
type Tile_Chain_X = tuple[tuple[Point, Wall | Box | LBox | RBox | Space], ...]
type Tile_Chain_Y = tuple[Tile_Chain_X, ...]


@dataclass(frozen=True)
class Box:
    symbol: Symbol = Symbol.Box


@dataclass(frozen=True)
class LBox:
    symbol: Symbol = Symbol.LBox


@dataclass(frozen=True)
class RBox:
    symbol: Symbol = Symbol.RBox


@dataclass(frozen=True)
class Wall:
    symbol: Symbol = Symbol.Wall


@dataclass(frozen=True)
class Space:
    symbol = Symbol.Space


@dataclass
class Vector:
    x: int
    y: int


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, vector: Vector) -> Point:
        assert isinstance(vector, Vector)
        return Point(self.x + vector.x, self.y + vector.y)


@dataclass
class Robot:
    x: int
    y: int
    symbol: Symbol = Symbol.Robot


@dataclass
class Board:
    robot: Robot
    tiles: dict[Point, Box | Wall | Space]
    width: int
    height: int


def check_is_move(move: str) -> bool:
    return move in (
        Symbol.Up.value,
        Symbol.Down.value,
        Symbol.Left.value,
        Symbol.Right.value,
    )


def double_board(input: str) -> str:
    match input:
        case Symbol.Robot.value:
            return f"{Symbol.Robot.value}{Symbol.Space.value}"
        case Symbol.Box.value:
            return f"{Symbol.LBox.value}{Symbol.RBox.value}"
        case char:
            return char * 2


def parse(
    input: str, decorator: Callable[[str], str] | None = None
) -> tuple[Board, tuple[Move, ...]]:
    def reducer(
        current: tuple[tuple[str, ...], str], incoming: str
    ) -> tuple[tuple[str, ...], str]:
        board, move = current

        if incoming and check_is_move(incoming[0]):
            return board, move + incoming
        elif incoming:
            return board + (
                "".join(map(decorator, incoming)) if decorator else incoming,
            ), move
        else:
            return current

    board, move = reduce(reducer, input.strip().splitlines(), ((), ""))

    return parse_board(board), tuple(parse_move(i) for i in move)


def parse_move(move: str) -> Move:
    assert check_is_move(move)

    match move:
        case Symbol.Up.value:
            return Symbol.Up

        case Symbol.Down.value:
            return Symbol.Down

        case Symbol.Left.value:
            return Symbol.Left

        case _:
            return Symbol.Right


def parse_board(board: tuple[str, ...]) -> Board:
    robot = next(search(board, Symbol.Robot))
    return Board(
        Robot(robot.x, robot.y),
        merge(
            {point: Wall() for point in search(board, Symbol.Wall)},
            {point: Box() for point in search(board, Symbol.Box)},
            {point: LBox() for point in search(board, Symbol.LBox)},
            {point: RBox() for point in search(board, Symbol.RBox)},
        ),
        len(board[0]),
        len(board),
    )


def search(board: tuple[str, ...], symbol: Symbol) -> Generator[Point, None, None]:
    return (
        Point(x, y)
        for y, row in enumerate(board)
        for x, item in enumerate(row)
        if item == symbol.value
    )


def move_to_vector(move: Move) -> Vector:
    match move:
        case Symbol.Up:
            return Vector(0, -1)

        case Symbol.Down:
            return Vector(0, 1)

        case Symbol.Left:
            return Vector(-1, 0)

        case Symbol.Right:
            return Vector(1, 0)


def robot_push(board: Board, vector: Vector) -> Board:
    tile_chain = get_tile_chain(board, vector)

    if not check_can_push(tile_chain):
        return board

    if isinstance(tile_chain[0][0], Point):
        return robot_push_x(tile_chain, board, vector)  # type: ignore
    else:
        return robot_push_y(tile_chain, board, vector)  # type: ignore


def robot_push_x(tile_chain: Tile_Chain_X, board: Board, vector: Vector) -> Board:
    robot_new = tile_chain[0][0]

    return Board(
        Robot(robot_new.x, robot_new.y),
        dissoc(
            merge(
                board.tiles,
                {
                    position + vector: tile
                    # everything in the chain moves except the last one
                    for position, tile in tile_chain[:-1]
                },
            ),
            robot_new,
        ),
        board.width,
        board.height,
    )


def robot_push_y(tile_chain: Tile_Chain_Y, board: Board, vector: Vector) -> Board:
    return Board(
        Robot(board.robot.x + vector.x, board.robot.y + vector.y),
        merge(
            dissoc(board.tiles, *(point for row in tile_chain for point, _ in row)),
            {
                position + vector: tile
                for row in tile_chain[:-1]
                for position, tile in row
            },
        ),
        board.width,
        board.height,
    )


def robot_instruct(board: Board, moves: tuple[Move, ...]) -> Board:
    return reduce(robot_push, map(move_to_vector, moves), board)


def get_tile_chain(board: Board, vector: Vector) -> Tile_Chain_X | Tile_Chain_Y:
    if vector.y == 0:
        return get_tile_chain_x(board, vector)
    else:
        return get_tile_chain_y(board, vector)


def get_tile_chain_x(board: Board, vector: Vector) -> Tile_Chain_X:
    result, current = (), Point(board.robot.x, board.robot.y)

    while True:
        current += vector
        tile = board.tiles.get(current, Space())

        result += ((current, tile),)

        match tile:
            case Wall() | Space():
                break

            case Box():
                continue

    return result


def get_tile_chain_y(board: Board, vector: Vector) -> Tile_Chain_Y:
    def reducer(
        current: set[tuple[Point, Any]], incoming: Point
    ) -> set[tuple[Point, Any]]:
        point_new = incoming + vector
        tile = board.tiles.get(point_new, Space())

        current.add((point_new, tile))

        match tile:
            case LBox():
                point_right = Point(point_new.x + 1, point_new.y)
                assert isinstance(board.tiles[point_right], RBox)
                current.add((point_right, board.tiles[point_right]))

            case RBox():
                point_left = Point(point_new.x - 1, point_new.y)
                assert isinstance(board.tiles[point_left], LBox)
                current.add((point_left, board.tiles[point_left]))

        return current

    result, current = (), (Point(board.robot.x, board.robot.y),)

    while True:
        row = tuple(reduce(reducer, current, set()))

        current = (point for point, tile in row if not isinstance(tile, Space))

        if check_tile_chain_y_break_condition(row):
            result += (row,)
            break
        else:
            result += (
                tuple(
                    (point, tile) for point, tile in row if not isinstance(tile, Space)
                ),
            )

    return result


def check_is_row_of_space(tile_chain: Tile_Chain_X) -> bool:
    return all(isinstance(item, Space) for _, item in tile_chain)


def check_row_has_wall(tile_chain: Tile_Chain_X) -> bool:
    return any(isinstance(item, Wall) for _, item in tile_chain)


def check_tile_chain_y_break_condition(tile_chain: Tile_Chain_X) -> bool:
    return check_is_row_of_space(tile_chain) or check_row_has_wall(tile_chain)


def check_can_push(tile_chain: Tile_Chain_X | Tile_Chain_Y) -> bool:
    if isinstance(tile_chain[0][0], Point):
        return check_can_push_x(tile_chain)  # type: ignore
    else:
        return check_can_push_y(tile_chain)  # type: ignore


def check_can_push_x(tile_chain: Tile_Chain_X) -> bool:
    _, last_tile = tile_chain[-1]

    match last_tile:
        case Wall():
            return False

        case Space():
            return True

        case _:
            raise Exception("Undefined behavior")


def check_can_push_y(tile_chain: Tile_Chain_Y) -> bool:
    if check_is_row_of_space(tile_chain[-1]):
        return True
    elif check_row_has_wall(tile_chain[-1]):
        return False
    else:
        raise Exception("Undefined behavior")


def visualize(board: Board) -> str:
    return "\n".join(
        "".join(
            visualize_get_symbol(board, Point(x, y)).value for x in range(board.width)
        )
        for y in range(board.height)
    )


def visualize_get_symbol(board: Board, position: Point) -> Symbol:
    if board.robot.x == position.x and board.robot.y == position.y:
        return Symbol.Robot
    else:
        return board.tiles.get(position, Space()).symbol


def get_coordinate(point: Point) -> int:
    return point.y * 100 + point.x


def part1(input: str) -> int:
    return sum(
        get_coordinate(point)
        for point, tile in robot_instruct(*parse(input)).tiles.items()
        if isinstance(tile, Box)
    )


def part2(input: str) -> int:
    return sum(
        get_coordinate(point)
        for point, tile in robot_instruct(*parse(input, double_board)).tiles.items()
        if isinstance(tile, LBox)
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
