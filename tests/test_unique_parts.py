from explore_nwps.unique_parts import unique_parts


def test_unique_parts_different_lengths():
    unique = unique_parts(["foo/a1.b1", "foo/a2.b2.txt"])
    assert len(unique) == 3
    assert unique[0] == ["a1", "a2"]
    assert unique[1] == ["b1", "b2"]
    assert unique[2] == ["txt"]
