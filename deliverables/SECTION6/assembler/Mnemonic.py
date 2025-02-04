#!/usr/bin/python
# -*- coding: utf-8  -*-

class MnemonicBase:
    @property
    def binary(self):
        return self.__binary

    def __init__(self, binary:str):
        self.__binary = binary

    @staticmethod
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.__binary == other.__binary

    def __str__(self):
        return self.__binary

class DEST(MnemonicBase):
    pass
    
class M(DEST):
    def __init__(self):
        super().__init__()
    

# EOF
