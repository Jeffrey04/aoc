from aoc2022_d8_python.day8 import (
    DIRECTION_BOTTOM,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_TOP,
    check_tree_is_visible,
    map_create,
    tree_count_best_score,
    tree_count_distance,
    tree_count_score,
    tree_count_visible,
    tree_list_previous,
)

test_input = """
30373
25512
65332
33549
35390
""".strip()


def test_map_create() -> None:
    assert [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ] == map_create(test_input)


def test_tree_list_previous() -> None:
    tree = map_create(test_input)

    assert [2, 5] == tree_list_previous(tree, 1, 1, DIRECTION_LEFT)
    assert [0, 5] == tree_list_previous(tree, 1, 1, DIRECTION_TOP)
    assert [2, 1, 5, 5] == tree_list_previous(tree, 1, 1, DIRECTION_RIGHT)
    assert [5, 3, 5, 5] == tree_list_previous(tree, 1, 1, DIRECTION_BOTTOM)

    assert [2, 5, 5] == tree_list_previous(tree, 1, 2, DIRECTION_LEFT)
    assert [3, 5] == tree_list_previous(tree, 1, 2, DIRECTION_TOP)
    assert [2, 1, 5] == tree_list_previous(tree, 1, 2, DIRECTION_RIGHT)
    assert [3, 5, 3, 5] == tree_list_previous(tree, 1, 2, DIRECTION_BOTTOM)


def test_tree_is_visible() -> None:
    tree = map_create(test_input)

    assert True == check_tree_is_visible([2, 5])
    assert True == check_tree_is_visible([0, 5])
    assert False == check_tree_is_visible([2, 1, 5, 5])
    assert False == check_tree_is_visible([5, 3, 5, 5])


def test_tree_count_visible() -> None:
    assert 21 == tree_count_visible(test_input)


def test_tree_count_distance() -> None:
    tree = map_create(test_input)

    assert 1 == tree_count_distance([2, 5, 5])
    assert 1 == tree_count_distance([3, 5])
    assert 2 == tree_count_distance([2, 1, 5])
    assert 2 == tree_count_distance([3, 5, 3, 5])


def test_tree_count_score() -> None:
    tree_map = map_create(test_input)

    assert 4 == tree_count_score(tree_map, 1, 2)
    assert 8 == tree_count_score(tree_map, 3, 2)


def test_tree_count_best_score() -> None:
    assert 8 == tree_count_best_score(test_input)
