import os

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.join(current_dir, "..")

def read_text(file: str) -> str:
    file_path = os.path.abspath(file)
    with open(file_path, encoding="utf-8") as text_file:
        return text_file.read()


def read_equation_element(dir: str, file_name: str) -> int:
    file_path = f"{parent_dir}{os.sep}{dir}{os.sep}{file_name}"
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
        return int(file_content)