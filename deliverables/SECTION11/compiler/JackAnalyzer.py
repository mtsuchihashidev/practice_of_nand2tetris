#!/usr/bin/python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser as ap
import sys
from os import listdir
from os.path import isdir, isfile, splitext, basename, join

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from Utils import Utils, Log



class Main:
    def __init__(self, jack_program: str):
        self.__jack_program = jack_program
        self.__filelist = []
        if isdir(self.__jack_program):
            for fd in listdir(self.__jack_program):
                fl = join(self.__jack_program, fd)
                if not isfile(fl):
                    continue
                if splitext(fl)[1] != '.jack':
                    continue
                self.__filelist.append(fl)
        elif isfile(self.__jack_program):
            self.__filelist.append(self.__jack_program)
        else:
            raise Exception(f"invalid input: {jack_program}")

    def __run(self):
        try:
            for filename in self.__filelist:
                filebase = splitext(basename(filename))[0]
                compiler = CompilationEngine(JackTokenizer(filename), filebase)
                compiler.compile_class()
        except Exception as e:
            raise e
  
    def __exec(self):
        self.__run()
        return 0
        
    @staticmethod
    def execute(params:list)->int:
        m = Main(params[0])
        return m.__exec()

if __name__ == '__main__':
    parser = ap(prog="JackAnalyzer", usage='%(prog)s filename [option]')
    parser.add_argument('filename')

    args = parser.parse_args()
    exit(Main.execute(sys.argv[1:]))

# EOF
