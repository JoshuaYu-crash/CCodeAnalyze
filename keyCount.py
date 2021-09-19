from sys import argv
import os
import re
from dfa import DFA

keysList = ["auto", "break", "case", "char", "const", "continue",
            "default", "do", "double", "else", "enum", "extern", "float",
            "for", "goto", "if", "int", "long", "register", "return",
            "short", "signed", "sizeof", "static", "struct", "switch",
            "typedef", "union", "unsigned", "void", "volatile", "while"]

# count for if-else and if-else if-else
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
            code += i.strip() + ' '
    # remove keys in string
    code = re.sub("\"[^\"]*\"", "__STRING__", code)
    # remove keys in annotation /* ~~ */
    code = re.sub("/\*[\s\S]*\*/", "", code)
    return " " + code


# find the pos of } by given {'s pos
def findRightIndex(startIndex, endIndex, str):
    stack = []
    ans = startIndex
    for i in range(startIndex, endIndex):
        if str[i] == "{":
            stack.append(str[i])
        elif str[i] == "}":
            if len(stack) > 1:
                stack.pop()
            else:
                ans = i
                break
        else:
            pass
    return ans


# hand code by level
def codeHandler(code, level):
    ansList = []
    if level >= 1:
        ansList.append(countKeys(code))
    if level >= 2:
        ansList.append(countSwitch(code))
    if level >= 3:
        # exchange else if to elseif
        code = re.sub("else\s+if", "elseif", code)
        # exchange else{ to else {
        code = re.sub("else{", "else {", code)
        matchCode(code)
        ansList.append(ie)
    if level >= 4:
        ansList.append(iei)
    output(ansList)
    pass


# level 1 count keys, by DFA
def countKeys(code):
    dfa = DFA(keysList)
    # for i in dfa.match(code):
    #     print(i)
    return len(dfa.match(code))


# level 1 count keys, by re
def countKeysByRE(code):
    sum = 0
    for i in keysList:
        temp = len(re.findall("[^0-9a-zA-Z\_]" + i + "[^0-9a-zA-Z\_]", code))
        sum +=temp
    return sum


# level 2 count switch and case
def countSwitch(code):
    switchList = re.finditer("[ };]switch\([^)]*\)\s*{", code)
    switchNum = 0
    caseNumList = []
    for switch in switchList:
        switchNum += 1
        leftIndex = switch.end()
        rightIndex = findRightIndex(leftIndex-1, len(code), code)
        caseList = re.findall("case", code[leftIndex:rightIndex])
        caseNumList.append(len(caseList))
    return [switchNum, caseNumList]


# level 3 and 4 match if-else and if-else if-else
# match code block, keep matching the next if
def matchCode(code):
    lpos = 0
    codeLen = len(code)
    while True:
        if lpos >= codeLen or re.search("[ ;}]if\s*\([^)]*\)", code[lpos:]) is None:
            break
        lpos = matchIf(code[lpos:]) + lpos
    return ie, iei


# need match if block and return right block position
def matchIf(code):
    ifObj = re.search("[ ;}]if\s*\([^)]*\)", code)
    if ifObj:
        # if()
        #     ^
        lpos = ifObj.end()

        ifElseIf = False
        ifElse = False
        global ie
        global iei

        # find rpos
        if re.search("^\s*if\s*\([^)]*\)", code[lpos:]):
            rpos = matchIf(code[lpos:]) + lpos

        elif re.search("^\s*{", code[lpos:]):
            lpos = re.search("^\s*{", code[lpos:]).end() + lpos
            rpos = findRightIndex(lpos - 1, len(code), code)
            ifBody = code[lpos:rpos]
            matchCode(ifBody)

        # with no {}, end with ;
        else:
            rpos = re.search(";", code[lpos:]).end() + lpos - 1
            ifBody = code[lpos:rpos]

        # 1.match else if
        if re.search("^\s*elseif\s*\([^)]*\)", code[rpos + 1:]):
            ifElseIf = True
            rpos += matchElseIf(code[rpos + 1:]) + 1

        # 2.match else
        if re.search("^\s*else[^0-9a-zA-Z_]", code[rpos + 1:]):
            ifElse = True
            rpos += matchElse(code[rpos + 1:]) + 1

        # judge status
        if ifElse and not ifElseIf:
            ie += 1
        if ifElseIf and ifElse:
            iei += 1
        return rpos


# match else-if block and return right position
def matchElseIf(code):
    elseIfObj = re.search("^\s*elseif\s*\([^)]*\)", code)
    if elseIfObj:
        # elseif()
        #         ^
        lpos = elseIfObj.end()
        # search else-if body
        # with no {}, match if
        if re.search("^\s*if\s*\([^)]*\)", code[lpos:]):
            rpos = matchIf(code[lpos:]) + lpos
            return rpos

        # match {}
        elif re.search("^\s*{", code[lpos:]):
            lpos = re.search("^\s*{", code[lpos:]).end() + lpos
            rpos = findRightIndex(lpos - 1, len(code), code)
            elseIfBody = code[lpos:rpos]
            matchCode(elseIfBody)
            if re.search("^\s*elseif\s*\([^)]*\)", code[rpos + 1:]):
                rpos += matchElseIf(code[rpos + 1:]) + 1
                return rpos
            else:
                return rpos
        # with no {}, match ;
        else:
            rpos = re.search(";", code[lpos:]).end() + lpos - 1
            elseIfBody = code[lpos:rpos]
            if re.search("^\s*elseif\s*\([^)]*\)", code[rpos + 1:]):
                rpos += matchElseIf(code[rpos + 1:]) + 1
                return rpos
            else:
                return rpos


# match else block and return right position
def matchElse(code):
    elseObj = re.search("^\s*else[^0-9a-zA-Z_]", code)
    if elseObj:
        # else
        #     ^
        lpos = elseObj.end()

        if re.search("^\s*if\s*\([^)]*\)", code[lpos:]):
            print("if")

        # match {}
        elif re.search("^\s*{", code[lpos:]):
            lpos = re.search("^\s*{", code[lpos:]).end() + lpos
            rpos = findRightIndex(lpos - 1, len(code), code)
            elseBody = code[lpos:rpos]
            matchCode(elseBody)
            return rpos

        # with no {}, match ;
        else:
            rpos = re.search(";", code[lpos:]).end() + lpos - 1
            elseIfBody = code[lpos:rpos]
            return rpos


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


# run code
def run():
    path, level = argparse()
    code = readfile(path)
    codeHandler(code, level)


# performance test
def performanceTest(path, time):
    for i in range(0, time):
        global ie
        global iei
        ie = 0
        iei = 0
        level = 4
        code = readfile(path)
        codeHandler(code, level)


# main func
if __name__ == '__main__':
    # performanceTest("./data/key.c", 10000)
    run()
    pass
