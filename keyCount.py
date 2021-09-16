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

ie = 0
iei = 0


# read args
def argparse():
    path, level = argv[1], int(argv[2])
    if level < 1 or level > 4:
        exit(1)
    return path, level


# read the C source file and return code
# remove annotation and string
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
            # remove keys in annotation //
            i = re.sub("//.*", "", i)
            # remove start space and end \n
            code += i.strip()+' '
    # remove keys in string
    code = re.sub("\"[^\"]*\"", "__STRING__", code)
    # remove keys in annotation /* ~~ */
    code = re.sub("/\*[\s\S]*\*/", "", code)
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
    if level >= 3:
        matchIf(re.sub("else if", "elseif", code))
        ansList.append(ie)
    if level >= 4:
        ansList.append(iei)
    output(ansList)
    pass


# level 1 count keys
def countKeys(code):
    dfa = DFA(keysList)
    # for i in dfa.match(code):
    #     print(i)
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
    if len(ansList) >= 2:
        print("switch num:", ansList[1][0])
        print("case num:", " ".join([str(i) for i in ansList[1][1]]))
    if len(ansList) >= 3:
        print("if-else num:", ansList[2])
    if len(ansList) >= 4:
        print("if-elseif-else num:", ansList[3])
    pass


# match if-else and if-else if-else
def matchIf(code):
    ifObj = re.search("[ ;}]if\s*\([^\)]*\)\s*{", code)
    if ifObj:
        # init status
        ifElse = False
        ifElseIf = False
        lpos = ifObj.end()
        rpos = findRightIndex(lpos, len(code), code)
        # match if body
        ifBody = code[lpos:rpos]
        matchIf(ifBody)

        # 1.match else if
        if re.search("^\s*elseif\s*\([^\)]*\)\s*{", code[rpos+1:]):
            ifElseIf = True
            rpos += matchElseIf(code[rpos+1:])+1

        # 2.match else
        if re.search("^\s*else\s*{", code[rpos+1:]):
            ifElse = True
            rpos += matchElse(code[rpos+1:])+1

        # judge status
        if ifElse and not ifElseIf:
            global ie
            ie += 1
        if ifElseIf and ifElse:
            global iei
            iei += 1
        matchIf(code[rpos+1:])


# match else
def matchElse(code):
    elseObj = re.search("^\s*else\s*{", code)
    if elseObj:
        lpos = elseObj.end()
        rpos = findRightIndex(lpos, len(code), code)
        elseBody = code[lpos:rpos]
        matchIf(elseBody)
        return rpos


# match else-if
def matchElseIf(code):
    elseIfObj = re.search("^\s*elseif\s*\([^\)]*\)\s*{", code)
    if elseIfObj:
        lpos = elseIfObj.end()
        rpos = findRightIndex(lpos, len(code), code)
        elseIfBody = code[lpos:rpos]
        matchIf(elseIfBody)
        if re.search("^\s*elseif\s*\([^\)]*\)\s*{", code[rpos + 1:]):
            nextRPosLen = matchElseIf(code[rpos+1:])
            rpos += nextRPosLen + 1
            return rpos
        else:
            return rpos
    return 0


if __name__ == '__main__':
    path, level = argparse()
    code = readfile(path)
    codeHandler(code, level)
    pass
