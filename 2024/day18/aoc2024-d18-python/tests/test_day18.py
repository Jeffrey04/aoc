from aoc2024_d18_python.day18 import (
    Point,
    get_corrupted_map,
    parse,
    part1,
    part2,
    visualize,
)

input = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def test_parse() -> None:
    expected = """
...#...
..#..#.
....#..
...#..#
..#..#.
.#..#..
#.#....
""".strip()
    memory = parse(input, Point(6, 6))

    assert visualize(memory, get_corrupted_map(memory, 12)) == expected


def test_part1() -> None:
    expected = 22

    assert part1(input, Point(6, 6), 12) == expected


def test_part2() -> None:
    expected = "6,1"

    assert part2(input, Point(6, 6)) == expected
