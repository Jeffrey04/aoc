from aoc2024_d15_python.day15 import (
    Board,
    Box,
    Point,
    Robot,
    Symbol,
    Wall,
    double_board,
    get_coordinate,
    move_to_vector,
    parse,
    part1,
    part2,
    robot_instruct,
    robot_push,
    visualize,
)

input_small = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""


input_large = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


def test_parse() -> None:
    expected = (
        Board(
            Robot(2, 2),
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
                # row 1
                Point(0, 1): Wall(),
                Point(3, 1): Box(),
                Point(5, 1): Box(),
                Point(7, 1): Wall(),
                # row 2
                Point(0, 2): Wall(),
                Point(1, 2): Wall(),
                Point(4, 2): Box(),
                Point(7, 2): Wall(),
                # row 3
                Point(0, 3): Wall(),
                Point(4, 3): Box(),
                Point(7, 3): Wall(),
                # row 4
                Point(0, 4): Wall(),
                Point(2, 4): Wall(),
                Point(4, 4): Box(),
                Point(7, 4): Wall(),
                # row 5
                Point(0, 5): Wall(),
                Point(4, 5): Box(),
                Point(7, 5): Wall(),
                # row 6
                Point(0, 6): Wall(),
                Point(7, 6): Wall(),
                # row 7
                Point(0, 7): Wall(),
                Point(1, 7): Wall(),
                Point(2, 7): Wall(),
                Point(3, 7): Wall(),
                Point(4, 7): Wall(),
                Point(5, 7): Wall(),
                Point(6, 7): Wall(),
                Point(7, 7): Wall(),
            },
            8,
            8,
        ),
        (
            Symbol.Left,
            Symbol.Up,
            Symbol.Up,
            Symbol.Right,
            Symbol.Right,
            Symbol.Right,
            Symbol.Down,
            Symbol.Down,
            Symbol.Left,
            Symbol.Down,
            Symbol.Right,
            Symbol.Right,
            Symbol.Down,
            Symbol.Left,
            Symbol.Left,
        ),
    )

    assert parse(input_small) == expected


def test_push() -> None:
    board, _ = parse(input_small)

    vector = move_to_vector(Symbol.Left)
    expected = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Up)
    expected = """
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Up)
    expected = """
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Right)
    expected = """
########
#..@OO.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Right)
    expected = """
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Right)
    expected = """
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Down)
    expected = """
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Left)
    expected = """
########
#....OO#
##.@...#
#...O..#
#.#.O..#
#...O..#
#...O..#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Down)
    expected = """
########
#....OO#
##.....#
#..@O..#
#.#.O..#
#...O..#
#...O..#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Right)
    expected = """
########
#....OO#
##.....#
#...@O.#
#.#.O..#
#...O..#
#...O..#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Right)
    expected = """
########
#....OO#
##.....#
#....@O#
#.#.O..#
#...O..#
#...O..#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Down)
    expected = """
########
#....OO#
##.....#
#.....O#
#.#.O@.#
#...O..#
#...O..#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Left)
    expected = """
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Left)
    expected = """
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected


def test_robot_instruct() -> None:
    board, moves = parse(input_small)
    expected = """
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########
""".strip()

    assert visualize(robot_instruct(board, moves)) == expected

    board, moves = parse(input_large)
    expected = """
##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########
""".strip()

    assert visualize(robot_instruct(board, moves)) == expected


def test_get_coordinate() -> None:
    input = Point(4, 1)
    expected = 104

    assert get_coordinate(input) == expected


def test_part1() -> None:
    expected = 2028

    assert part1(input_small) == expected

    expected = 10092

    assert part1(input_large) == expected


def test_double_board() -> None:
    board, _ = parse(input_large, double_board)
    expected = """
####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################
""".strip()

    assert visualize(board) == expected


def test_push_double() -> None:
    board, _ = parse(
        """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""".strip(),
        double_board,
    )

    expected = """
##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############
""".strip()
    assert visualize(board) == expected

    vector = move_to_vector(Symbol.Left)
    expected = """
##############
##......##..##
##..........##
##...[][]@..##
##....[]....##
##..........##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Down)
    expected = """
##############
##......##..##
##..........##
##...[][]...##
##....[].@..##
##..........##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Down)
    expected = """
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.......@..##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Left)
    expected = """
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##......@...##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Left)
    expected = """
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.....@....##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Up)
    expected = """
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Up)
    expected = """
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Left)
    expected = """
##############
##......##..##
##...[][]...##
##....[]....##
##....@.....##
##..........##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Left)
    expected = """
##############
##......##..##
##...[][]...##
##....[]....##
##...@......##
##..........##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Up)
    expected = """
##############
##......##..##
##...[][]...##
##...@[]....##
##..........##
##..........##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected

    vector = move_to_vector(Symbol.Up)
    expected = """
##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############
""".strip()

    assert visualize((board := robot_push(board, vector))) == expected


def test_robot_instruct_double() -> None:
    expected = """
####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..@......[].[][]##
##......[][]..[]..##
####################
""".strip()
    assert visualize(robot_instruct(*parse(input_large, double_board))) == expected


def test_part2() -> None:
    expected = 9021
    assert part2(input_large) == expected
