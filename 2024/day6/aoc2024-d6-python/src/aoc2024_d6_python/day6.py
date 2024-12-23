from collections.abc import Generator
from sys import stdin

DIRECTION_DEFAULT = (0, -1)
SYMBOL_GUARD = "^"
SYMBOL_OBSTRUCTION = "#"

ROTATE_RIGHT = {
    (0, 0): 0,
    (0, 1): -1,
    (1, 0): 1,
    (1, 1): 0,
}


def check_is_in_board(dimension: tuple[int, int], x: int, y: int) -> bool:
    return not (x < 0 or y < 0 or x >= dimension[0] or y >= dimension[1])


def check_is_passable(
    obstructions: dict[tuple[int, int], bool], x: int, y: int
) -> bool:
    return obstructions.get((x, y), False) is False


def check_is_passable_with_new_object(
    obstructions: dict[tuple[int, int], bool],
    new_obstacle: tuple[int, int],
    x: int,
    y: int,
) -> bool:
    return check_is_passable(obstructions, x, y) and (x, y) != new_obstacle


def guard_forward(
    guard: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    return (
        guard[0] + direction[0],
        guard[1] + direction[1],
    )


def guard_rotate(
    direction: tuple[int, int], rotation: dict[tuple[int, int], int]
) -> tuple[int, int]:
    return (
        direction[0] * ROTATE_RIGHT[(0, 0)] + direction[1] * ROTATE_RIGHT[(0, 1)],
        direction[0] * ROTATE_RIGHT[(1, 0)] + direction[1] * ROTATE_RIGHT[(1, 1)],
    )


def guard_move(
    obstructions: dict[tuple[int, int], bool],
    guard: tuple[int, int],
    direction: tuple[int, int],
    rotation: dict[tuple[int, int], int],
) -> tuple[tuple[int, int], tuple[int, int]]:
    result = ()
    destination = guard_forward(guard, direction)

    match check_is_passable(obstructions, *destination):
        case True:
            result = direction, destination

        case False:
            result = guard_rotate(direction, rotation), guard

    return result


def guard_move_with_new_obstacle(
    obstructions: dict[tuple[int, int], bool],
    new_obstacle: tuple[int, int],
    guard: tuple[int, int],
    direction: tuple[int, int],
    rotation: dict[tuple[int, int], int],
) -> tuple[tuple[int, int], tuple[int, int]]:
    result = ()
    destination = guard_forward(guard, direction)

    match check_is_passable_with_new_object(obstructions, new_obstacle, *destination):
        case True:
            result = direction, destination

        case False:
            result = guard_rotate(direction, rotation), guard

    return result


def finder(
    board: tuple[str, ...], symbol: str
) -> Generator[tuple[int, int], None, None]:
    return (
        (x, y)
        for y, row in enumerate(board)
        for x, item in enumerate(tuple(row))
        if item == symbol
    )


def parse(
    input: str,
) -> tuple[
    dict[tuple[int, int], bool],
    tuple[int, int],
    tuple[int, int],
]:
    board = tuple(input.strip().splitlines())

    return (
        {point: True for point in finder(board, SYMBOL_OBSTRUCTION)},
        next(finder(board, SYMBOL_GUARD)),
        (len(board[0]), len(board)),
    )


def get_visited_tiles(
    obstructions: dict[tuple[int, int], bool],
    guard: tuple[int, int],
    dimension: tuple[int, int],
    direction: tuple[int, int] = DIRECTION_DEFAULT,
    rotation: dict[tuple[int, int], int] = ROTATE_RIGHT,
) -> dict[tuple[int, int], bool]:
    tiles = {guard: True}

    while check_is_in_board(dimension, *guard):
        direction, guard = guard_move(obstructions, guard, direction, rotation)

        tiles[guard] = True

    # last tile is outside of the board
    del tiles[guard]

    return tiles  # type: ignore


def part1(input: str) -> int:
    return len(get_visited_tiles(*parse(input)))


def part2(input: str) -> int:
    board = parse(input)

    tiles = get_visited_tiles(*board)
    del tiles[board[1]]

    return len(
        tuple(
            None
            for tile in tiles
            if check_is_loopable(
                tile,
                *board,
            )
        )
    )


def check_is_loopable(
    new_obstacle: tuple[int, int],
    obstructions: dict[tuple[int, int], bool],
    guard: tuple[int, int],
    dimension: tuple[int, int],
    direction=DIRECTION_DEFAULT,
    rotation=ROTATE_RIGHT,
) -> bool:
    result = False

    steps = dict()

    while check_is_in_board(dimension, *guard):
        direction, guard_new = guard_move_with_new_obstacle(
            obstructions,
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
