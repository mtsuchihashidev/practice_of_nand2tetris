#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os import listdir
from os.path import isdir, isfile, splitext, basename

from Parser import Parser
from CodeWriter import CodeWriter
from CommandType import C_ARITHMETIC, C_PUSH, C_POP, \
    C_LABEL, C_GOTO, C_IF, \
    C_FUNCTION, C_RETURN, C_CALL
from Utils import Utils

class Main:
    @staticmethod
    def execute(params:list)->int:
        vmpgm = params[0]
        filelist = []
        if isdir(vmpgm):
            for fd in listdir(vmpgm):
                if not isfile(fd):
                    continue
                if splitext(fd)[1] != '.vm':
                    continue
                filelist.append(fd)
        elif isfile(vmpgm):
            filelist.append(vmpgm)
        else:
            raise Exception(f"invalid input: {vmpgm}")
        program_name = Utils.get_corename(vmpgm)
        code_writer = CodeWriter(program_name)
        code_writer.write_init()
        for filename in filelist:
            code_writer.set_file_name(filename)
            try:
                parser = Parser(filename)
                while parser.has_more_commands():
                    parser.advance()
                    command_type = parser.command_type()
                    if command_type == C_ARITHMETIC:
                        command = parser.arg1()
                        code_writer.write_arithmetic(command)
                    elif command_type in (C_PUSH, C_POP):
                        arg1 = parser.arg1()
                        arg2 = parser.arg2()
                        code_writer.write_push_pop(command_type, arg1, int(arg2))
                    elif command_type == C_LABEL:
                        arg1 = parser.arg1()
                        code_writer.write_label(arg1)
                    elif command_type == C_GOTO:
                        arg1 = parser.arg1()
                        code_writer.write_goto(arg1)
                    elif command_type == C_IF:
                        arg1 = parser.arg1()
                        code_writer.write_if(arg1)
                    elif command_type == C_CALL:
                        arg1 = parser.arg1()
                        arg2 = parser.arg2()
                        code_writer.write_call(arg1, int(arg2))
                    elif command_type == C_FUNCTION:
                        arg1 = parser.arg1()
                        arg2 = parser.arg2()
                        code_writer.write_function(arg1, int(arg2))
                    elif command_type == C_RETURN:
                        code_writer.write_return()
                    else:
                        raise Exception(f"invalid command: {command_type.__classname__}")
            except Exception as e:
                raise e
            finally:
                code_writer.close()
        return 0


if __name__ == '__main__':
    exit(Main.execute(sys.argv[1:]))

# EOF
