from pathlib import Path
import sys

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from utils.charenconde import calculate_encrypted_code, convert_to_unicode
from utils.keys import generate_private_key, generate_public_key
from utils.primes import generate_random_prime
from utils.reading import read_text
from utils.totient import calculate_totient_euler
from utils.writers import write_plain_text, write_cipher_text, write_the_primes_product
from utils.writers import write_the_public_key, write_the_private_key


SHELL_LIST = sys.argv

def help():
    print("\nencrypt [FILE_TO_ENCRYPT]\n")
    print("Obs.: You must to be in the same directory of the file.")
    sys.exit()


def encrypt(plain_text: str, p: int, q: int, public: int) -> str:
    semiprime = p * q
    cipher_text = ""
    for charactere in plain_text:
        charactere_unicode = ord(charactere)
        encrypted_charactere_code = calculate_encrypted_code(charactere_unicode, public, semiprime)
        unicode_char = convert_to_unicode(encrypted_charactere_code)
        cipher_text += unicode_char
    return cipher_text


def main(file: str):
    # { p E N | p > 1 }
    p = generate_random_prime(34, 636)

    # { q E N | q > 1 }
    q = generate_random_prime(74, 264)

    # semiprime -> p * q
    write_the_primes_product(p, q)

    # φ(p * q) = φ(p) * φ(q) = (p - 1) * (q - 1)
    phi_n = calculate_totient_euler(p, q)

    public_key = generate_public_key(phi_n)
    write_the_public_key(public_key)

    private_key = generate_private_key(phi_n, public_key)
    write_the_private_key(private_key)

    text = read_text(file)
    write_plain_text(text, file)

    encrypted_text = encrypt(text, p, q, public_key)
    write_cipher_text(encrypted_text, file)

if len(SHELL_LIST) <= 2 and not "--help" in SHELL_LIST:
    main(SHELL_LIST[1])
elif "--help" in SHELL_LIST:
    help()
else:
    print("Just the file to encrypt is accepted")