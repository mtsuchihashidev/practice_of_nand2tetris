#!/usr/bin/python
# -*- coding: utf-8  -*-

class Code:
    def dest(self, mnemonic:str) -> str:
        if mnemonic == 'M':
            return '001'
        elif mnemonic == 'D':
            return '010'
        elif mnemonic == 'MD':
            return '011'
        elif mnemonic == 'A':
            return '100'
        elif mnemonic == 'AM':
            return '101'
        elif mnemonic == 'AD':
            return '110'
        elif mnemonic == 'AMD':
            return '111'
        else:
            # null
            return '000'

    def comp(self, mnemonic:str) -> str:
        if mnemonic == '0':
            return '0' + '101010'
        elif mnemonic == '1':
            return '0' + '111111'
        elif mnemonic == '-1':
            return '0' + '111010'
        elif mnemonic == 'D':
            return '0' + '001100'
        elif mnemonic == 'A':
            return '0' + '110000'
        elif mnemonic == 'M':
            return '1' + '110000'
        elif mnemonic == '!D':
            return '0' + '001111'
        elif mnemonic == '!A':
            return '0' + '110001'
        elif mnemonic == '!M':
            return '1' + '110001'
        elif mnemonic == '-D':
            return '0' + '001111'
        elif mnemonic == '-A':
            return '0' + '110011'
        elif mnemonic == '-M':
            return '1' + '110011'
        elif mnemonic == 'D+1':
            return '0' + '011111'
        elif mnemonic == 'A+1':
            return '0' + '110111'
        elif mnemonic == 'M+1':
            return '1' + '110111'
        elif mnemonic == 'D-1':
            return '0' + '001110'
        elif mnemonic == 'A-1':
            return '0' + '110010'
        elif mnemonic == 'M-1':
            return '1' + '110010'
        elif mnemonic == 'D+A':
            return '0' + '000010'
        elif mnemonic == 'D+M':
            return '1' + '000010'
        elif mnemonic == 'D-A':
            return '0' + '010011'
        elif mnemonic == 'D-M':
            return '1' + '010011'
        elif mnemonic == 'A-D':
            return '0' + '000111'
        elif mnemonic == 'M-D':
            return '1' + '000111'
        elif mnemonic == 'D&A':
            return '0' + '000000'
        elif mnemonic == 'D&M':
            return '1' + '000000'
        elif mnemonic == 'D|A':
            return '0' + '010101'
        elif mnemonic == 'D|M':
            return '1' + '010101'
        else:
            # TODO
            raise Exception()

    def jump(self, mnemonic:str) -> str:
        if mnemonic == 'JGT':
            return '001'
        elif mnemonic == 'JEQ':
            return '010'
        elif mnemonic == 'JGE':
            return '011'
        elif mnemonic == 'JLT':
            return '100'
        elif mnemonic == 'JNE':
            return '101'
        elif mnemonic == 'JLE':
            return '110'
        elif mnemonic == 'JMP':
            return '111'
        else:
            # null
            return '000'


# EOF
