def calculate_encrypted_code(charactere_unicode: int, public: int, n: int) -> int:
    cipher_code = pow(charactere_unicode, public, n)
    return cipher_code


def calculate_decrypted_code(charactere_unicode: int, private: int, n: int) -> int:
    plain_code = pow(charactere_unicode, private, n)
    return plain_code


def convert_to_unicode(cipher_code: int) -> str:
    unicode_char = chr(cipher_code)
    return unicode_char