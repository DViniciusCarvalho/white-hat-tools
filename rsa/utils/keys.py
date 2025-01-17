import random

from .validations import numbers_are_coprimes


def generate_public_key(phi_n: int) -> int:
    while True:
        public_key = random.randint(1, phi_n - 1)
        if numbers_are_coprimes(public_key, phi_n):
            return public_key
        continue


def generate_private_key(phi_n: int, e: int) -> int:
    private_key = pow(e, -1, phi_n)
    return private_key