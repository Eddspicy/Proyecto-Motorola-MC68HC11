# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"b[ceghlmnprsv][aceilnoqrst](\s)?([a-zA-Z]{0,256})?"
test_str = "bgt HOLA"

match = re.fullmatch(regex, test_str)

print(match)