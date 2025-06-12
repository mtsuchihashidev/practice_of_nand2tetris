#!/usr/bin/python3
# -*- coding: utf-8 -*-

from CommandType import CommandType, C_ADD, C_SUB, C_NEG, C_EQ, \
    C_GT, C_LT, C_AND, C_OR, C_NOT

from SegmentType import SegmentType, SEG_CONST, SEG_ARG, SEG_LOCAL, \
    SEG_STATIC, SEG_THIS, SEG_THAT, SEG_POINTER, SEG_TEMP


class VMWriter:
    def __init__(self, filepath):
        """新しいファイルを作り、それに書き込む準備をする
        """
        # TODO Sys.vmを出力するように改修する
        self.__lines = []
        self.__filepath = filepath

    def writePuth(self, segment:SegmentType, index:int):
        """pushコマンドを書く
        """
        line = f"\tpush {str(segment)} {index}"
        self.__lines.append(line)

    def writePop(self, segment:SegmentType, index:int):
        """popコマンドを書く
        """
        line = f"\tpop {str(segment)} {index}"
        self.__lines.append(line)

    def writeArithmetic(self, command:CommandType):
        """算術コマンドを書く
        """
        line = f"{str(command)}"
        self.__lines.append(line)

    def writeLabel(self, label:str):
        """labelコマンドを書く
        """
        line = f"label {label}"
        self.__lines.append(line)

    def writeGoto(self, label:str):
        """
        """
        line = f"\tgoto {label}"
        self.__lines.append(line)

    def writeIf(self, label:str):
        line = f"\tif-goto {label}"
        self.__lines.append(line)

    def writeCall(self, name:str, n_args:int):
        line = f"\tcall {name} {str(n_args)}"
        self.__lines.append(line)

    def writeFunction(self, name:str, n_args:int):
        line = f"function {name} {str(n_args)}"
        self.__lines.append(line)

    def writeReturn(self):
        line = f"\treturn"
        self.__lines.append(line)

    def close(self):
        """出力ファイルを閉じる
        """
        with open(self.__filepath, 'w', encoding="utf-8") as fo:
            fo.write("\n".join(self.__lines))
    

# EOF
