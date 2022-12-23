from functools import reduce
from operator import mul
from sys import stdin

DIRECTION_LEFT = 0
DIRECTION_RIGHT = 1
DIRECTION_TOP = 2
DIRECTION_BOTTOM = 3
DIRECTIONS = (DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_TOP, DIRECTION_BOTTOM)


def map_create(map_raw: str) -> list[list[int]]:
    return [[int(tree) for tree in line] for line in map_raw.strip().splitlines()]


def tree_list_previous(
    tree_map: list[list[int]], row: int, col: int, direction: int
) -> list[int]:
    return (
        tree_list_left(tree_map, row, col)
        if direction == DIRECTION_LEFT
        else tree_list_right(tree_map, row, col)
        if direction == DIRECTION_RIGHT
        else tree_list_top(tree_map, row, col)
        if direction == DIRECTION_TOP
        else tree_list_bottom(tree_map, row, col)
    )


def tree_list_left(tree_map: list[list[int]], row: int, col: int) -> list[int]:
    return [tree_map[row][c] for c in range(col + 1)]


def tree_list_right(tree_map: list[list[int]], row: int, col: int) -> list[int]:
    return [tree_map[row][c] for c in range(col, len(tree_map[0]))][::-1]


def tree_list_top(tree_map: list[list[int]], row: int, col: int) -> list[int]:
    return [tree_map[r][col] for r in range(row + 1)]


def tree_list_bottom(tree_map: list[list[int]], row: int, col: int) -> list[int]:
    return [tree_map[r][col] for r in range(row, len(tree_map))][::-1]


def check_tree_is_visible(tree_list: list[int]) -> bool:
    return len(tree_list) == 1 or all(tree < tree_list[-1] for tree in tree_list[:-1])


def tree_count_visible(tree_raw: str) -> int:
    tree_map = map_create(tree_raw)

    return sum(
        int(
            any(
                check_tree_is_visible(tree_list_previous(tree_map, row, col, direction))
                for direction in DIRECTIONS
            )
        )
        for row in range(len(tree_map))
        for col in range(len(tree_map[0]))
    )


def tree_count_distance(tree_list: list[int], idx: int = -2, result: int = 0) -> int:
    return (
        result
        if idx < len(tree_list) * -1
        else tree_count_distance(tree_list, idx - 1, result + 1)
        if tree_list[idx] < tree_list[-1]
        else (result + 1)
    )


def tree_count_score(tree_map: list[list[int]], row: int, col: int) -> int:
    return reduce(
        mul,
        (
            tree_count_distance(tree_list_previous(tree_map, row, col, direction))
            for direction in DIRECTIONS
        ),
    )


def tree_count_best_score(tree_raw: str) -> int:
    tree_map = map_create(tree_raw)

    return max(
        tree_count_score(tree_map, row, col)
        for row in range(len(tree_map))
        for col in range(len(tree_map[0]))
    )


def main() -> None:
    tree_raw = stdin.read()

    print(f"PYTHON:\t{tree_count_visible(tree_raw)} {tree_count_best_score(tree_raw)}")


if __name__ == "__main__":
    main()
