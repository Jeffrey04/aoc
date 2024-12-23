from aoc2024_d16_python.day16 import Maze, Point, Wall, parse, part1

input1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

input2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""


def test_parse():
    expected = (
        Maze(
            Point(1, 13),
            Point(13, 1),
            {
                # row 0
                Point(0, 0): Wall(),
                Point(1, 0): Wall(),
                Point(2, 0): Wall(),
                Point(3, 0): Wall(),
                Point(4, 0): Wall(),
                Point(5, 0): Wall(),
                Point(6, 0): Wall(),
                Point(7, 0): Wall(),
                Point(8, 0): Wall(),
                Point(9, 0): Wall(),
                Point(10, 0): Wall(),
                Point(11, 0): Wall(),
                Point(12, 0): Wall(),
                Point(13, 0): Wall(),
                Point(14, 0): Wall(),
                # row 1
                Point(0, 1): Wall(),
                Point(8, 1): Wall(),
                Point(14, 1): Wall(),
                # row 2
                Point(0, 2): Wall(),
                Point(2, 2): Wall(),
                Point(4, 2): Wall(),
                Point(5, 2): Wall(),
                Point(6, 2): Wall(),
                Point(8, 2): Wall(),
                Point(10, 2): Wall(),
                Point(11, 2): Wall(),
                Point(12, 2): Wall(),
                Point(14, 2): Wall(),
                # row 3
                Point(0, 3): Wall(),
                Point(6, 3): Wall(),
                Point(8, 3): Wall(),
                Point(12, 3): Wall(),
                Point(14, 3): Wall(),
                # row 4
                Point(0, 4): Wall(),
                Point(2, 4): Wall(),
                Point(3, 4): Wall(),
                Point(4, 4): Wall(),
                Point(6, 4): Wall(),
                Point(7, 4): Wall(),
                Point(8, 4): Wall(),
                Point(9, 4): Wall(),
                Point(10, 4): Wall(),
                Point(12, 4): Wall(),
                Point(14, 4): Wall(),
                # row 5
                Point(0, 5): Wall(),
                Point(2, 5): Wall(),
                Point(4, 5): Wall(),
                Point(12, 5): Wall(),
                Point(14, 5): Wall(),
                # row 6
                Point(0, 6): Wall(),
                Point(2, 6): Wall(),
                Point(4, 6): Wall(),
                Point(5, 6): Wall(),
                Point(6, 6): Wall(),
                Point(7, 6): Wall(),
                Point(8, 6): Wall(),
                Point(10, 6): Wall(),
                Point(11, 6): Wall(),
                Point(12, 6): Wall(),
                Point(14, 6): Wall(),
                # row 7
                Point(0, 7): Wall(),
                Point(12, 7): Wall(),
                Point(14, 7): Wall(),
                # row 8
                Point(0, 8): Wall(),
                Point(1, 8): Wall(),
                Point(2, 8): Wall(),
                Point(4, 8): Wall(),
                Point(6, 8): Wall(),
                Point(7, 8): Wall(),
                Point(8, 8): Wall(),
                Point(9, 8): Wall(),
                Point(10, 8): Wall(),
                Point(12, 8): Wall(),
                Point(14, 8): Wall(),
                # row 9
                Point(0, 9): Wall(),
                Point(4, 9): Wall(),
                Point(10, 9): Wall(),
                Point(12, 9): Wall(),
                Point(14, 9): Wall(),
                # row 10
                Point(0, 10): Wall(),
                Point(2, 10): Wall(),
                Point(4, 10): Wall(),
                Point(6, 10): Wall(),
                Point(7, 10): Wall(),
                Point(8, 10): Wall(),
                Point(10, 10): Wall(),
                Point(12, 10): Wall(),
                Point(14, 10): Wall(),
                # row 11
                Point(0, 11): Wall(),
                Point(6, 11): Wall(),
                Point(10, 11): Wall(),
                Point(12, 11): Wall(),
                Point(14, 11): Wall(),
                # row 12
                Point(0, 12): Wall(),
                Point(2, 12): Wall(),
                Point(3, 12): Wall(),
                Point(4, 12): Wall(),
                Point(6, 12): Wall(),
                Point(8, 12): Wall(),
                Point(10, 12): Wall(),
                Point(12, 12): Wall(),
                Point(14, 12): Wall(),
                # row 13
                Point(0, 13): Wall(),
                Point(4, 13): Wall(),
                Point(10, 13): Wall(),
                Point(14, 13): Wall(),
                # row 14
                Point(0, 14): Wall(),
                Point(1, 14): Wall(),
                Point(2, 14): Wall(),
                Point(3, 14): Wall(),
                Point(4, 14): Wall(),
                Point(5, 14): Wall(),
                Point(6, 14): Wall(),
                Point(7, 14): Wall(),
                Point(8, 14): Wall(),
                Point(9, 14): Wall(),
                Point(10, 14): Wall(),
                Point(11, 14): Wall(),
                Point(12, 14): Wall(),
                Point(13, 14): Wall(),
                Point(14, 14): Wall(),
            },
            15,
            15,
        ),
        Point(1, 13),
    )

    assert parse(input1) == expected


def test_part1() -> None:
    expected = 7036

    assert part1(input1) == expected

    expected = 11048

    assert part1(input2) == expected


def test_part1_reddit() -> None:
    # https://www.reddit.com/r/adventofcode/comments/1hfhgl1/2024_day_16_part_1_alternate_test_case/
    input = """
###########################
#######################..E#
######################..#.#
#####################..##.#
####################..###.#
###################..##...#
##################..###.###
#################..####...#
################..#######.#
###############..##.......#
##############..###.#######
#############..####.......#
############..###########.#
###########..##...........#
##########..###.###########
#########..####...........#
########..###############.#
#######..##...............#
######..###.###############
#####..####...............#
####..###################.#
###..##...................#
##..###.###################
#..####...................#
#.#######################.#
#S........................#
###########################
"""
    expected = 21148

    assert part1(input) == expected