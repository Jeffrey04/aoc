from collections.abc import Generator
from dataclasses import dataclass
from sys import stdin

import dask.bag as db
from dask.diagnostics import ProgressBar  # type: ignore

SYMBOL_GUARD = "^"
SYMBOL_OBSTRUCTION = "#"

ROTATE_RIGHT = {
    (0, 0): 0,
    (0, 1): 1,
    (1, 0): -1,
    (1, 1): 0,
}


@dataclass
class Guard:
    position: tuple[int, int]
    direction = (0, -1)

    def rotate(self, direction: dict[tuple[int, int], int]) -> None:
        self.direction = (
            self.direction[0] * ROTATE_RIGHT[(0, 0)]
            + self.direction[1] * ROTATE_RIGHT[(1, 0)],
            self.direction[0] * ROTATE_RIGHT[(0, 1)]
            + self.direction[1] * ROTATE_RIGHT[(1, 1)],
        )

    def forward(self) -> tuple[int, int]:
        return (
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1],
        )


@dataclass
class Board:
    obstruction: tuple[tuple[int, int], ...]
    guard: Guard
    dimension: tuple[int, int]
    rotation: dict[tuple[int, int], int]

    def check_is_in_board(self, x: int, y: int) -> bool:
        return not (x < 0 or y < 0 or x >= self.dimension[0] or y >= self.dimension[1])

    def check_is_obstruction(self, x: int, y: int) -> bool:
        return (x, y) in self.obstruction

    def check_guard_can_move(self) -> bool:
        return not self.check_is_obstruction(*self.guard.forward())

    def move_guard(self) -> tuple[int, int]:
        destination = self.guard.forward()

        match self.check_guard_can_move():
            case True:
                self.guard.position = destination

            case False:
                self.guard.rotate(self.rotation)

        return self.guard.position


def finder(
    board: tuple[str, ...], symbol: str
) -> Generator[tuple[int, int], None, None]:
    return (
        (x, y)
        for y, row in enumerate(board)
        for x, item in enumerate(tuple(row))
        if item == symbol
    )


def parse(input: str) -> Board:
    board = tuple(input.strip().splitlines())
    position = next(finder(board, SYMBOL_GUARD))

    return Board(
        tuple(finder(board, SYMBOL_OBSTRUCTION)),
        Guard(position),
        ((len(board[0]), len(board))),
        ROTATE_RIGHT,
    )


def part1(input: str) -> int:
    board = parse(input)
    unique_steps = {board.guard.position}

    while board.check_is_in_board(*board.guard.position):
        unique_steps.add(board.move_guard())

    # last step is outside of the board
    return len(unique_steps) - 1


def part2(input: str) -> int:
    board = parse(input)
    initial, steps = board.guard.position, []

    while board.check_is_in_board(*board.guard.position):
        step = (board.guard.position, board.move_guard())

        if step[0] != step[1]:
            steps.append(step)

    with ProgressBar():
        return (
            db.from_sequence(  # type: ignore
                # condition 1: point must be a original visited point
                set(
                    (point, input_insert_obstacle(input, point))
                    for _, point in steps[:-1]
                    if point != initial
                ),
                50,
            )
            .starmap(check_is_loopable)
            .filter(None)
            .count()
            .compute()
        )


def input_insert_obstacle(input: str, point: tuple[int, int]) -> str:
    return "\n".join(
        "".join(
            SYMBOL_OBSTRUCTION if point == (x, y) else item
            for x, item in enumerate(tuple(row))
        )
        for y, row in enumerate(input.strip().splitlines())
    )


def check_is_loopable(point: tuple[int, int], input: str) -> bool:
    result = False

    board = parse(input)

    steps = []

    while board.check_is_in_board(*board.guard.position):
        step = (board.guard.position, board.move_guard())

        if step[0] == step[1]:
            continue
        elif step in steps:
            # condition 2: if current step was attempted, it is a loop
            result = True
            break

        steps.append(step)

    return result


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
