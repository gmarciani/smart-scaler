def pprint_qtable(qtable):
    """
    Return the pretty string representation of a QTable.
    :param qtable: (object) the QTable.
    :return: (string) the pretty string representation of a QTable.
    """
    return pprint_2d_matrix(from_qtable_to_matrix(qtable))


def pprint_2d_matrix(matrix):
    """
    Return the pretty string representation of a 2D matrix.
    :param q_table: (object) the 2D matrix.
    :return: (string) the pretty string representation of a 2D matrix.
    """
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = "\t".join("{{:{}}}".format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return "\n".join(table)


def from_qtable_to_matrix(qtable):
    """
    Convert a QTable into a 2D matrix.
    :param qtable: (object) a QTable.
    :return: (2D matrix) the 2D matrix representation of the QTable.
    """
    states = sorted(set(key[0] for key in qtable))
    actions = sorted(set(key[1] for key in qtable))

    matrix = []

    first_row = [""]
    for a in actions:
        first_row.append(str(a))

    matrix.append(first_row)

    for state in states:
        row = [str(state)]
        for action in actions:
            row.append(qtable[(state,action)])
        matrix.append(row)

    return matrix


if __name__ == "__main__":
    import random

    states = ["A1", "B20", "C300"]
    actions = [1, 20, 300]
    q_table = {}
    for s in states:
        for a in actions:
            q_table[(s, a)] = random.random()

    print(pprint_qtable(q_table))