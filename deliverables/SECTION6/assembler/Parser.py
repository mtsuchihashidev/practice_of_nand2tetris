#!/usr/bin/python
# -*- coding: utf-8  -*-
import re
import sys

from Const import EMPTY
from AssemblerException import InvalidArgumentsError, ExistNoCommandError, ParseError
from CommandType import A_COMMAND, C_COMMAND, L_COMMAND, CommandType


RX_FILENAME = re.compile(r'.*[A-Z]\w+\.asm$', re.S)
RX_COMMENT = re.compile(r'^//', re.S)
RX_DECIMAL = re.compile(r'^\d+$', re.S)
RX_A_COMMAND = re.compile(r'^@(\w)$', re.S)
# TODO もう少し精緻化
RX_C_COMMAND = re.compile(r'^([^=]+)=([^;]+)(:?;(\w+))?$', re.S)
RX_L_COMMAND = re.compile(r'^\((\w+)\)%', re.S)

class Parser:
    def __init__(self, filename):
        """
        入力ファイル/ストリームを開きパースを行う準備をする
        """
        if not RX_FILENAME.match(filename):
            # TODO
            raise InvalidArgumentsError(f"filename: {filename}")
        def filter_comment(seq):
            return filter(lambda x: not RX_COMMENT.search(x), seq)
        def filter_blank(seq):
            return filter(lambda x: x, seq)
        def map_cleanup(seq):
            return map(lambda x: x.strip().replace(' ', ''), seq)
        self.__command_list = []
        with open(filename, 'r') as fi:
            self.__command_list = list(
                filter_comment(
                    filter_blank(
                        map_cleanup(fi.readlines())
                    )
                )
            )
        self.__index = -1
        self.__size = len(self.__command_list)

    def has_more_commands(self)->bool:
        """
        入力にまだコマンドが存在するか？
        """
        return self.__index < self.__size - 1

    def advance(self):
        """
        入力から次のコマンドを読み、それを現在のコマンドにする。
        このルーチンはhasMoreCommand()がtrueの場合のみ呼ぶようにする。
        最初は現コマンドは空である。
        """
        if not self.has_more_commands():
            raise ExistNoCommandError()
        self.__index += 1

    def command_type(self) -> CommandType:
        """
        現コマンドの種類を返す。
        * A_COMMAND は @Xxx を意味し、Xxx はシンボルか10進数の数値である
        * C_COMMAND は dest=comp;jumpを意味する
        * L_COMMAND は疑似コマンドである。(Xxx)を意味する。Xxx はシンボルである。
        """
        cmd = self.__getCurrentCommand()
        if RX_A_COMMAND.search(cmd):
            return A_COMMAND
        elif RX_C_COMMAND.search(cmd):
            return C_COMMAND
        elif RX_L_COMMAND.search(cmd):
            return L_COMMAND
        else:
            # TODO
            raise ParseError()

    def symbol(self) -> str:
        """
        現コマンド@Xxx または (Xxx) の Xxx を返す。
        Xxx はシンボルまたは10進数の数値である。
        このルーチンはcommandType()がA_COMMANDまたはL_COMMANDのときだけ呼ぶようにする。
        """
        command = self.__getCurrentCommand()
        command_type = self.command_type()
        if command_type == A_COMMAND:
            a_command = RX_A_COMMAND.search(command)[1]
            if RX_DECIMAL.search(a_command):
                return self.__to_binary(a_command)
            else:
                return a_command
        elif command_type == L_COMMAND:
            mo = RX_L_COMMAND.search(command)
            return mo[1]
        else: 
            # TODO
            raise ParseError()
        
    def dest(self) -> str:
        """
        現C命令のdestニーモニックを返す（候補として8つの可能性がある）。
        このルーチンはcommand_type()がC_COMMANDのときだけ呼ぶようにする。
        """
        command = self.__getCurrentCommand()
        command_type = self.command_type()
        if command_type != C_COMMAND:
            raise ParseError()
        mo = RX_C_COMMAND.search(command)
        return mo[1]

    def comp(self) -> str:
        """
        現C命令のcompニーモニックを返す（候補として28つの可能性がある）。
        このルーチンはcommandType()がC_COMMANDのときだけ呼ぶようにする。
        """
        command = self.__getCurrentCommand()
        command_type = self.command_type()
        if command_type != C_COMMAND:
            raise ParseError()
        mo = RX_C_COMMAND.search(command)
        return mo[2]

    def jump(self) -> str:
        """
        現C命令のjumpニーモニックを返す（候補として8つの可能性がある）。
        このルーチンはcommandType()がC_COMMANDのときだけ呼ぶようにする。
        """
        command = self.__getCurrentCommand()
        command_type = self.command_type()
        if command_type != C_COMMAND:
            raise ParseError()
        mo = RX_C_COMMAND.search(command)
        return mo[3] or EMPTY


    def __getCurrentCommand(self):
        return self.__command_list[self.__index]

    def __to_binary(self, decimal:str)->str:
        return f"{bin(int(decimal))[2:]:0>16}"
        

if __name__ == '__main__':
    pass
    # print("test 1")
    # try:
    #     testee = Parser("hoge")

# EOF
