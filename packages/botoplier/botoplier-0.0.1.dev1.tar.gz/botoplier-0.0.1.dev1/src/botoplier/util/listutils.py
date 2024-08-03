# From https://stackoverflow.com/a/2158532
# Cristian, CC-BY-SA 3.0
def flatten_generator(lst):
    for el in lst:
        if isinstance(el, list):
            yield from flatten_generator(el)
        else:
            yield el


def flatten(lst: list):
    return list(flatten_generator(lst))
