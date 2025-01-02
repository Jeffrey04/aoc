from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
from itertools import count, pairwise
from math import inf
from queue import PriorityQueue
from sys import stdin
from typing import Literal

from cytoolz.functoolz import memoize
from cytoolz.itertoolz import first
from pyrsistent import PMap, pmap

type CodeKey = Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A"]
type Actions = tuple[Action, ...]


@dataclass(frozen=True)
class Vector:
    row: int
    column: int


@dataclass(frozen=True)
class Position:
    row: int
    column: int

    def __add__(self, vector: Vector) -> Position:
        return Position(self.row + vector.row, self.column + vector.column)


class Action(Enum):
    Up = "^"
    Down = "v"
    Left = "<"
    Right = ">"
    Activate = "A"


@dataclass(frozen=True)
class Keypad[T]:
    buttons: PMap[Position, T]
    initial: Position


@dataclass(order=True)
class Node:
    cost: int
    position: Position = field(compare=False)


def keypad_init_numeric() -> Keypad[CodeKey]:
    return Keypad(
        pmap(
            {
                Position(0, 0): "7",
                Position(1, 0): "8",
                Position(2, 0): "9",
                Position(0, 1): "4",
                Position(1, 1): "5",
                Position(2, 1): "6",
                Position(0, 2): "1",
                Position(1, 2): "2",
                Position(2, 2): "3",
                Position(1, 3): "0",
                Position(2, 3): "A",
            }
        ),
        Position(2, 3),
    )


def keypad_init_directional() -> Keypad[Action]:
    return Keypad(
        pmap(
            {
                Position(1, 0): Action.Up,
                Position(2, 0): Action.Activate,
                Position(0, 1): Action.Left,
                Position(1, 1): Action.Down,
                Position(2, 1): Action.Right,
            }
        ),
        Position(2, 0),
    )


def action_to_vector(direction: Action) -> Vector:
    match direction:
        case Action.Up:
            return Vector(0, -1)

        case Action.Down:
            return Vector(0, 1)

        case Action.Left:
            return Vector(-1, 0)

        case Action.Right:
            return Vector(1, 0)

        case Action.Activate:
            raise Exception("Activation is not a direction")


@memoize
def destination_get_actions[T](
    keypad: Keypad[T], destination: T, origin: Position
) -> tuple[Position, Sequence[Actions]]:
    open: PriorityQueue[Node] = PriorityQueue()
    open.put(Node(0, origin))
    visited = set()
    actions_list: dict[Position, set[Actions]] = {origin: {()}}
    result = None

    while not open.empty():
        current = open.get()

        if keypad.buttons.get(current.position) == destination:
            result = current.position
            continue
        elif current.position in visited:
            continue

        visited.add(current.position)

        if keypad.buttons.get(current.position) is not None:
            for action in (Action.Up, Action.Down, Action.Left, Action.Right):
                vector = action_to_vector(action)

                open.put(Node(current.cost + 1, current.position + vector))

                actions_list[current.position + vector] = actions_list.get(
                    current.position + vector, set()
                ) | set(
                    actions + (action,) for actions in actions_list[current.position]
                )

    assert result is not None

    return result, actions_list_filter_minimum(
        moves + (Action.Activate,) for moves in actions_list[result]
    )


def actions_get_delta(actions: Actions) -> int:
    return reduce(
        lambda current, incoming: current + (0 if incoming[0] == incoming[1] else 1),
        pairwise(actions),
        0,
    )


def actions_list_filter_minimum(
    actions_list: Sequence[Actions] | Iterator[Actions],
) -> Sequence[Actions]:
    delta = tuple((actions_get_delta(actions), actions) for actions in actions_list)

    return tuple(
        actions
        for d, actions in delta
        if d == (min(delta, key=lambda item: item[0])[0])
    )


def action_to_string(action: Action) -> str:
    match action:
        case Action.Up:
            return "^"
        case Action.Down:
            return "v"
        case Action.Left:
            return "<"
        case Action.Right:
            return ">"
        case Action.Activate:
            return "A"


def actions_to_string(actions: Actions) -> str:
    return "".join(action_to_string(action) for action in actions)


def get_user_actions(remote_actions: Actions, user_pad: Keypad[Action]) -> Actions:
    results = ((),)
    user_position = user_pad.initial

    for action in remote_actions:
        user_position, actions_list = destination_get_actions(
            user_pad,
            action,
            user_position,
        )

        results = tuple(
            result + actions for result in results for actions in actions_list
        )

    return first(actions_list_filter_minimum(results))  # type: ignore


@memoize
def get_remote_actions(
    door_actions: Actions, remote_pad: Keypad[Action]
) -> Sequence[Actions]:
    remote_position = remote_pad.initial
    results = ((),)

    for door_action in door_actions:
        remote_position, remote_actions_list = destination_get_actions(
            remote_pad, door_action, remote_position
        )

        results = tuple(
            result + remote_actions
            for result in results
            for remote_actions in remote_actions_list
        )

    return results


def get_robot_actions(code: str, door_pad: Keypad[CodeKey]) -> Sequence[Actions]:
    robot_position = door_pad.initial
    results = ((),)

    for code_key in tuple(code):
        robot_position, robot_actions_list = destination_get_actions(
            door_pad,
            code_key,  # type: ignore
            robot_position,
        )

        results = tuple(
            result + robot_actions
            for result in results
            for robot_actions in robot_actions_list
        )

    return results


def code_to_actions(code: str) -> Actions:
    return first(
        actions_list_filter_minimum(
            get_user_actions(remote_actions, keypad_init_directional())
            for robot_actions in get_robot_actions(code, keypad_init_numeric())
            for remote_actions in get_remote_actions(
                robot_actions, keypad_init_directional()
            )
        )
    )


def code_to_actions2(code: str) -> Actions:
    results = get_robot_actions(code, keypad_init_numeric())
    min_delta, to_return = inf, None

    for _ in range(25):
        results = (
            actions
            for result in results
            for actions in get_remote_actions(result, keypad_init_directional())
        )

    for result in results:
        actions = get_user_actions(result, keypad_init_directional())
        delta = actions_get_delta(actions)

        if delta < min_delta:
            min_delta = delta
            to_return = actions

    assert to_return is not None

    return to_return


def actions_to_complexity(actions: Actions, code: str) -> int:
    return len(actions) * int(code.rstrip("A").lstrip("0"))


def part1(input: str) -> int:
    return sum(
        actions_to_complexity(code_to_actions(code), code)
        for code in input.strip().splitlines()
    )


def part2(input: str) -> int:
    return sum(
        actions_to_complexity(code_to_actions2(code), code)
        for code in input.strip().splitlines()
    )


def main() -> None:
    input = stdin.read()
    # print("PYTHON:", part1(input))
    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
