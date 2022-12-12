from aoc2022_d7_python.day7 import (
    Directory,
    calculate_total_size,
    find_biggest_directory,
    input_build_tree,
    parse_input,
)

test_input = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip()


def test_parse_input() -> None:
    expected = (
        ("$ cd /", ()),
        ("$ ls", ("dir a", "14848514 b.txt", "8504156 c.dat", "dir d")),
        ("$ cd a", ()),
        ("$ ls", ("dir e", "29116 f", "2557 g", "62596 h.lst")),
        ("$ cd e", ()),
        ("$ ls", ("584 i",)),
        ("$ cd ..", ()),
        ("$ cd ..", ()),
        ("$ cd d", ()),
        ("$ ls", ("4060174 j", "8033020 d.log", "5626152 d.ext", "7214296 k")),
    )

    assert expected == parse_input(test_input)


def test_input_build_tree() -> None:
    expected = {
        "/": Directory(
            children=("/a", "/d"),
            size=48381165,
        ),
        "/a": Directory(children=("/a/e",), size=94853),
        "/d": Directory(children=(), size=24933642),
        "/a/e": Directory(children=(), size=584),
    }

    assert expected == input_build_tree(parse_input(test_input))


def test_step_1() -> None:
    assert 95437 == calculate_total_size(test_input)


def test_step2() -> None:
    assert 24933642 == find_biggest_directory(test_input)
