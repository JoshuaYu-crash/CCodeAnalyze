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


def findRightIndex(startIndex, endIndex, str):
    stack = []
    ans = startIndex
    for i in range(startIndex, endIndex):
        if str[i] == "{":
            stack.append("i")
        elif str[i] == "}":
            if len(stack) != 0:
                stack.pop()
            else:
                ans = i
                break
        else:
            pass
    return ans


# codeHandler
def codeHandler(code, level):
    ansList = []
    if level >= 1:
        ansList.append(countKeys(code))
    if level >= 2:
        ansList.append(countSwitch(code))

    output(ansList)
    pass


# level 1 count keys
def countKeys(code):
    dfa = DFA(keysList)
    for i in dfa.match(code):
        print(i)
    return len(dfa.match(code))


# level 2 count switch and case
def countSwitch(code):
    switchList = re.finditer("[ };]switch\([^\)]*\)\s*{", code)
    switchNum = 0
    caseNumList = []
    for switch in switchList:
        switchNum+=1
        leftIndex = switch.end()
        rightIndex = findRightIndex(leftIndex, len(code), code)
        caseList = re.findall("case", code[leftIndex:rightIndex])
        caseNumList.append(len(caseList))
    return [switchNum, caseNumList]


# output ans
def output(ansList):
    if len(ansList) >= 1:
        print("total num: ", ansList[0])
    if len((ansList)) >= 2:
        print("switch num:", ansList[1][0])
        print("case num:", " ".join([str(i) for i in ansList[1][1]]))
    pass


if __name__ == '__main__':
    path, level = argparse()
    code = readfile(path)
    print(code)
    codeHandler(code, level)
    pass
