from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
from itertools import chain, pairwise
from queue import PriorityQueue
from sys import stdin
from typing import Literal

from cytoolz.functoolz import compose, memoize
from cytoolz.itertoolz import first, last
from pyrsistent import PMap, pmap

# FIXME alternatively I should do this as Enum to fix all the type error
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
        lambda current, incoming: current
        + (0 if first(incoming) == last(incoming) else 1),
        pairwise(actions),
        0,
    )


def actions_list_filter_minimum(
    actions_list: Sequence[Actions] | Iterator[Actions],
) -> Sequence[Actions]:
    delta = tuple((actions_get_delta(actions), actions) for actions in actions_list)

    return tuple(actions for d, actions in delta if d == first(min(delta, key=first)))


def actions_to_string(actions: Actions) -> str:
    return "".join(action.value for action in actions)


def code_to_actions[T](
    code: Sequence[CodeKey],
    depth: int,
    collector_code: Callable[[Iterator[T]], T] = compose(tuple, chain.from_iterable),
    default: T = (),
    collector_branch: Callable[[Iterator[T]], T] = compose(
        first, actions_list_filter_minimum
    ),
    collector_leaf: Callable[[Sequence[Actions]], T] = compose(
        first, actions_list_filter_minimum
    ),
) -> T:
    return collector_code(
        code_expand(
            code,
            keypad_init_numeric(),
            keypad_init_directional(),
            depth,
            default,
            collector_branch,
            collector_leaf,
        )
    )


@memoize
def actions_expand[T](
    actions: Actions,
    depth: int,
    action_pad: Keypad[Action],
    default: T,
    collector_branch: Callable[[Iterator[T]], T],
    collector_leaf: Callable[[Sequence[Actions]], T],
) -> T:
    assert depth >= 1

    candidates = ((),)
    result = default

    position = action_pad.initial
    for action in actions:
        position, actions_list = destination_get_actions(action_pad, action, position)

        if depth == 1:
            candidates = tuple(
                result + actions_incoming
                for result in candidates
                for actions_incoming in actions_list
            )
        else:
            result += collector_branch(
                actions_expand(
                    actions_incoming,
                    depth - 1,
                    action_pad,
                    default,
                    collector_branch,
                    collector_leaf,
                )
                for actions_incoming in actions_list
            )  # type: ignore

    if depth == 1:
        result = collector_leaf(candidates)

    return result


def actions_expand_optimized[T](
    actions_list: Sequence[Actions],
    depth: int,
    action_pad: Keypad[Action],
    default: T,
    collector_branch: Callable[[Iterator[T]], T],
    collector_leaf: Callable[[Sequence[Actions]], T],
) -> T:
    return collector_branch(
        actions_expand(
            actions, depth, action_pad, default, collector_branch, collector_leaf
        )
        for actions in actions_list
    )


def code_expand[T](
    code: Sequence[CodeKey],
    num_pad: Keypad[CodeKey],
    action_pad: Keypad[Action],
    depth: int,
    default: T,
    collector_branch: Callable[[Iterator[T]], T],
    collector_leaf: Callable[[Sequence[Actions]], T],
) -> Iterator[T]:
    robot_position = num_pad.initial

    for code_key in code:
        robot_position, actions_list = destination_get_actions(
            num_pad,
            code_key,
            robot_position,
        )

        yield actions_expand_optimized(
            actions_list,
            depth,
            action_pad,
            default,
            collector_branch,
            collector_leaf,
        )


def actions_to_complexity(actions: int | Actions, code: str) -> int:
    return (actions if isinstance(actions, int) else len(actions)) * int(
        code.rstrip("A").lstrip("0")
    )


def part1(input: str) -> int:
    return sum(
        actions_to_complexity(
            code_to_actions(
                code,  # type: ignore
                2,
            ),
            code,
        )
        for code in input.strip().splitlines()
    )


def part2(input: str) -> int:
    return sum(
        actions_to_complexity(
            code_to_actions(
                code,  # type: ignore
                25,
                sum,
                0,
                min,
                lambda actions_list: min(len(actions) for actions in actions_list),
            ),
            code,
        )
        for code in input.strip().splitlines()
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
