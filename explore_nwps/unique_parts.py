from typing import Iterable


def unique_parts(filenames: Iterable[str], sep: str = ".") -> list[list[str]]:
    """Returns the unique parts of all filenames. Parts are separated by `sep`.

    For example, consider two filenames, each with three parts:

    >>> unique = unique_parts(["foo/a1.b1.txt", "foo/a2.b2.txt"])
    >>> len(unique)
    3

    >>> unique[0]
    ['a1', 'a2']

    >>> unique[1]
    ['b1', 'b2']

    >>> unique[2]
    ['txt']
    """
    split_filenames = [filename.split("/")[-1] for filename in filenames]
    unique_parts: list[set[str]] = []
    for filename in split_filenames:
        sections = filename.split(sep)
        for i, section in enumerate(sections):
            try:
                s = unique_parts[i]
            except IndexError:
                unique_parts.append(set())
                s = unique_parts[i]
            s.add(section)

    unique_lists: list[list[str]] = []
    for unique_part in unique_parts:
        unique_list = list(unique_part)
        unique_list.sort()
        unique_lists.append(unique_list)

    return unique_lists
