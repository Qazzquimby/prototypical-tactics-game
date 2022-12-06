def read_fromlist(value, lst):
    if not value.lower() in lst:
        raise ValueError(value + " is not in list: " + str(lst))
    return value.lower()
