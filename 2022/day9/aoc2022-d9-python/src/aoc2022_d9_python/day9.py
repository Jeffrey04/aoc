from collections import defaultdict, namedtuple
from functools import partial, reduce
from operator import add
from sys import stdin
from typing import Optional, Union

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


class Rope(defaultdict):
    def __init__(
        self,
        head: tuple[int, int],
        tail: Optional[tuple[int, int]] = None,
    ) -> None:
        super().__init__(lambda: False)

        self.start = head
        self.head = head
        self.tail = tail if tail else head
        self[self._tail] = True

    @property
    def start(self) -> tuple[tuple[int, int], bool]:
        return self._start, self[self._start]

    @start.setter
    def start(self, start: tuple[int, int]) -> None:
        self._start = start

    @property
    def head(self) -> tuple[tuple[int, int], bool]:
        return self._head, self[self._head]

    @head.setter
    def head(self, head: tuple[int, int]) -> None:
        self._head = head

    @property
    def tail(self) -> tuple[tuple[int, int], bool]:
        return self._tail, self[self._tail]

    @tail.setter
    def tail(self, tail: tuple[int, int]) -> None:
        self._tail = tail
        self[self._tail] = True

    def __repr__(self) -> str:
        return repr(dict(self, _HEAD=self.head, _TAIL=self.tail, _START=self.start))


def check_rope_is_touching(rope_state: Rope) -> bool:
    head, _ = rope_state.head
    tail, _ = rope_state.tail

    return (
        head == tail or check_is_adjacent(head, tail) or check_is_diagonal(head, tail)
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


def rope_move_tail(rope_state: Rope, direction_head: str) -> Rope:
    if check_rope_is_touching(rope_state):
        return rope_state

    head, _ = rope_state.head
    tail_current, _ = rope_state.tail
    tail_position_new: tuple[int, int] = tuple(
        map(add, tail_current, DIRECTIONS[direction_head])
    )

    if check_is_adjacent(head, tail_position_new):
        rope_state.tail = tail_position_new

    else:
        second_move = (
            (DIRECTION_UP, DIRECTION_DOWN)
            if direction_head in (DIRECTION_LEFT, DIRECTION_RIGHT)
            else (DIRECTION_LEFT, DIRECTION_RIGHT)
        )

        for move in second_move:
            tail_position_final: tuple[int, int] = tuple(
                map(add, tail_position_new, DIRECTIONS[move])
            )

            if check_is_adjacent(head, tail_position_final):
                rope_state.tail = tail_position_final
                break

    return rope_state


def rope_move_head(rope_state: Rope, direction: str) -> Rope:
    head, _ = rope_state.head
    rope_state.head = tuple(map(add, head, DIRECTIONS[direction]))

    return rope_state


def rope_move_motion(rope_state: Rope, direction: str, repetition: int) -> Rope:
    return (
        rope_state
        if repetition == 0
        else rope_move_motion(
            rope_move_tail(rope_move_head(rope_state, direction), direction),
            direction,
            repetition - 1,
        )
    )


def rope_calculate_visited(rope_state: Rope, motion_list: str) -> int:
    return len(
        tuple(
            item
            for item in reduce(
                lambda current, incoming: rope_move_motion(
                    current, incoming[0], int(incoming[1])
                ),
                (item.strip().split(" ") for item in motion_list.strip().splitlines()),
                rope_state,
            ).values()
            if item
        )
    )


def main() -> None:
    input_raw = stdin.read()

    print(f"PYTHON:\t{rope_calculate_visited(Rope((0, 0)), input_raw)}")


if __name__ == "__main__":
    main()
