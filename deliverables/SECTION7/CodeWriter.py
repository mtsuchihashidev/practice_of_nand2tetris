#!/usr/bin/python
# -*- coding: utf-8 -*-
from os.path import splitext

from CommandType import C_PUSH, C_POP, CommandType
from Utils import Utils


class CodeWriter:
    __TRUE = 65535
    __FALSE = 0
    def __init__(self, filename:str):
        """
        出力ファイル/ストリームを開き、書き込み準備を行う。
        """
        asm_filename = f"{Utils.get_corename(filename)}.asm"
        self.__fw = open(asm_filename, 'w')
        stmt = []
        stmt.append('@256')
        stmt.append('D=A')
        stmt.append('@SP')
        stmt.append('M=D')
        self.__fw.write('\n'.join(stmt) + "\n")
    def set_file_name(self, filename:str):
        """
        CodeWriterモジュールに新しいVMファイルの変換が開始したことを知らせる。
        """
        self.__classname = Utils.get_corename(filename)
        self.__eq_cnt = 0
        self.__gt_cnt = 0
        self.__lt_cnt = 0
    def write_arithmetic(self, command:str):
        """
        与えられた算術コマンドをアセンブリコードに変換し、それを書き込む。
        """
        def get_stack_pop_asm()->list:
            stmt = []
            # A=0
            stmt.append('@SP')
            # M[0] = M[0] - 1  # prev address
            stmt.append('M=M-1')
            # A = M[0]
            stmt.append('A=M')
            return stmt
        cmd = command.lower()
        stmt = []
        if cmd == 'add':
            # # A=0
            # stmt.append('@SP')
            # # M[0] = M[0] - 1  # prev address
            # stmt.append('M=M-1')
            # # A = M[0]
            # stmt.append('A=M')
            stmt = get_stack_pop_asm()
            # D = M[A]
            stmt.append('D=M')
            # # A=0
            # stmt.append('@SP')
            # # M[0] = M[0] - 1  # prev address
            # stmt.append('M=M-1')
            # # A = M[0]
            # stmt.append('A=M')
            stmt = stmt + get_stack_pop_asm()
            # M[A] = D + M[A]
            stmt.append('M=D+M')
        elif cmd == 'sub':
            stmt = get_stack_pop_asm()
            # D = M[A]
            stmt.append('D=M')
            stmt = stmt + get_stack_pop_asm()
            # M[A] = D + M[A]
            stmt.append('M=M-D')
        elif cmd == 'neg':
            stmt = get_stack_pop_asm()
            # M[A] = M[A]
            stmt.append('M=-M')
        elif cmd == 'eq':
            eq_true = f"{self.__classname}.{self.__eq_cnt}.EQTRUE"
            eq_end = f"{self.__classname}.{self.__eq_cnt}.EQEND"
            self.__eq_cnt += 1
            stmt = get_stack_pop_asm()
            # D = M[A]
            stmt.append('D=M')
            stmt = stmt + get_stack_pop_asm()
            # D = M[A] - D
            stmt.append('D=M-D')
            # D;JEQ
            stmt.append(f"@{eq_true}")
            stmt.append('D;JEQ')
            # D = 0
            stmt.append(f"@{self.__FALSE}")
            stmt.append('D=A')
            # M[0]
            stmt.append('@SP')
            # A = M[0]
            stmt.append('A=M')
            # M[A] = 0x0000(FALSE)
            stmt.append('M=D')
            stmt.append(f"@{eq_end}")
            stmt.append('0;JMP')
            # IF TRUE
            stmt.append(f"({eq_true})")
            # A = 0xEFFF
            # stmt.append(f"@{self.__TRUE}")
            stmt.append('@0')
            stmt.append('A=!A')
            # D = A
            stmt.append('D=A')
            # A = 0
            stmt.append('@SP')
            # A = M[0]
            stmt.append('A=M')
            # M[A] = 0xFFFF
            stmt.append('M=D')
            stmt.append(f"({eq_end})")
        elif cmd == 'gt':
            gt_true = f"{self.__classname}.{self.__gt_cnt}.GTTRUE"
            gt_end = f"{self.__classname}.{self.__gt_cnt}.GTEND"
            self.__gt_cnt += 1
            stmt = get_stack_pop_asm()
            # D = M[A]
            stmt.append('D=M')
            stmt = stmt + get_stack_pop_asm()
            # D = M[A] - D
            stmt.append('D=M-D')
            # D;JEQ
            stmt.append(f"@{gt_true}")
            stmt.append('D;JGT')
            # D = 0
            stmt.append(f"@{self.__FALSE}")
            stmt.append('D=A')
            # M[0]
            stmt.append('@SP')
            # A = M[0]
            stmt.append('A=M')
            # M[A] = 0x0000(FALSE)
            stmt.append('M=D')
            stmt.append(f"@{gt_end}")
            stmt.append('0;JMP')
            # IF TRUE
            stmt.append(f"({gt_true})")
            # A = 0xFFFF
            # stmt.append(f"@{self.__TRUE}")
            stmt.append('@0')
            stmt.append('A=!A')
            # D = A
            stmt.append('D=A')
            # A = 0
            stmt.append('@SP')
            # A = M[0]
            stmt.append('A=M')
            # M[A] = 0xFFFF
            stmt.append('M=D')
            stmt.append(f"({gt_end})")
        elif cmd == 'lt':
            lt_true = f"{self.__classname}.{self.__lt_cnt}.LTTRUE"
            lt_end = f"{self.__classname}.{self.__lt_cnt}.LTEND"
            self.__lt_cnt += 1
            stmt = get_stack_pop_asm()
            # D = M[A]
            stmt.append('D=M')
            stmt = stmt + get_stack_pop_asm()
            # D = M[A] - D
            stmt.append('D=M-D')
            # D;JEQ
            stmt.append(f"@{lt_true}")
            stmt.append('D;JLT')
            # D = 0
            stmt.append(f"@{self.__FALSE}")
            stmt.append('D=A')
            # M[0]
            stmt.append('@SP')
            # A = M[0]
            stmt.append('A=M')
            # M[A] = 0x0000(FALSE)
            stmt.append('M=D')
            stmt.append(f"@{lt_end}")
            stmt.append('0;JMP')
            # IF TRUE
            stmt.append(f"({lt_true})")
            # A = 0xFFFF
            # stmt.append(f"@{self.__TRUE}")
            stmt.append('@0')
            stmt.append('A=!A')
            # D = A
            stmt.append('D=A')
            # A = 0
            stmt.append('@SP')
            # A = M[0]
            stmt.append('A=M')
            # M[A] = 0xFFFF
            stmt.append('M=D')
            stmt.append(f"({lt_end})")
        elif cmd == 'and':
            stmt = get_stack_pop_asm()
            # D = M[A]
            stmt.append('D=M')
            stmt = stmt + get_stack_pop_asm()
            # M[A] = D & M[A]
            stmt.append('M=D&M')
        elif cmd == 'or':
            stmt = get_stack_pop_asm()
            # D = M[A]
            stmt.append('D=M')
            stmt = stmt + get_stack_pop_asm()
            # M[A] = D & M[A]
            stmt.append('M=D|M')
        elif cmd == 'not':
            stmt = get_stack_pop_asm()
            # M[A] = D & M[A]
            stmt.append('M=!M')
        else:
            raise Exception('Not ARITHMETIC command')
        # SP + 1
        stmt.append('@SP')
        stmt.append('M=M+1')
        self.__fw.write('\n'.join(stmt) + "\n")
    def write_push_pop(self, command:CommandType, segment:str, index:int):
        """
        C_PUSHまたはC_POPコマンドをアセンブリコードに変換し、それを書き込む。
        """
        if command != C_PUSH and command != C_POP:
            raise Exception(f"not Push/Pop command: {command}")
        stmt = []
        seg = segment.lower()
        if index < 0:
            raise Exception(f"invalid index: {index}")
        # indexが上限を超えたらどうする？
        if command == C_PUSH:
            # only 1 in the vm
            if seg == 'constant':
                if index > 32767:
                    raise Exception(f"not support index: {index}")
                stmt.append(f"@{index}")
                stmt.append('D=A')
            elif seg == 'temp':
                if index > 8:
                    raise Exception(f"out of index at temp segment: {index} > 8")
                tmp_idx = 5 + index  # temp segment's base address
                stmt.append(f"@{tmp_idx}")
                stmt.append('D=M')
            # only 1 in each classes
            elif seg == 'static':
                symbol = f"{self.__classname}.{index}"
                stmt.append(f"@{symbol}")  # static segment's base address
                stmt.append('D=M')
            # only 1 in each class.function
            elif seg in ('argument', 'local', 'this', 'that'):
                if seg == 'argument':
                    # As pop, this ARG base address increments +1
                    stmt.append('@ARG')
                elif seg == 'local':
                    stmt.append('@LCL')
                elif seg == 'this':
                    stmt.append('@THIS')
                elif seg == 'that':
                    stmt.append('@THAT')
                stmt.append('A=M')
                for _ in range(index):
                    stmt.append('A=A+1')
                stmt.append('D=M')
                # stmt.append(f"@{index}")
                # stmt.append('A=D+A')
                # stmt.append('D=M')
            elif seg == 'pointer':
                if index > 1:
                    raise Exception(f"out of index at pointer segment: {index} > 1")
                ptr_idx = 3 + index  # temp segment's base address
                stmt.append(f"@{ptr_idx}")
                stmt.append('D=M')
            else:
                raise Exception(f"invalid segment: {seg}")
            # A = SP
            stmt.append('@SP')
            # A = M[SP]
            stmt.append('A=M')
            # M[A] = D
            stmt.append('M=D')
            # A = SP
            stmt.append('@SP')
            # M[SP] = M[SP] + 1
            stmt.append('M=M+1')
        elif command == C_POP:
            # POP M->D
            stmt.append('@SP')
            stmt.append('M=M-1')
            # A = M[SP]
            stmt.append('A=M')
            # D = M[A] (D = M[(M[SP])])
            stmt.append('D=M')
            
            # only 1 in the vm
            if seg == 'constant':
                # Phony command?
                return
            elif seg == 'temp':
                if index > 8:
                    raise Exception(f"out of index at temp segment: {index} > 8")
                tmp_idx = 5 + index  # temp segment's base address
                stmt.append(f"@{tmp_idx}")
                stmt.append('M=D')
            # only 1 in each classes
            elif seg == 'static':
                symbol = f"{self.__classname}.{index}"
                stmt.append(f"@{symbol}")  # static segment's base address
                stmt.append('M=D')
            # only 1 in each class.function
            elif seg in ('argument', 'local', 'this', 'that'):
                if seg == 'argument':
                    # As pop, this ARG base address increments +1
                    stmt.append('@ARG')
                    stmt.append('A=M')
                elif seg == 'local':
                    # stmt.append('@LCL')
                    stmt.append('@LCL')
                    stmt.append('A=M')
                elif seg == 'this':
                    stmt.append('@THIS')
                    stmt.append('A=M')
                elif seg == 'that':
                    stmt.append('@THAT')
                    stmt.append('A=M')
                for _ in range(index):
                    stmt.append('A=A+1')
                stmt.append('M=D')
            elif seg == 'pointer':
                if index > 1:
                    raise Exception(f"out of index at pointer segment: {index} > 1")
                ptr_idx = 3 + index  # temp segment's base address
                stmt.append(f"@{ptr_idx}")
                stmt.append('M=D')
            else:
                raise Exception(f"invalid segment: {seg}")
            # stmt.append('@SP')
            # stmt.append('A=M')
            # stmt.append('D=M')
            # stmt.append('M=D')
        else:
            pass
        self.__fw.write('\n'.join(stmt) + "\n")
            
    def close(self):
        """
        出力ファイルを閉じる。
        """
        if not self.__fw:
            return
        self.__fw.close()



# EOF
