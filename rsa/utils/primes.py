import random

def generate_random_prime(start: int, end: int) -> int:
    prime_number = None
    while True:
        is_prime = True
        random_number = random.randint(start, end)
        for antecessor in range(2, random_number):
            if random_number % antecessor == 0:
                is_prime = False
                break
        if is_prime:
            prime_number = random_number
            break
    return prime_number