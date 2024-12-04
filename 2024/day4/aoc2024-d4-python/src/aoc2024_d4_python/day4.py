from ast import Assert
from sys import stdin

goal = "XMAS"


def board_get_offset(board, x, y):
    assert 0 <= x < len(board[0])
    assert 0 <= y < len(board)

    return board[y][x]


def find_w2e(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            goal[offset] == board_get_offset(board, x + offset, y)  # fmt: skip
            for offset in range(len(goal))
        )
    except AssertionError:
        return False


def find_e2w(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            goal[offset] == board_get_offset(board, x - offset, y)  # fmt: skip
            for offset in range(len(goal))
        )
    except AssertionError:
        return False


def find_n2s(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            goal[offset] == board_get_offset(board, x, y + offset)  # fmt: skip
            for offset in range(len(goal))
        )
    except AssertionError:
        return False


def find_s2n(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            goal[offset] == board_get_offset(board, x, y - offset)  # fmt: skip
            for offset in range(len(goal))
        )
    except AssertionError:
        return False


def find_nw2se(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            goal[offset] == board_get_offset(board, x + offset, y + offset)  # fmt: skip
            for offset in range(len(goal))
        )
    except AssertionError:
        return False


def find_se2nw(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            goal[offset] == board_get_offset(board, x - offset, y - offset)  # fmt: skip
            for offset in range(len(goal))
        )
    except AssertionError:
        return False


def find_ne2sw(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            goal[offset] == board_get_offset(board, x - offset, y + offset)  # fmt: skip
            for offset in range(len(goal))
        )
    except AssertionError:
        return False


def find_sw2ne(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            goal[offset] == board_get_offset(board, x + offset, y - offset)  # fmt: skip
            for offset in range(len(goal))
        )
    except AssertionError:
        return False


def find_start(board: tuple[str, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (x, y)
        for y in range(len(board))
        for x in range(len(board[y]))
        if board[y][x] == goal[0]
    )


def count_goal(board: tuple[str, ...]) -> int:
    def finder(x, y, board) -> int:
        result = (
            find_w2e(x, y, board),
            find_e2w(x, y, board),
            find_n2s(x, y, board),
            find_s2n(x, y, board),
            find_nw2se(x, y, board),
            find_se2nw(x, y, board),
            find_ne2sw(x, y, board),
            find_sw2ne(x, y, board),
        )

        return len([x for x in result if x])

    return sum(finder(*(*point, board)) for point in find_start(board))


def main() -> None:
    input = stdin.read()

    print("PYTHON:", count_goal(tuple(input.strip().splitlines())))


if __name__ == "__main__":
    main()
