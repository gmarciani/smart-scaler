INFINITE = float("inf")


def get_upper_bound(bounds, value):
    """
    Get the maximum upper bound in bounds for value.
    :param bounds: (list(float)) the list of bounds.
    :param value: (float) the vaue to map.
    :return: (float) the maximum upper bound in bounds for value.
    """
    sorted_bounds = sorted(bounds)

    if value > sorted_bounds[-1]:
        raise KeyError("There is no upper-bound for value {}".format(value))

    upper_bound = INFINITE

    for bound in sorted_bounds:
        if value <= bound < upper_bound:
            upper_bound = bound
    return upper_bound


if __name__ == "__main__":
    bounds = [0.1, 0.2, 0.3, 0.4, 0.5]

    print(get_upper_bound(bounds, 0.1))
