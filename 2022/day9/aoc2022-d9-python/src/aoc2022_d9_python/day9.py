from collections import defaultdict, namedtuple
from functools import reduce
from operator import add
from sys import stdin
from typing import Optional, Union

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
        chain: int = 0,
        tail: Optional[tuple[int, int]] = None,
    ) -> None:
        super().__init__(lambda: False)

        self.start = head
        self.head = head

        self.chain = chain

        self.tail = (tail,) if tail else ((head,) * chain)

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
        return self._tail[-1], self[self._tail[-1]]

    @tail.setter
    def tail(self, tail: tuple[tuple[int, int], ...]) -> None:
        self._tail = tail
        self[self._tail[-1]] = True

    @property
    def tail_chain(self) -> tuple[tuple[int, int], ...]:
        return self._tail

    def __repr__(self) -> str:
        return repr(
            dict(
                self,
                _HEAD=self.head,
                _TAIL=self.tail,
                _TAIL_CHAIN=self.tail_chain,
                _START=self.start,
            )
        )


def check_rope_is_touching(alpha: tuple[int, int], beta: tuple[int, int]) -> bool:
    return (
        alpha == beta
        or check_is_adjacent(alpha, beta)
        or check_is_diagonal(alpha, beta)
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
    result = []
    head_current, _ = rope_state.head

    for tail_current in rope_state.tail_chain:
        if check_rope_is_touching(head_current, tail_current):
            result.append(tail_current)

        else:
            tail_position_new: tuple[int, int] = tuple(
                map(add, tail_current, DIRECTIONS[direction_head])
            )

            if check_is_adjacent(head_current, tail_position_new):
                result.append(tail_position_new)

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

                    if check_rope_is_touching(head_current, tail_position_final):
                        result.append(tail_position_final)
                        direction_head = move
                        break

        head_current = result[-1]

    rope_state.tail = tuple(result)

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


def visualize(rope_state: Rope) -> Rope:
    if len(rope_state.tail_chain) < 9:
        return rope_state

    for row in range(50, -50, -1):
        line = []
        for column in range(-50, 50):
            position = (row, column)
            line.append(
                "H"
                if rope_state.head[0] == position
                else "1"
                if rope_state.tail_chain[0] == position
                else "2"
                if rope_state.tail_chain[1] == position
                else "3"
                if rope_state.tail_chain[2] == position
                else "4"
                if rope_state.tail_chain[3] == position
                else "5"
                if rope_state.tail_chain[4] == position
                else "6"
                if rope_state.tail_chain[5] == position
                else "7"
                if rope_state.tail_chain[6] == position
                else "8"
                if rope_state.tail_chain[7] == position
                else "9"
                if rope_state.tail_chain[8] == position
                else "s"
                if rope_state.start[0] == position
                else "#"
                if rope_state[position]
                else "."
            )
        print("".join(line))

    print()
    return rope_state


def main() -> None:
    input_raw = stdin.read()

    print(
        f"PYTHON:\t{rope_calculate_visited(Rope((0, 0), chain=1), input_raw)} "
        f"{rope_calculate_visited(Rope((0, 0), chain=9), input_raw)}"
    )


if __name__ == "__main__":
    main()
