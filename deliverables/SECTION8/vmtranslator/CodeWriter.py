#!/usr/bin/python
# -*- coding: utf-8 -*-
from os.path import splitext
import sys

from CommandType import C_PUSH, C_POP, CommandType
from Utils import Utils


class CodeWriter:
    __FALSE = 0
    def __init__(self, filename:str):
        """
        出力ファイル/ストリームを開き、書き込み準備を行う。
        """
        asm_filename = f"{Utils.get_corename(filename)}.asm"
        self.__fw = open(asm_filename, 'w')
        self.__is_done_init = False
        self.__global_stack_size = 0
        self.__local_size = 0
        self.__argument_size = 0
        self.__this_size = 0
        self.__that_size = 0
        self.__call_count = dict()
    def set_file_name(self, filename:str):
        """
        CodeWriterモジュールに新しいVMファイルの変換が開始したことを知らせる。
        """
        self.__classname = Utils.get_corename(filename)
        # TODO REMOVE
        self.__functionname = "Karitaiou"
        self.__eq_cnt = 0
        self.__gt_cnt = 0
        self.__lt_cnt = 0
    def write_init(self):
        """
        VMの初期化（これは「ブートストラップ」と呼ばれる）を行うアセンブリコードを書く。
        このコードは出力ファイルの先頭に配置しなければならない。
        """
        self.__functionname = "Sys.init"
        self.__eq_cnt = 0
        self.__gt_cnt = 0
        self.__lt_cnt = 0
        self.__call_count['Sys.init'] = -1

        stmt = []
        # # # # M[SP] = 256
        # # # stmt.append('@256')
        # # # stmt.append('D=A')
        # # # stmt.append('@SP')
        # # # stmt.append('M=D')
        # # M[LCL] = 256
        # stmt.append('@256')
        # stmt.append('D=A')
        # stmt.append('@LCL')
        # stmt.append('M=D')
        # # M[ARG] = 257
        # stmt.append('@257')
        # stmt.append('D=A')
        # stmt.append('@ARG')
        # stmt.append('M=D')
        # # M[THIS] = 258
        # stmt.append('@258')
        # stmt.append('D=A')
        # stmt.append('@THIS')
        # stmt.append('M=D')
        # # M[THAT] = 259
        # stmt.append('@259')
        # stmt.append('D=A')
        # stmt.append('@THAT')
        # stmt.append('M=D')
        # # M[POINTER] = 260
        # stmt.append('@9999')
        # stmt.append('D=A')
        # stmt.append('@260')
        # stmt.append('M=D')
        # # M[SP] = 261
        # stmt.append('@261')
        # stmt.append('D=A')
        # stmt.append('@SP')
        # stmt.append('M=D')
        # self.__fw.write('\n'.join(stmt) + "\n")
        # # # call Sys.init
        # # TODO DEBUG
        # self.__fw.write('\n'.join(['@9001']) + "\n")
        # self.write_call('Sys.init', 0)
        # # stmt.append('@Sys.init')
        # # stmt.append('0;JMP')
        
        
        # TODO

        self.__is_done_init = True
    def write_arithmetic(self, command:str):
        """
        与えられた算術コマンドをアセンブリコードに変換し、それを書き込む。
        """
        def get_stack_pop_asm()->list:
            stmt = []
            stmt = self.__backward_sp(stmt)
            # A = M[0]
            stmt.append('A=M')
            return stmt
        cmd = command.lower()
        stmt = []
        if cmd == 'add':
            stmt = get_stack_pop_asm()
            # D = M[A]
            stmt.append('D=M')
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
        stmt = self.__forward_sp(stmt)
        self.__write(stmt)
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
            self.__global_stack_size += 1
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
            stmt = self.__forward_sp(stmt)
        elif command == C_POP:
            self.__global_stack_size -= 1
            # # POP M->D
            stmt = self.__backward_sp(stmt)
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
        else:
            pass
        self.__write(stmt)
    def write_label(self, label:str):
        """
        labelコマンドを行うアセンブリコードを書く
        """
        label = self.__get_label(label)
        stmt = []
        stmt.append(f"({label})")
        self.__write(stmt)
    def write_goto(self, label:str):
        """
        gotoコマンドを行うアセンブリコードを書く
        """
        label = self.__get_label(label)
        stmt = []
        stmt.append(f"@{label}")
        stmt.append('0;JMP')
        self.__write(stmt)
    def write_if(self, label:str):
        """
        if-gotoコマンドを行うアセンブリコードを書く
        """
        self.__global_stack_size -= 1
        label = self.__get_label(label)
        stmt = []
        stmt = self.__backward_sp(stmt)
        stmt.append('A=M')
        stmt.append('D=M')
        stmt.append(f"@{label}")
        stmt.append('D;JNE')
        self.__write(stmt)
    def write_call(self, function_name: str, num_args: int):
        """
        callコマンドを行うアセンブリコードを書く
        """
        if not function_name in self.__call_count or not self.__call_count[function_name]:
            self.__call_count[function_name] = -1
        self.__call_count[function_name] += 1
        return_address_element = []
        return_address_element.append("RETURN")
        self.__functionname = function_name
        return_address_element.append(self.__get_functionname())
        return_address_element.append(str(self.__call_count[function_name]))
        return_address = ".".join(return_address_element)

        def push_base_address(symbol:str, stmt:list)->list:
            stmt.append(f"@{symbol}")
            stmt.append('A=M')
            stmt.append('D=A')
            stmt.append('@SP')
            stmt.append('A=M')
            stmt.append('M=D')
            return self.__forward_sp(stmt)
        stmt = []
        # push return-address
        stmt.append(f"@{return_address}")
        stmt.append('D=A')
        stmt.append('@SP')
        stmt.append('A=M')
        stmt.append('M=D')
        stmt = self.__forward_sp(stmt)
        # push LCL
        stmt = push_base_address('LCL', stmt)
        # push ARG
        stmt = push_base_address('ARG', stmt)
        # push THIS
        stmt = push_base_address('THIS', stmt)
        # push THAT
        stmt = push_base_address('THAT', stmt)
        # called-function's ARG
        stmt.append('@SP')        
        stmt.append('D=M')
        # len([ret-adrss, LCL, ARG, THIS, THAT]) -> 5
        for _ in range(num_args + 5):
            stmt.append('D=D-1')
        stmt.append('@ARG')
        stmt.append('M=D')
        # TODO ???? does SP progress? or not?
        # LCL = SP
        stmt.append('@SP')
        stmt.append('D=M')
        stmt.append('@LCL')
        stmt.append('M=D')
        # goto f
        stmt.append(f"@{function_name}")
        stmt.append('0;JMP')
        # label return-address
        stmt.append(f"({return_address})")
        self.__write(stmt)
    def write_return(self):
        """
        returnコマンドを行うアセンブリコードを書く
        """
        def backward(frame:str, symbol:str, num:int, stmt:list)->list:
            # THAT = *(FRAME - 1)
            stmt.append(f"@{frame}")
            stmt.append('A=M')
            for _ in range(num):
                stmt.append('A=A-1')
            stmt.append('D=M')
            stmt.append(f"@{symbol}")
            stmt.append('M=D')
            return stmt
        # frame = 'RETURN:FRAME'
        frame = 'R13'
        ret = 'R14'
        stmt = []
        # FRAME = LCL
        stmt.append('@LCL')
        stmt.append('D=M')
        stmt.append(f"@{frame}")
        stmt.append('M=D')
        # RET = *(FRAME - 5)
        stmt.append('@LCL')
        stmt.append('D=M')
        for _ in range(5):
            stmt.append('D=D-1')
        stmt.append(f"@{ret}")
        stmt.append('M=D')
        # *ARG = pop()
        stmt = self.__backward_sp(stmt)
        stmt.append('@SP')
        stmt.append('A=M')
        stmt.append('D=M')
        stmt.append('@ARG')
        stmt.append('A=M')
        stmt.append('M=D')
        # SP = ARG + 1
        stmt.append('@ARG')
        stmt.append('A=M')
        stmt.append('D=A+1')
        stmt.append('@SP')
        stmt.append('M=D')
        # THAT = *(FRAME - 1)
        stmt = backward(frame, 'THAT', 1, stmt)
        # THIS = *(FRAME - 2)
        stmt = backward(frame, 'THIS', 2, stmt)
        # ARG = *(FRAME - 3)
        stmt = backward(frame, 'ARG', 3, stmt)
        # LCL = *(FRAME - 4)
        stmt = backward(frame, 'LCL', 4, stmt)
        # goto RET
        stmt.append(f"@{ret}")
        stmt.append('A=M')
        stmt.append('0;JMP')
        self.__write(stmt)
    def write_function(self, function_name: str, num_locals: int):
        """
        fuctionコマンドを行うアセンブリコードを書く
        """
        self.__functionname = function_name
        stmt = []
        stmt.append(f"({function_name})")
        # progress SP to num_locals
        for _ in range(num_locals):
            stmt = self.__forward_sp(stmt)
        # initialize LCL 0
        stmt.append('@LCL')
        stmt.append('A=M')
        for _ in range(num_locals - 1):
            stmt.append('M=0')
            stmt.append('A=A+1')
        stmt.append('M=0')
        self.__write(stmt)        
    def close(self):
        """
        出力ファイルを閉じる。
        """
        if not self.__fw:
            return
        self.__fw.close()
    def __write(self, stmt: list):
        if not self.__is_done_init:
            return
        self.__fw.write('\n'.join(stmt) + "\n")
    def __get_label(self, label:str)->str:
        return f"{self.__get_functionname()}${label}"
    def __get_functionname(self)->str:
        # return f"{self.__classname}.{self.__functionname}"
        return f"{self.__functionname}"
    def __forward_sp(self, stmt:list)->list:
        return self.__forward_ram_address('SP', stmt)
    def __backward_sp(self, stmt:list)->list:
        return self.__backward_ram_address('SP', stmt)    
    def __forward_ram_address(self, symbol:str, stmt:list)->list:
        # A = SYMBOL
        stmt.append(f"@{symbol}")
        # M[SYMBOL] = M[SYMBOL] + 1
        stmt.append('M=M+1')
        return stmt
    def __backward_ram_address(self, symbol:str, stmt:list)->list:
        # A = SYMBOL
        stmt.append(f"@{symbol}")
        # M[SYMBOL] = M[SYMBOL] - 1 # prev address
        stmt.append('M=M-1')
        return stmt







# EOF
