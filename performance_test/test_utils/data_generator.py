import string
from random import choice


def generate_random_str(length: int = 32):
    return ''.join([choice(string.digits + string.ascii_letters + ' ') for __ in range(length)])
