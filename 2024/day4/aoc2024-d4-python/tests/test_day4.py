from aoc2024_d4_python.day4 import (
    count_goal,
    find_e2w,
    find_n2s,
    find_ne2sw,
    find_nw2se,
    find_s2n,
    find_se2nw,
    find_start,
    find_sw2ne,
    find_w2e,
)


def test_find_w2e() -> None:
    input = (
        0,
        0,
        ("XMAS",),
    )
    expected = True

    assert find_w2e(*input) == expected

    input = (
        0,
        0,
        ("XMA",),
    )
    expected = False

    assert find_w2e(*input) == expected


def test_find_n2s() -> None:
    input = (
        0,
        0,
        ("X", "M", "A", "S"),
    )
    expected = True

    assert find_n2s(*input) == expected


def test_find_s2n() -> None:
    input = (
        0,
        3,
        ("S", "A", "M", "X"),
    )
    expected = True

    assert find_s2n(*input) == expected


def test_find_e2w() -> None:
    input = (
        3,
        0,
        ("SAMX",),
    )
    expected = True

    assert find_e2w(*input) == expected

    input = (
        2,
        0,
        ("AMX",),
    )
    expected = False

    assert find_e2w(*input) == expected


def test_find_nw2se() -> None:
    input = (
        0,
        0,
        ("X...", ".M..", "..A.", "...S"),
    )
    expected = True

    assert find_nw2se(*input) == expected


def test_find_se2nw() -> None:
    input = (
        3,
        3,
        ("S...", ".A..", "..M.", "...X"),
    )
    expected = True

    assert find_se2nw(*input) == expected

    input = (
        1,
        9,
        tuple(
            """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".strip().splitlines()
        ),
    )
    expected = False

    assert find_se2nw(*input) == expected


def test_find_ne2sw() -> None:
    input = (
        3,
        0,
        ("...X", "..M.", ".A..", "S..."),
    )
    expected = True

    assert find_ne2sw(*input) == expected


def test_find_sw2ne() -> None:
    input = (
        0,
        3,
        ("...S", "..A.", ".M..", "X..."),
    )
    expected = True

    assert find_sw2ne(*input) == expected


def test_find_start() -> None:
    input = """
..X...
.SAMX.
.A..A.
XMAS.S
.X....
"""
    expected = (
        (2, 0),
        (4, 1),
        (0, 3),
        (1, 4),
    )

    assert find_start(tuple(input.strip().splitlines())) == expected


def test_count():
    input = """
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
"""
    expected = 18

    assert count_goal(tuple(input.strip().splitlines())) == expected

    input = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
    expected = 18

    assert count_goal(tuple(input.strip().splitlines())) == expected
