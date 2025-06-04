#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from os.path import splitext
import sys

from Structure import SKeyword, SSymbol, SIntegerConstant, \
    SStringConstant, SIdentifier, SClass, SClassVarDec

from Utils import Utils, Log


class OutputLogic(metaclass = ABCMeta):
    @abstractmethod
    def accept(self, structure):
        pass

class XmlParser:
    def __init__(self)
        pass
    def accept(self, structure):
        structure.operate(self)
        
        


    
# EOF
