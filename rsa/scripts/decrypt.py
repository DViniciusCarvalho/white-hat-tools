from pathlib import Path
import sys

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from utils.charenconde import calculate_decrypted_code, convert_to_unicode
from utils.reading import read_text, read_equation_element
from utils.writers import write_plain_text


SHELL_LIST = sys.argv

def help():
    print("\ndecrypt [FILE_TO_DECRYPT]\n")
    print("Obs.: You must to be in the same directory of the file.")
    sys.exit()


def decrypt(cipher_text: str, private: int, semiprime: int) -> str:
    plain_text = ""
    for charactere in cipher_text:
        charactere_unicode = ord(charactere)
        encrypted_charactere_code = calculate_decrypted_code(charactere_unicode, private, semiprime)
        unicode_char = convert_to_unicode(encrypted_charactere_code)  
        plain_text += unicode_char
    return plain_text


def get_private_key() -> int:
    private_key = read_equation_element("keys", "private.key")
    return private_key


def get_primes_product() -> int:
    semiprime_product = read_equation_element("semiprime", "product.txt")
    return semiprime_product
    

def get_cipher_text(file: str) -> str:
    cipher_text = read_text(file)
    return cipher_text


def main(file: str) -> None:
    cipher_text = get_cipher_text(file)
    private_key = get_private_key()
    semiprime = get_primes_product()
    decrypted_text = decrypt(cipher_text, private_key, semiprime)
    write_plain_text(decrypted_text, file)


if len(SHELL_LIST) <= 2 and not "--help" in SHELL_LIST:
    main(SHELL_LIST[1])
elif "--help" in SHELL_LIST:
    help()
else:
    print("Just the file to decrypt is accepted")