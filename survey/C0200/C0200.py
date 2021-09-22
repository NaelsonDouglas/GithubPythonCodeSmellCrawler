def get_index(target, values):
    for i in range(len(values)):
        if values[i] == target:
            return i
    return -1


def get_index(target, values):
    for i, value in enumerate(values):
        if value == target:
            return i
    return -1