def read_fromlist(value, lst):
    if value.lower() not in lst:
        raise ValueError(value + " is not in list: " + str(lst))
    return value.lower()
