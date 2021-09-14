from sys import argv
import os


# read args
def argparse():
    path, level = argv[1], int(argv[2])
    if level < 1 or level > 4:
        exit(1)
    return path, level


# read the C source file
def readfile(path):
    # check if file exists
    if not os.path.exists(path):
        print("file not exists!")
        exit(1)
    # openfile and return code
    with open(path, "r") as f:
        code = f.read()
        return code


# codeHandler
def codeHandler(code, level):
    print(code)
    print(level)
    pass


if __name__ == '__main__':
    path, level = argparse()
    code = readfile(path)
    codeHandler(code, level)
    pass
