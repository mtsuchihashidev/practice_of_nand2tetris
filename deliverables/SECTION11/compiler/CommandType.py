#!/usr/bin/python
# -*- coding: utf-8 -*-

class CommandType:
    @staticmethod
    def __eq__(self, other):
        return type(self) == type(other)

class C_ADD(CommandType):
    def __str__(self):
        return "add"
class C_SUB(CommandType):
    def __str__(self):
        return "sub"
class C_NEG(CommandType):
    def __str__(self):
        return "neg"
class C_EQ(CommandType):
    def __str__(self):
        return "eq"
class C_GT(CommandType):
    def __str__(self):
        return "gt"
class C_LT(CommandType):
    def __str__(self):
        return "lg"
class C_AND(CommandType):
    def __str__(self):
        return "and"
class C_OR(CommandType):
    def __str__(self):
        return "or"
class C_NOT(CommandType):
    def __str__(self):
        return "not"

# EOF
