from operator import itemgetter
from sys import stdin

xmas = "XMAS"
mas = "MAS"


def board_get_point(board, x, y):
    assert 0 <= x < len(board[0])
    assert 0 <= y < len(board)

    return board[y][x]


def find_cross(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        cross = tuple(
            (
                board_get_point(board, x + offset, y + offset),
                board_get_point(board, x - offset, y + offset),
            )
            for offset in range(-1, 2)
        )
    except AssertionError:
        return False

    return all(
        word in (mas, mas[::-1])
        for word in ("".join(map(itemgetter(i), cross)) for i in range(2))
    )


def find_w2e(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            xmas[offset] == board_get_point(board, x + offset, y)  # fmt: skip
            for offset in range(len(xmas))
        )
    except AssertionError:
        return False


def find_e2w(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            xmas[offset] == board_get_point(board, x - offset, y)  # fmt: skip
            for offset in range(len(xmas))
        )
    except AssertionError:
        return False


def find_n2s(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            xmas[offset] == board_get_point(board, x, y + offset)  # fmt: skip
            for offset in range(len(xmas))
        )
    except AssertionError:
        return False


def find_s2n(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            xmas[offset] == board_get_point(board, x, y - offset)  # fmt: skip
            for offset in range(len(xmas))
        )
    except AssertionError:
        return False


def find_nw2se(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            xmas[offset] == board_get_point(board, x + offset, y + offset)  # fmt: skip
            for offset in range(len(xmas))
        )
    except AssertionError:
        return False


def find_se2nw(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            xmas[offset] == board_get_point(board, x - offset, y - offset)  # fmt: skip
            for offset in range(len(xmas))
        )
    except AssertionError:
        return False


def find_ne2sw(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            xmas[offset] == board_get_point(board, x - offset, y + offset)  # fmt: skip
            for offset in range(len(xmas))
        )
    except AssertionError:
        return False


def find_sw2ne(x: int, y: int, board: tuple[str, ...]) -> bool:
    try:
        return all(
            xmas[offset] == board_get_point(board, x + offset, y - offset)  # fmt: skip
            for offset in range(len(xmas))
        )
    except AssertionError:
        return False


def find_anchor(board: tuple[str, ...], anchor: str) -> tuple[tuple[int, int], ...]:
    return tuple(
        (x, y)
        for y in range(len(board))
        for x in range(len(board[y]))
        if board[y][x] == anchor
    )


def count_xmas(board: tuple[str, ...]) -> int:
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

    return sum(finder(*(*point, board)) for point in find_anchor(board, xmas[0]))


def count_cross(board: tuple[str, ...]) -> int:
    return len(
        [True for point in find_anchor(board, mas[1]) if find_cross(*(*point, board))]
    )


def main() -> None:
    input = tuple(stdin.read().strip().splitlines())

    print("PYTHON:", count_xmas(input), count_cross(input))


if __name__ == "__main__":
    main()
