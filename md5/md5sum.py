from hashlib import md5
from sys import argv

def md5sum(filename):
    md5_hash = md5()
    with open(filename, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

if __name__ == "__main__":
    file_path = argv[1]
    hash_value = md5sum(file_path)
    print(hash_value)