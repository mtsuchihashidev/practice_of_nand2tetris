#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import sys

from Base import Structure



class Term(Structure):
    @property
    def value(self):
        return self.__value

    def __init__(self, name, value):
        super().__init__(name)
        self.__value = value

    def operate(self, logic):
        logic.logic_term(self)

    def get_children(self)->Structure:
        return None

    def add(self, child: Structure)->bool:
        return False
    
    def remove(self, child: Structure)->bool:
        return False

class Node(Structure):
    def __init__(self, name):
        super().__init__(name)
        self.__children = []

    def operate(self, logic):
        # TODO
        logic.logic_node(self)

    def get_children(self)->Structure:
        return self.__children

    def add(self, child):
        self.__children.append(child)
        return True

    def remove(self, child: Structure):
        # TODO
        return True

    
class SKeyword(Term):
    def __init__(self, keyword:str):
        super().__init__('keyword', keyword)

class SSymbol(Term):
    def __init__(self, symbol):
        super().__init__('symbol', symbol)

class SIntegerConstant(Term):
    def __init__(self, int_const):
        super().__init__('integerConstant', int_const)

class SStringConstant(Term):
    def __init__(self, str_const):
        super().__init__('stringConstant', str_const)
    
class SIdentifier(Term):
    def __init__(self, identifier):
        super().__init__('identifier', identifier)
    
class SClass(Node):
    def __init__(self):
        super().__init__('class')

class SClassVarDec(Node):
    def __init__(self):
        super().__init__('classVarDec')

class SSubroutineDec(Node):
    def __init__(self):
        super().__init__('subroutineDec')

class SParameterList(Node):
    def __init__(self):
        super().__init__('parameterList')

class SSubroutineBody(Node):
    def __init__(self):
        super().__init__('subroutineBody')

class SVarDec(Node):
    def __init__(self):
        super().__init__('varDec')

class SStatements(Node):
    def __init__(self):
        super().__init__('statements')

class SLetStatement(Node):
    def __init__(self):
        super().__init__('letStatement')

class SDoStatement(Node):
    def __init__(self):
        super().__init__('doStatement')

class SIfStatement(Node):
    def __init__(self):
        super().__init__('ifStatement')

class SWhileStatement(Node):
    def __init__(self):
        super().__init__('whileStatement')

class SReturnStatement(Node):
    def __init__(self):
        super().__init__('returnStatement')

class SExpression(Node):
    def __init__(self):
        super().__init__('expression')

class STerm(Node):
    def __init__(self):
        super().__init__('term')

class SExpressionList(Node):
    def __init__(self):
        super().__init__('expressionList')

# EOF
