from math import ceil
from sys import argv, exit
from typing import Union


def report_file_not_found_error():
    print("File not found. Please ensure that the file path is correct.")
    exit()


def report_i_flag_wrong():
    print("The \"-i\" flag must be followed by the line size, which must be specified as an integer.")
    exit()


def help():
    print("\nbyread [path/to/file] [-i] [line_length]\n")
    print("    -i   Specifies the line_length, the interval (default = 16)\n")
    exit()


def args_contains(argument: str, argument_list: list[str]) -> bool:
    if argument in argument_list:
        return True
    return False


def get_file_bytes(argument_list: list[str]) -> Union[bytes, None]:
    file_path = argument_list[1]
    try:
        with open(file_path, "rb") as binary_file:
            content = binary_file.read()
            return content
    except FileNotFoundError:
        report_file_not_found_error()


def get_hex_list(file_bytes: bytes) -> list[str]:
    hex_list = []
    for byte in file_bytes:
        hex_value = hex(byte)[2:].zfill(2)
        hex_list.append(hex_value)
    return hex_list

def get_line_length(argument_list: list[str]) -> int:
    flag_index = argument_list.index("-i")
    try:
        line_length = int(argument_list[flag_index + 1])
        return line_length
    except ValueError:
        report_i_flag_wrong()


def get_hex_offset(coeficient: int, line_length) -> str:
    hex_offset = "{:X}".format(coeficient * line_length)
    filled_offset = hex_offset.zfill(8)
    return filled_offset


def get_ascii_format(line: list[str], line_length: int) -> str:
    ascii_list = []
    for hex_string in line:
        try:
            int_value = int(hex_string, 16)
            ascii_char = chr(int_value)
            ascii_list.append(ascii_char)
        except ValueError:
            ascii_list.append(".")
        
    concatenated_ascii = concat_ascii_chars(ascii_list, line_length)   
    return concatenated_ascii


def concat_ascii_chars(ascii_list: list[str], line_length: int) -> str:
    if len(ascii_list) < line_length:
        ascii_list = fill_line(ascii_list, line_length, ".")
    return f"|{''.join(ascii_list)}|"


def fill_line(line: list[str], line_length: int, fill: str) -> str:
    for i in range(line_length - len(line)):
        line.append(fill)
    return line


def concat_line(line: list[str], line_length: int) -> str:
    if len(line) < line_length:
        line = fill_line(line, line_length, "  ")
    return " ".join(line)


def get_lines_array(file_hex_bytes: list[str], line_length=26) -> list[str]:
    file_hex_bytes_length = len(file_hex_bytes)
    lines_number = ceil(file_hex_bytes_length / line_length)
    lines = []

    if file_hex_bytes_length <= line_length:
        offset = get_hex_offset(0, line_length)
        organized_bytes = concat_line(file_hex_bytes, line_length)
        lines.append(f"{offset}  {organized_bytes}")
    else:
        for i in range(lines_number):
            line = []

            for k in range(line_length):
                index = i * line_length + k
                if file_hex_bytes_length > index:
                    line.append(file_hex_bytes[index].zfill(2))
    
            offset = get_hex_offset(i, line_length)
            organized_bytes = concat_line(line, line_length)
            ascii_format = get_ascii_format(line, line_length)
            lines.append(f"{offset}  {organized_bytes}  {ascii_format}")

    return lines
        

def show_lines(lines_list: list[str]):
    for line in lines_list:
        print(line)


def main():
    argument_list = argv

    if args_contains("--help", argument_list):
        help()

    file_bytes = get_file_bytes(argument_list)
    file_hex_bytes_list = get_hex_list(file_bytes)

    if args_contains("-i", argument_list):
        line_length = get_line_length(argument_list)
        lines_list = get_lines_array(file_hex_bytes_list, line_length)
        show_lines(lines_list)

    else:
        lines_list = get_lines_array(file_hex_bytes_list)
        show_lines(lines_list)


if __name__ == "__main__":
    main()