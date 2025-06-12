#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Structure(metaclass = ABCMeta):
    @property
    def name(self):
        return self.__name

    def __init__(self, name):
        self.__name = name

    @abstractmethod
    def operate(self, logic):
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
    @staticmethod
    def __eq__(self, other):
        if type(self) == type(other):
            return True
        return self.name == other.name

    def __eq__(self, other):
        return self.__name == other.name

# EOF
