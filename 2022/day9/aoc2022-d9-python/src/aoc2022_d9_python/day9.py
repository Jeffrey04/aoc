from collections import defaultdict, namedtuple
from functools import partial, reduce
from operator import add
from sys import stdin
from typing import Optional

State = namedtuple(
    "State",
    ["is_start", "is_head", "is_tail", "tail_visited"],
    defaults=[False, False, False, False],
)

DIRECTION_UP = "U"
DIRECTION_DOWN = "D"
DIRECTION_LEFT = "L"
DIRECTION_RIGHT = "R"

DIRECTIONS = {
    DIRECTION_UP: (1, 0),
    DIRECTION_DOWN: (-1, 0),
    DIRECTION_LEFT: (0, -1),
    DIRECTION_RIGHT: (0, 1),
}


def rope_init(
    head: tuple[int, int],
    tail: Optional[tuple[int, int]] = None,
    is_start: Optional[bool] = False,
) -> dict[int, dict[int, State]]:
    rope: dict[int, dict[int, State]] = defaultdict(partial(defaultdict, State))

    head_updated = State(
        is_start=is_start or rope[head[0]][head[1]].is_start,
        is_head=True,
        is_tail=rope[head[0]][head[1]].is_tail,
        tail_visited=rope[head[0]][head[1]].tail_visited,
    )

    rope[head[0]][head[1]] = head_updated

    if tail:
        rope[tail[0]][tail[1]] = State(
            is_start=rope[tail[0]][tail[1]].is_start,
            is_head=rope[tail[0]][tail[1]].is_head,
            is_tail=True,
            tail_visited=True,
        )
    else:
        rope[head[0]][head[1]] = State(
            is_start=rope[head[0]][head[1]].is_start,
            is_head=rope[head[0]][head[1]].is_head,
            is_tail=True,
            tail_visited=True,
        )

    return rope


def check_rope_is_touching(rope_state: dict[int, dict[int, State]]) -> bool:
    head, tail = rope_find_ends(rope_flatten(rope_state))

    return (
        head[0] == tail[0]
        or check_is_adjacent(head[0], tail[0])
        or check_is_diagonal(head[0], tail[0])
    )


def check_is_adjacent(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return (head[0] == tail[0] and abs(head[1] - tail[1]) == 1) or (
        head[1] == tail[1] and abs(head[0] - tail[0]) == 1
    )


def check_is_diagonal(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return head[0] in (tail[0] + 1, tail[0] - 1) and head[1] in (
        tail[1] + 1,
        tail[1] - 1,
    )


def rope_find_ends(
    rope_state_flatten: tuple[tuple[tuple[int, int], State], ...]
) -> tuple[tuple[tuple[int, int], State], tuple[tuple[int, int], State]]:
    return (
        next(filter(lambda item: item[-1].is_head, rope_state_flatten)),
        next(filter(lambda item: item[-1].is_tail, rope_state_flatten)),
    )


def rope_flatten(
    rope_state: dict[int, dict[int, State]]
) -> tuple[tuple[tuple[int, int], State], ...]:
    return tuple(
        ((row, col), state)
        for row, _col in rope_state.items()
        for col, state in _col.items()
    )


def rope_move_tail(
    rope_state: dict[int, dict[int, State]], direction_head: str
) -> dict[int, dict[int, State]]:
    if check_rope_is_touching(rope_state):
        return rope_state

    head, tail_current = rope_find_ends(rope_flatten(rope_state))
    tail_position_new = tuple(map(add, tail_current[0], DIRECTIONS[direction_head]))

    if check_is_adjacent(head[0], tail_position_new):
        rope_state[tail_current[0][0]][tail_current[0][1]] = State(
            is_start=rope_state[tail_current[0][0]][tail_current[0][1]].is_start,
            is_head=rope_state[tail_current[0][0]][tail_current[0][1]].is_head,
            is_tail=False,
            tail_visited=rope_state[tail_current[0][0]][
                tail_current[0][1]
            ].tail_visited,
        )
        rope_state[tail_position_new[0]][tail_position_new[1]] = State(
            is_start=rope_state[tail_position_new[0]][tail_position_new[1]].is_start,
            is_head=rope_state[tail_position_new[0]][tail_position_new[1]].is_head,
            is_tail=True,
            tail_visited=True,
        )

    else:
        second_move = (
            (DIRECTION_UP, DIRECTION_DOWN)
            if direction_head in (DIRECTION_LEFT, DIRECTION_RIGHT)
            else (DIRECTION_LEFT, DIRECTION_RIGHT)
        )

        for move in second_move:
            tail_position_final = tuple(map(add, tail_position_new, DIRECTIONS[move]))

            if check_is_adjacent(head[0], tail_position_final):
                rope_state[tail_current[0][0]][tail_current[0][1]] = State(
                    is_start=rope_state[tail_current[0][0]][
                        tail_current[0][1]
                    ].is_start,
                    is_head=rope_state[tail_current[0][0]][tail_current[0][1]].is_head,
                    is_tail=False,
                    tail_visited=rope_state[tail_current[0][0]][
                        tail_current[0][1]
                    ].tail_visited,
                )
                rope_state[tail_position_final[0]][tail_position_final[1]] = State(
                    is_start=rope_state[tail_position_final[0]][
                        tail_position_final[1]
                    ].is_start,
                    is_head=rope_state[tail_position_final[0]][
                        tail_position_final[1]
                    ].is_head,
                    is_tail=True,
                    tail_visited=True,
                )
                break

    return rope_state


def rope_move_head(
    rope_state: dict[int, dict[int, State]], direction: str
) -> dict[int, dict[int, State]]:
    head, _ = rope_find_ends(rope_flatten(rope_state))
    head_position = tuple(map(add, head[0], DIRECTIONS[direction]))

    rope_state[head[0][0]][head[0][1]] = State(
        is_start=rope_state[head[0][0]][head[0][1]].is_start,
        is_head=False,
        is_tail=rope_state[head[0][0]][head[0][1]].is_tail,
        tail_visited=rope_state[head[0][0]][head[0][1]].tail_visited,
    )
    rope_state[head_position[0]][head_position[1]] = State(
        is_start=rope_state[head_position[0]][head_position[1]].is_start,
        is_head=True,
        is_tail=rope_state[head_position[0]][head_position[1]].is_tail,
        tail_visited=rope_state[head_position[0]][head_position[1]].tail_visited,
    )

    return rope_state


def rope_move_motion(
    rope_state: dict[int, dict[int, State]], direction: str, repetition: int
) -> dict[int, dict[int, State]]:
    return (
        rope_state
        if repetition == 0
        else rope_move_motion(
            rope_move_tail(rope_move_head(rope_state, direction), direction),
            direction,
            repetition - 1,
        )
    )


def rope_calculate_visited(
    rope_state: dict[int, dict[int, State]], motion_list: str
) -> int:
    return len(
        tuple(
            item
            for item in rope_flatten(
                reduce(
                    lambda current, incoming: rope_move_motion(
                        current, incoming[0], int(incoming[1])
                    ),
                    (
                        item.strip().split(" ")
                        for item in motion_list.strip().splitlines()
                    ),
                    rope_state,
                )
            )
            if item[-1].tail_visited
        )
    )


def main() -> None:
    input_raw = stdin.read()

    print(
        f"PYTHON:\t{rope_calculate_visited(rope_init((0, 0), is_start=True), input_raw)}"
    )


if __name__ == "__main__":
    main()
