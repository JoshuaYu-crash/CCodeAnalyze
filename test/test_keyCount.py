import unittest
from keyCount import *


class MyTestCase(unittest.TestCase):
    def test_readfile(self):
        filepath = "./test_read.c"
        ans = "int main() { printf(__STRING__); }"
        self.assertEqual(readfile(filepath).strip(), ans)


    def test_findRightIndex(self):
        str1 = "{{{}}}"
        str2 = "{{}{}{}}"
        str3 = "{123321{}  {}{{}}123321}"
        ans1 = 4
        ans2 = 2
        ans3 = 23
        self.assertEqual(findRightIndex(1, len(str1), str1), ans1)
        self.assertEqual(findRightIndex(1, len(str2), str2), ans2)
        self.assertEqual(findRightIndex(0, len(str3), str3), ans3)


    def test_countKeys(self):
        code = readfile("./test_matchCode.c")
        self.assertEqual(countKeysByRE(code), 53)


    def test_countSwitch(self):
        code = readfile("./test_matchCode.c")
        self.assertEqual(countSwitch(code), [2, [3, 2]])

    def test_matchIf(self):
        code1 = " if() ;"
        code2 = " if() {}"
        code3 = " if() if() ;"
        ans1 = 6
        ans2 = 7
        ans3 = 11
        self.assertEqual(matchIf(code1), ans1)
        self.assertEqual(matchIf(code2), ans2)
        self.assertEqual(matchIf(code3), ans3)


    def test_matchElseIf(self):
        code1 = " elseif() ;"
        code2 = " elseif() {}"
        code3 = " elseif() if() ;"
        ans1 = 10
        ans2 = 11
        ans3 = 15
        self.assertEqual(matchElseIf(code1), ans1)
        self.assertEqual(matchElseIf(code2), ans2)
        self.assertEqual(matchElseIf(code3), ans3)


    def test_matchElse(self):
        code1 = " else {}"
        code2 = " else ;"
        ans1 = 7
        ans2 = 6
        self.assertEqual(matchElse(code1), ans1)
        self.assertEqual(matchElse(code2), ans2)


    def test_matchCode(self):
        code = readfile("./test_matchCode.c")
        # print(code)
        # exchange else if to elseif
        code = re.sub("else\s+if", "elseif", code)
        # exchange else{ to else {
        code = re.sub("else{", "else {", code)
        ie, iei = matchCode(code)
        self.assertEqual(ie, 4)
        self.assertEqual(iei, 4)


if __name__ == '__main__':
    unittest.main()
