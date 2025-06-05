#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

# from Base import Term, Node
from Base import Structure

# class Structure(metaclass = ABCMeta):
#     @abstractmethod
#     def operate(self, logic):
#         pass
#     @abstractmethod
#     def get_children(self):
#         pass
#     @abstractmethod
#     def add(self, child)->bool:
#         if not isfinstance(child, Structure):
#             raise Exception()
#         pass
#     @abstractmethod
#     def remove(self, child)->bool:
#         if not isfinstance(child, Structure):
#             raise Exception()
#         pass

class Term(Structure):
    @property
    def name(self):
        return self.__name
    @property
    def value(self):
        return self.__value

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def operate(self, logic):
        logic.logic_term(self)

    def get_children(self)->Structure:
        return None

    def add(self, child: Structure)->bool:
        print(f"Term.add: {child}")
        return False
    
    def remove(self, child: Structure)->bool:
        return False

class Node(Structure):
    @property
    def name(self):
        return self.__name

    def __init__(self, name):
        self.__name = name
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
    def __init__(self, str_cosnt):
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
        super().__init__('paramerterList')

class SSubroutineBody(Node):
    def __init__(self):
        super().__init__('subroutineBody')

class SVarDec(Node):
    def __init__(self):
        super().__init__('varDec')

class SStatements(Node):
    def __init__(self):
        super().__init__('statement')

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

class SExpression(Node):
    def __init__(self):
        super().__init__('expression')

class STerm(Node):
    def __init__(self):
        super().__init__('term')

class SExpressionList(Node):
    def __init__(self):
        super().__init__('expressionList')

        
# TODO add more structures

if __name__ == '__main__':
    c = SClass()

    # class
    c.add(SKeyword('class'))
    # className
    c.add(SIdentifier('Main'))
    c.add(SSymbol('{'))

    # classVarDec
    cvd = SClassVarDec()
    c.add(cvd)
    cvd.add(SKeyword('static'))
    cvd.add(SKeyword('boolean'))
    cvd.add(SIdentifier('test'))
    cvd.add(SSymbol(';'))

    
    # subroutineDec
    sd = SSubroutineDec()
    c.add(sd)
    sd.add(SKeyword('function'))
    sd.add(SKeyword('void'))
    sd.add(SIdentifier('main'))
    sd.add(SSymbol('('))
    pl = SParameterList()
    sd.add(pl)
    sd.add(SSymbol(')'))

    sbdy = SSubroutineBody()
    sd.add(sbdy)
    sbdy.add(SSymbol('{'))

    v = SVarDec()
    sbdy.add(v)
    v.add(SKeyword('var'))
    v.add(SIdentifier('SquareGame'))
    v.add(SIdentifier('game'))
    v.add(SSymbol(';'))

    stmt = SStatements()
    sbdy.add(stmt)

    lstmt = SLetStatement()
    stmt.add(lstmt)
    lstmt.add(SKeyword('let'))
    lstmt.add(SIdentifier('game'))
    lstmt.add(SSymbol('='))
    
    exps = SExpression()
    lstmt.add(exps)

    trm = STerm()
    exps.add(trm)
    trm.add(SIdentifier('SquareGame'))
    trm.add(SSymbol('.'))
    trm.add(SIdentifier('new'))
    trm.add(SSymbol('('))

    expsl = SExpressionList()
    trm.add(expsl)

    trm.add(SSymbol(')'))
    lstmt.add(SSymbol('='))
    










# EOF
