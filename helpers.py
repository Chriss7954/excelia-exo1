import random


def generate_cookie_value():
    """Return une longueur de 128
    >>> len(generate_cookie_value())
    128
    """
    return str("".join(random.choice("0123456789ABCDEFabcdef@&!") for i in range(128)))


def somme(a, b):
    """Return the somme of 4 + 4 that do 8
    >>> somme(4, 4)
    8
    """
    return int(a) + int(b)
