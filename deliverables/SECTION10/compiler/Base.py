#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Structure(metaclass = ABCMeta):
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


# EOF
