def get_index(values, target):
    result = -1
    for i in range(len(values)):
        if values[i] == target:
            return i
    return result