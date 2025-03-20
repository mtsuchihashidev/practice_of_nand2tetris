#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from CommandType import C_ARITHMETIC, C_PUSH, C_POP, \
    C_LABEL, C_GOTO, C_IF, \
    C_FUNCTION, C_RETURN, C_CALL, \
    CommandType
from Utils import Utils

class Parser:
    __ARITHMETIC_SYMBOLS = set(['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'])
    def __init__(self, filename:str):
        """
        入力ファイル/ストリームを開きパースを行う準備をする
        """
        def checker(_s:str)->bool:
            s = _s.strip()
            is_ok = True
            is_ok = is_ok and len(s) != 0
            is_ok = is_ok and not s.startswith("//")
            return is_ok
        with open(filename, 'r') as fi:
            self.__vm_lines = list(filter(lambda x: checker(x),
                                          map(lambda x: x.strip(),
                                              fi.readlines())))
        self.__class_name = Utils.get_corename(filename)
        self.__cidx = -1
        self.__command = ''
        self.__arg1 = ''
        self.__arg2 = ''
    def has_more_commands(self)->bool:
        """
        入力において、さらにコマンドが存在するか？
        """
        return self.__cidx < len(self.__vm_lines) - 1
    def advance(self):
        """
        入力から次のコマンドを読み、それを現コマンドとする。
        has_more_commands()がtrueの場合のみ、本ルーチンを呼ぶようにする。
        """
        if not self.has_more_commands():
            raise Exception('no more commands')
        self.__cidx += 1
        elms = self.__vm_lines[self.__cidx].split()
        self.__command = elms[0] if len(elms) > 0 else ''
        self.__arg1 = elms[1] if len(elms) > 1 else ''
        self.__arg2 = elms[2] if len(elms) > 2 else ''
    def command_type(self)->CommandType:
        """
        現VMコマンドの種類を返す。
        算術コマンドはすべてC_ARITHMETICが返される。
        """
        cmd = self.__command.lower()
        if cmd in self.__ARITHMETIC_SYMBOLS:
            return C_ARITHMETIC
        elif cmd == 'push':
            return C_PUSH
        elif cmd == 'pop':
            return C_POP
        elif cmd == 'label':
            return C_LABEL
        elif cmd == 'goto':
            return C_GOTO
        elif cmd == 'if-goto':
            return C_IF
        elif cmd == 'function':
            return C_FUNCTION
        elif cmd == 'call':
            return C_CALL
        elif cmd == 'return':
            return C_RETURN
        else:
             raise Exception(f"unsupport command: {cmd}")   
    def arg1(self)->str:
        """
        現コマンドの最初の引数が返される。
        C_ARITHMETICの場合、コマンド自体(add, subなど)が返される。
        現コマンドがC_RETURNの場合、本ルーチンは呼ばないようにする。
        """
        cmd_type = self.command_type()
        if cmd_type == C_RETURN:
            raise Exception(f"invalid call: arg1 ({cmd_type.__class__.__name__})")
        elif cmd_type == C_ARITHMETIC:
            return self.__command.lower()
        else:
            return self.__arg1
    def arg2(self)->int:
        """
        現コマンドの2番めの引数が返される。
        現コマンドがC_PUSH, C_POP, C_FUNCTION, C_CALLの場合のみ本ルーチンを呼ぶようにする。
        """
        cmd_type = self.command_type()
        if cmd_type in (C_PUSH, C_POP, C_FUNCTION, C_CALL):
            return self.__arg2
        else:
            raise Exception(f"invalid call: arg2 ({cmd_type.__class__.__name__})")
            


# EOF
