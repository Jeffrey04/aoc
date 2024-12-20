import operator
from functools import reduce
from itertools import count
from os import system
from sys import stdin
from typing import Annotated

import typer
from cytoolz import merge_with

type Point = tuple[int, int]
type Velocity = tuple[int, int]
type Dimension = tuple[int, int]
type Robot_Map = dict[Point, int]


def parse(
    input: str,
) -> tuple[tuple[Point, ...], tuple[Velocity, ...]]:
    def inner(
        current: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
        incoming: str,
    ) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
        points, velocities = current
        point, velocity = incoming.split(" ")

        return (
            points + (tuple(int(item) for item in point.strip("p=").split(",")),),
            velocities
            + (tuple(int(item) for item in velocity.strip("v=").split(",")),),
        )  # type: ignore

    return reduce(
        inner,
        input.strip().splitlines(),
        ((), ()),  # type: ignore
    )


def move(robot: Point, velocity: Velocity, dimension: Dimension) -> tuple[int, int]:
    return tuple(
        (position + delta) % size
        for position, delta, size in zip(robot, velocity, dimension)
    )  # type: ignore


def move_robots(
    robots: tuple[Point, ...],
    velocities: tuple[Velocity, ...],
    dimension: Dimension,
    seconds: int,
) -> tuple[Point, ...]:
    for _ in range(seconds):
        robots = tuple(
            move(robot, velocity, dimension)
            for robot, velocity in zip(robots, velocities)
        )

    return robots


def robots_to_map(robots: tuple[Point, ...]) -> Robot_Map:
    return reduce(
        lambda current, incoming: merge_with(sum, current, {incoming: 1}), robots, {}
    )


def robot_map_to_quadrants(
    robot_map: Robot_Map, dimension: Dimension
) -> tuple[Robot_Map, Robot_Map, Robot_Map, Robot_Map]:
    width, height = dimension
    x_divider = (width - 1) / 2
    y_divider = (height - 1) / 2

    return (
        {
            (x, y): value
            for (x, y), value in robot_map.items()
            if x < x_divider and y < y_divider
        },
        {
            (x, y): value
            for (x, y), value in robot_map.items()
            if x > x_divider and y < y_divider
        },
        {
            (x, y): value
            for (x, y), value in robot_map.items()
            if x < x_divider and y > y_divider
        },
        {
            (x, y): value
            for (x, y), value in robot_map.items()
            if x > x_divider and y > y_divider
        },
    )


def stepper(input: str, dimension: Dimension) -> None:
    robots, velocities = parse(input)

    for iteration in count(1):
        if iteration % 100 == 0:
            print(f"Iteration {iteration}")

        robots = move_robots(robots, velocities, dimension, 1)
        robot_map = robots_to_map(robots)

        if iteration < 6480:
            continue

        if map_find_with_neighbour(robot_map, 8):
            system("clear")
            for row in tuple(
                tuple(
                    "#" if (row, column) in robot_map else "."
                    for column in range(dimension[0])
                )
                for row in range(dimension[1])
            ):
                print("".join(row))

            typer.confirm(
                f"Continue (Iteration {iteration})?", default=True, abort=True
            )


def map_find_with_neighbour(robot_map: Robot_Map, neighbour_count: int):
    return any(
        len(
            tuple(
                filter(
                    None,
                    (
                        robot_map.get((x - 1, y - 1)),
                        robot_map.get((x - 1, y)),
                        robot_map.get((x - 1, y + 1)),
                        robot_map.get((x, y - 1)),
                        robot_map.get((x, y + 1)),
                        robot_map.get((x + 1, y - 1)),
                        robot_map.get((x + 1, y)),
                        robot_map.get((x + 1, y + 1)),
                    ),
                )
            )
        )
        >= neighbour_count
        for (x, y) in robot_map.keys()
    )


def part1(input: str, dimension: Dimension) -> int:
    return reduce(
        operator.mul,
        (
            sum(quadrant.values())
            for quadrant in robot_map_to_quadrants(
                robots_to_map(
                    move_robots(*parse(input), dimension=dimension, seconds=100)
                ),
                dimension,
            )
        ),
    )


def part2(input: str, dimension: Dimension) -> int:
    robots, velocities = parse(input)

    for iteration in count(1):
        robots = move_robots(robots, velocities, dimension, 1)

        if map_find_with_neighbour(robots_to_map(robots), 8):
            return iteration

    raise Exception("Not found")


def main(
    input_file: Annotated[typer.FileText, typer.Argument()],
    is_stepper: Annotated[bool, typer.Option("--stepper")] = False,
) -> None:
    input = input_file.read()
    dimension = (101, 103)

    match is_stepper:
        case True:
            stepper(input, dimension)

        case False:
            print("PYTHON:", part1(input, dimension), part2(input, dimension))


if __name__ == "__main__":
    typer.run(main)
