target in values

##########


def contains_value(target, values):
    result = False
    for value in values:
        if value == target:
            result = True
            break
    return result

