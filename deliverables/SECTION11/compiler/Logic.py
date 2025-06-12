#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from xml.dom import minidom
import xml.etree.ElementTree as ET

from SymbolTable import SymbolTable, KIND_STATIC, KIND_FIELD, KIND_ARG, \
    KIND_VAR
from Structure import Term, Node, SKeyword, SSymbol, \
    SIntegerConstant, SStringConstant, SIdentifier, SClass, \
    SClassVarDec, SSubroutineDec, SParameterList, SSubroutineBody, \
    SVarDec, SStatements, SLetStatement, SDoStatement, SIfStatement, \
    SWhileStatement, SReturnStatement, SExpression, STerm, SExpressionList
from VMWrite import VMWriter



class Logic(metaclass = ABCMeta):
    @abstractmethod
    def logic_term(self, term:Term):
        pass
    @abstractmethod
    def logic_node(self, node:Node):
        pass
    @abstractmethod
    def write(self):
        pass

# can't execute. i guess i foot ElementTree's bug.
class XmlLogic(Logic):
    def __init__(self, filename):
        self.__filename = filename
        self.__root = None
        self.__current = None
        
    def logic_term(self, term):
        elm = ET.SubElement(self.__current, term.name)
        elm.text = f" {term.value} "

    def logic_node(self, node):
        pre = None
        if not self.__current:
            pre = ET.Element(node.name)
            self.__current = pre
        else:
            pre = self.__current
            self.__current = ET.SubElement(self.__current, node.name)
        print(f"self.__current: {self.__current}")
        for child in node.get_children():
            print(f"child: {child}")
            pre2 = self.__current
            child.operate(self)
        self.__current = pre

    def write(self):
        doc = minidom.parseString(ET.tostring(self.__current, 'utf-8'))  # , \
#                                               xml_declaration=False))
        with open(f"{self.__filename}.xml", 'w') as fo:
            doc.writexml(fo, encoding='utf-8', newl="\n", indent="", addindent="  ")

    def write_element(self, structure):
        doc = minidom.parseString(ET.tostring(structure, 'utf-8'))
        with open(f"{self.__filename}.xml", 'w') as fo:
            doc.writexml(fo, encoding='utf-8', newl="\n", indent="", addindent="  ")

# this is normaly executing.
class XmlLogic2(Logic):
    def __init__(self, filename):
        self.__filename = filename
        self.__root = None
        self.__current = None
        self.__indent = '  '
        self.__indent_level = 0
        self.__contents = ''
        
    def logic_term(self, term):
        indent = self.__indent * self.__indent_level
        elm = term.name
        val = term.value
        self.__contents += f"{indent}<{elm}> {val} </{elm}>\n"

    def logic_node(self, node):
        indent = self.__indent * self.__indent_level
        self.__contents += f"{indent}<{node.name}>\n"
        self.__indent_level += 1
        for child in node.get_children():
            child.operate(self)
        self.__indent_level -= 1
        self.__contents += f"{indent}</{node.name}>\n"

    def write(self):
        with open(f"{self.__filename}.xml", 'w', encoding='utf-8') as fo:
            fo.write(self.__contents)

class SymbolTableTest(Logic):
    def __init__(self, filename):
        self.__symbol_table = SymbolTable()
        self.__surrent_kind = None
        self.__current_id_type = ""
        cvd = SClassVarDec()
        pl = SParameterList()
        vd = SVarDec()
        self.__sym_tgt = set([cvd.name, pl.name, vd.name])

    def logic_term(self, term):
        pass

    def logic_node(self, node):
        # if node.name in self.__sym_tgt and len(node.get_children()) >= 3:
        if len(node.get_children()) >= 2 \
           and (node.name == 'classVarDec' \
                or node.name == 'varDec' \
                or node.name == 'parameterList'):
            print(f"TARGER: {node.name}")
            kind, id_type, name = None, "",  ""
            term_list = node.get_children()
            if node.name in ('classVarDec', 'varDec'):
                if node.name == 'classVarDec':
                    if term_list[0].value == 'static':
                        kind = KIND_STATIC
                    else:
                        kind = KIND_FIELD
                elif node.name == 'varDec':
                    kind = KIND_VAR
                id_type = term_list[1].value
                name = term_list[2].value
                self.__symbol_table.define(name, id_type, kind)
                if len(term_list) >= 4:
                    i = 3
                    while term_list[i].value == ',':
                        i += 1
                        name = term_list[i].value
                        self.__symbol_table.define(name, id_type, kind)
                        i += 1
            else:
                kind = KIND_ARG
                id_type = term_list[0].value
                name = term_list[1].value
                self.__symbol_table.define(name, id_type, kind)
                if len(term_list) >= 3:
                    i = 2
                    while term_list[i].value == ',':
                        i += 1
                        name = term_list[i].value
                        i += 1
                        id_type = term_list[i].value
                        self.__symbol_table.define(name, id_type, kind)
                        i += 1
        for child in node.get_children():
            child.operate(self)
        
    def write(self):
        pass

class VMCompiler(Logic):
    def __init__(self, filename):
        self.__symbol_table = SymbolTable()
        cvd = SClassVarDec()
        pl = SParameterList()
        vd = SVarDec()
        self.__sym_tgt = set([cvd.name, pl.name, vd.name])
        self.__vmwriter = VMWrite(filename)

    def logic_term(self, term):
        pass

    def logic_node(self, node):
        if node.name == 'class':
            # TODO initial call the class Main function main
            self.__class_name = node.value

        if len(node.get_children()) >= 2 \
           and (node.name == 'classVarDec' \
                or node.name == 'varDec' \
                or node.name == 'parameterList'):
            kind, id_type, name = None, "",  ""
            term_list = node.get_children()
            if node.name in ('classVarDec', 'varDec'):
                if node.name == 'classVarDec':
                    if term_list[0].value == 'static':
                        kind = KIND_STATIC
                    else:
                        kind = KIND_FIELD
                elif node.name == 'varDec':
                    kind = KIND_VAR
                id_type = term_list[1].value
                name = term_list[2].value
                self.__symbol_table.define(name, id_type, kind)
                if len(term_list) >= 4:
                    i = 3
                    while term_list[i].value == ',':
                        i += 1
                        name = term_list[i].value
                        self.__symbol_table.define(name, id_type, kind)
                        i += 1
            else:
                kind = KIND_ARG
                id_type = term_list[0].value
                name = term_list[1].value
                self.__symbol_table.define(name, id_type, kind)
                if len(term_list) >= 3:
                    i = 2
                    while term_list[i].value == ',':
                        i += 1
                        name = term_list[i].value
                        i += 1
                        id_type = term_list[i].value
                        self.__symbol_table.define(name, id_type, kind)
                        i += 1
        for child in node.get_children():
            child.operate(self)
        
    def write(self):
        print(self.__symbol_table)

if __name__ == '__main__':
    # simply testing
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
    lstmt.add(SSymbol(';'))

    dstmt = SDoStatement()
    stmt.add(dstmt)

    dstmt.add(SKeyword('do'))

    xml = XmlLogic2("test")
    c.operate(xml)
    xml.write()

# EOF
