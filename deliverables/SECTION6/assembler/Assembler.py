#!/usr/bin/python
# -*- coding: utf-8  -*-
import os
import re
import sys

from Parser import Parser
from CommandType import A_COMMAND, C_COMMAND, L_COMMAND
from Code import Code

def main(params):
    filename = params[0]
    basename = os.path.splitext(os.path.basename(filename))[0]
    parser = Parser(filename)
    code = Code()
    hack_list = []
    while parser.has_more_commands():
        parser.advance()
        binary = ''
        command_type = parser.command_type()
        if command_type in (A_COMMAND, L_COMMAND):
            binary = parser.symbol()
        elif command_type == C_COMMAND:
            binary = '111'
            binary += code.comp(parser.comp())
            binary += code.dest(parser.dest())
            binary += code.jump(parser.jump())
        else:
            raise Exception()
        hack_list.append(binary)

    with open(f"{basename}.hack", 'w') as fo:
        fo.write("\n".join(hack_list) + "\n")
    return 0

if __name__ == '__main__':
    exit(main(sys.argv[1:]))

# EOF
