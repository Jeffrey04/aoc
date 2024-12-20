from aoc2024_d14_python.day14 import (
    move,
    move_robots,
    parse,
    part1,
    robot_map_to_quadrants,
    robots_to_map,
)

input = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


def test_parse() -> None:
    expected = (
        (
            (0, 4),
            (6, 3),
            (10, 3),
            (2, 0),
            (0, 0),
            (3, 0),
            (7, 6),
            (3, 0),
            (9, 3),
            (7, 3),
            (2, 4),
            (9, 5),
        ),
        (
            (3, -3),
            (-1, -3),
            (-1, 2),
            (2, -1),
            (1, 3),
            (-2, -2),
            (-1, -3),
            (-1, -2),
            (2, 3),
            (-1, 2),
            (2, -3),
            (-3, -3),
        ),
    )

    assert parse(input) == expected


def test_move() -> None:
    robot = (2, 4)
    velocity = (2, -3)
    dimension = (11, 7)
    expected = (4, 1)

    assert (robot := move(robot, velocity, dimension)) == expected

    expected = (6, 5)
    assert (robot := move(robot, velocity, dimension)) == expected

    expected = (8, 2)
    assert (robot := move(robot, velocity, dimension)) == expected

    expected = (10, 6)
    assert (robot := move(robot, velocity, dimension)) == expected

    expected = (1, 3)
    assert (robot := move(robot, velocity, dimension)) == expected


def test_move_robots() -> None:
    dimension = (11, 7)
    seconds = 100
    expected = {
        (6, 0): 2,
        (9, 0): 1,
        (0, 2): 1,
        (1, 3): 1,
        (2, 3): 1,
        (5, 4): 1,
        (3, 5): 1,
        (4, 5): 2,
        (1, 6): 1,
        (6, 6): 1,
    }

    assert (
        robots_to_map(move_robots(*parse(input), dimension=dimension, seconds=seconds))
        == expected
    )


def test_robot_map_to_quadrants() -> None:
    dimension = (11, 7)
    robot_map = {
        (6, 0): 2,
        (9, 0): 1,
        (0, 2): 1,
        (1, 3): 1,
        (2, 3): 1,
        (5, 4): 1,
        (3, 5): 1,
        (4, 5): 2,
        (1, 6): 1,
        (6, 6): 1,
    }
    expected = (
        {
            (0, 2): 1,
        },
        {
            (6, 0): 2,
            (9, 0): 1,
        },
        {
            (3, 5): 1,
            (4, 5): 2,
            (1, 6): 1,
        },
        {
            (6, 6): 1,
        },
    )

    assert robot_map_to_quadrants(robot_map, dimension) == expected


def test_part1() -> None:
    dimension = (11, 7)
    expected = 12

    assert part1(input, dimension) == expected
