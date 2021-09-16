from sys import argv
import os
import re
from dfa import DFA


keysList = ["auto", "break", "case", "char", "const", "continue",
            "default", "do", "double", "else", "enum", "extern", "float",
            "for", "goto", "if", "int", "long", "register", "return",
            "short", "signed", "sizeof", "static", "struct", "switch",
            "typedef", "union", "unsigned", "void", "volatile", "while"]

targetsList = ["if", "else", "ifelse", "switch"]


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

    code = ""
    # openfile and return code
    with open(path, "r") as f:
        codeList = f.readlines()
    for i in codeList:
        if not re.match("^\s*#include", i):
            code += i.strip()+' '  # remove start space and end \n
    # code = re.sub("else if", "elseif", code)
    code = re.sub("\"[^\"]*\"", "__STRING__", code)
    return code


# codeHandler
def codeHandler(code, level):
    ansList = []
    if level >= 1:
        ansList.append(countKeys(code))

    output(ansList)
    pass


def countKeys(code):
    dfa = DFA(keysList)
    for i in dfa.match(code):
        print(i)
    return len(dfa.match(code))


# output ans
def output(ansList):
    if len(ansList) >= 1:
        print("total num: ", ansList[0])
    pass


if __name__ == '__main__':
    path, level = argparse()
    code = readfile(path)
    print(code)
    codeHandler(code, level)
    pass
