from itertools import groupby


def is_chain(it):
    start = it[0]
    for expected, (key, group) in enumerate(groupby(it), start):
        group = list(group)
        print(expected, key, group)
        if key != expected:
            return False
        if len(group) != 2:
            return False
    return True
l = [15,15,16,16,17,17,20,20,19,19]
print(is_chain(l))


