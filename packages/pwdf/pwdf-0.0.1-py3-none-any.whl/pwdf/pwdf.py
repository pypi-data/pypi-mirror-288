from sys import argv
from os import path


USAGE_MESSAGE = "Usage: pwdf <file>"


def run():
    if len(argv) != 2:
        print(USAGE_MESSAGE)
        return

    file_path = argv[1]
    if not path.isfile(file_path):
        print("ERROR: The file specified could not be found.")
        print(USAGE_MESSAGE)
        return

    abs_path = path.abspath(file_path)
    print(abs_path)
