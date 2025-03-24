#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os import listdir
from os.path import isdir, isfile, splitext, basename, join
import re

from Parser import Parser
from CodeWriter import CodeWriter
from CommandType import C_ARITHMETIC, C_PUSH, C_POP, \
    C_LABEL, C_GOTO, C_IF, \
    C_FUNCTION, C_RETURN, C_CALL
from Utils import Utils, Log

RX_SYS_INIT = re.compile(r'function\s+Sys.init', re.S)

class Main:
    def __init__(self, vm_program: str):
        self.__vm_program = vm_program
        self.__filelist = []
        if isdir(self.__vm_program):
            for fd in listdir(self.__vm_program):
                fl = join(self.__vm_program, fd)
                if not isfile(fl):
                    continue
                if splitext(fl)[1] != '.vm':
                    continue
                self.__filelist.append(fl)
        elif isfile(self.__vm_program):
            self.__filelist.append(self.__vm_program)
        else:
            raise Exception(f"invalid input: {vm_program}")

        # TODO search "Sys.init"
        self.__sys_init_filename = ''
        for filename in self.__filelist:
            with open(filename, 'r') as fi:
                if not RX_SYS_INIT.search(fi.read()):
                    continue
                if self.__sys_init_filename:
                    raise Exception(f"duplicate Sys.init. abort.")
                self.__sys_init_filename = filename
        self.__program_name = Utils.get_corename(self.__vm_program)
        self.__code_writer = CodeWriter(self.__program_name)

    def __to_asm(self, filename):
        parser = Parser(filename)
        while parser.has_more_commands():
            parser.advance()
            command_type = parser.command_type()
            if command_type == C_ARITHMETIC:
                command = parser.arg1()
                self.__code_writer.write_arithmetic(command)
            elif command_type in (C_PUSH, C_POP):
                arg1 = parser.arg1()
                arg2 = parser.arg2()
                self.__code_writer.write_push_pop(command_type, arg1, int(arg2))
            elif command_type == C_LABEL:
                arg1 = parser.arg1()
                self.__code_writer.write_label(arg1)
            elif command_type == C_GOTO:
                arg1 = parser.arg1()
                self.__code_writer.write_goto(arg1)
            elif command_type == C_IF:
                arg1 = parser.arg1()
                self.__code_writer.write_if(arg1)
            elif command_type == C_CALL:
                arg1 = parser.arg1()
                arg2 = parser.arg2()
                self.__code_writer.write_call(arg1, int(arg2))
            elif command_type == C_FUNCTION:
                arg1 = parser.arg1()
                arg2 = parser.arg2()
                self.__code_writer.write_function(arg1, int(arg2))
            elif command_type == C_RETURN:
                self.__code_writer.write_return()
            else:
                raise Exception(f"invalid command: {command_type.__class__.__name__}")

    def __run(self):
        try:
            for filename in self.__filelist:
                self.__code_writer.set_file_name(filename)
                self.__to_asm(filename)
        except Exception as e:
            raise e
        finally:
            self.__code_writer.close()

    def __exec(self):
        code_writer = self.__code_writer
        # self.__dry_run()
        self.__code_writer.set_file_name(self.__sys_init_filename)
        self.__code_writer.write_init()
        self.__run()
        return 0
        
    @staticmethod
    def execute(params:list)->int:
        m = Main(params[0])
        return m.__exec()

if __name__ == '__main__':
    exit(Main.execute(sys.argv[1:]))

# EOF
