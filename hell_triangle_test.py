"""Tests for hell_triangle."""

import hell_triangle as ht

TRI_1 = (
    (6,),
    (3, 5),
    (9, 7, 1),
    (4, 6, 8, 4),
)

TRI_2 = (
    (1,),
    (1, 9),
    (1, 1, 9),
    (1, 1, 1, 9),
    (1, 1, 1, 1, 9),
    (100, 1, 1, 1, 1, 9),
)

TRI_3 = (
    (1,),
    (9, 1),
    (9, 1, 1),
    (9, 1, 1, 1),
    (9, 1, 1, 1, 1),
    (9, 1, 1, 1, 1, 100),
)


def test_split():
    left, right = ht.split(TRI_1)
    assert left == ((3,), (9, 7), (4, 6, 8))
    assert right == ((5,), (7, 1), (6, 8, 4))


def test_max_path():
    assert ht.max_path(TRI_1) == 26
    assert ht.max_path(TRI_2) == 105
    assert ht.max_path(TRI_3) == 105


def test_max_path_cached():
    assert ht.max_path_cached(TRI_1) == 26
    assert ht.max_path_cached(TRI_2) == 105
    assert ht.max_path_cached(TRI_3) == 105


def test_max_path_iterative():
    assert ht.max_path_iterative(TRI_1) == 26
    assert ht.max_path_iterative(TRI_2) == 105
    assert ht.max_path_iterative(TRI_3) == 105
