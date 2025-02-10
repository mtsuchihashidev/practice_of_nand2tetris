#!/usr/bin/python
# -*- coding: utf-8  -*-
import os
import re
import sys

from Parser import Parser
from CommandType import A_COMMAND, C_COMMAND, L_COMMAND
from Code import Code
from SymbolTable import SymbolTable

def main(params):
    filename = params[0]
    basename = os.path.splitext(os.path.basename(filename))[0]
    parser0 = Parser(filename)
    symbol_table = SymbolTable()
    rom_counter = -1
    while parser0.has_more_commands():
        parser0.advance()
        rom_counter += 1
        command_type = parser0.command_type()
        if command_type != L_COMMAND:
            continue
        symbol = parser0.symbol()
        if symbol_table.contains(symbol):
            continue
        symbol_table.addEntry(symbol, rom_counter)
        rom_counter -= 1

    parser = Parser(filename)
    ram_counter = 16
    code = Code()
    hack_list = []
    while parser.has_more_commands():
        parser.advance()
        binary = ''
        command_type = parser.command_type()
        if command_type == A_COMMAND:
            symbol = parser.symbol()
            if symbol[0] in [str(i) for i in range(0,10)]:
                binary = symbol
            else:
                if not symbol_table.contains(symbol):
                    symbol_table.addEntry(symbol, ram_counter)
                    ram_counter += 1
                binary = f"{bin(symbol_table.getAddress(symbol))[2:]:0>16}"
        elif command_type == L_COMMAND:
            continue
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
