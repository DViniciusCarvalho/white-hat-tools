import os


current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.join(current_dir, "..")

def write_the_primes_product(p: int, q: int) -> None:
    product = p * q
    file_path = f"{parent_dir}{os.sep}semiprime{os.sep}product.txt"
    with open(file_path, "w") as product_file:
        product_file.write(str(product))


def write_the_public_key(public_key: int) -> None:
    file_path = f"{parent_dir}{os.sep}keys{os.sep}public.key"
    with open(file_path, "w") as public:
        public.write(str(public_key))


def write_the_private_key(private_key: int) -> None:
    file_path = f"{parent_dir}{os.sep}keys{os.sep}private.key"
    with open(file_path, "w", encoding="utf-8") as private:
        private.write(str(private_key))


def write_plain_text(plain: str, file: str) -> None:
    file_path_plain_text = os.path.abspath(file)
    file_path_plain_text_copy = f"{parent_dir}{os.sep}copy{os.sep}plain.txt"
    with open(file_path_plain_text, "w", encoding="utf-8") as plain_text:
        plain_text.write(plain)
    with open(file_path_plain_text_copy, "w", encoding="utf-8") as plain_text_copy:
        plain_text_copy.write(plain)


def write_cipher_text(cipher: str, file: str) -> None:
    file_path_cipher_text = os.path.abspath(file)
    file_path_cipher_text_copy = f"{parent_dir}{os.sep}copy{os.sep}cipher.txt"
    with open(file_path_cipher_text, "w", encoding="utf-8") as cipher_text:
        cipher_text.write(cipher)
    with open(file_path_cipher_text_copy, "w", encoding="utf-8") as cipher_text_copy:
        cipher_text_copy.write(cipher)