#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Structure(metaclass = ABCMeta):
    @abstractmethod
    def operate(self):
        pass
    @abstractmethod
    def get_children(self):
        pass
    @abstractmethod
    def add(self, child)->bool:
        if not isfinstance(child, Structure):
            raise Exception()
        pass
    @abstractmethod
    def remove(self, child)->bool:
        if not isfinstance(child, Structure):
            raise Exception()
        pass

class SKeyword(Structure):
    def __init__(self, keyword):
        self.__value = keyword

    def operate(self):
        pass

    def get_children(self)->Structure:
        return None

    def add(self, child: Structure)->bool:
        return False

    def remove(self, child: Structure)->bool:
        return False

class SSymbol(Structure):
    def __init__(self, symbol):
        self.__value = symbol

    def operate(self):
        pass

    def get_children(self)->Structure:
        return None

    def add(self, child: Structure)->bool:
        return False

    def remove(self, child: Structure)->bool:
        return False

class SIntegerConstant(Structure):
    def __init__(self, int_const):
        self.__value = int_const

    def operate(self):
        pass

    def get_children(self)->Structure:
        return None

    def add(self, child: Structure)->bool:
        return False

    def remove(self, child: Structure)->bool:
        return False
    
class SStringConstant(Structure):
    def __init__(self, str_cosnt):
        self.__value = str_const

    def operate(self):
        pass

    def get_children(self)->Structure:
        return None

    def add(self, child: Structure)->bool:
        return False

    def remove(self, child: Structure)->bool:
        return False
    
class SIdentifier(Structure):
    def __init__(self, identifier):
        self.__value = identifier

    def operate(self):
        pass

    def get_children(self)->Structure:
        return None

    def add(self, child: Structure)->bool:
        return False

    def remove(self, child: Structure)->bool:
        return False
    
class SClass(Structure):
    def __init__(self):
        self.__value = 'Class'
        self.__children = []
    def operate(self):
        pass
    def get_children(self)->Structure:
        return self.__children
    def add(self, child: Structure):
        self.__children.append(child)
    def remove(self, child: Structure):
        # TODO
        pass
        
# TODO add more structures

if __name__ == '__main__':
    c = SClass()

# EOF
