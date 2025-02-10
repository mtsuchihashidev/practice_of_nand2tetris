#!/usr/bin/python
# -*- coding: utf-8  -*-
class SymbolTable:
    def __init__(self):
        self.__rom_counter = 0
        self.__ram_counter = 16
        self.__tbl = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576
            }
    def addEntry(self, symbol:str, address:int):
        if self.contains(symbol) or not symbol or address < 0:
            return
        self.__tbl[symbol] = address

    def contains(self, symbol:str)->bool:
        return symbol in self.__tbl.keys()

    def getAddress(self, symbol:str)->int:
        return self.__tbl[symbol]

    def to_binary(self, num: int)->str:
        return f"{bin(num)[2:]:0>16}"


# EOF
