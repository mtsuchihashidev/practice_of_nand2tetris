#!/usr/bin/python
# -*- coding: utf-8 -*-

class TokenType:
    @staticmethod
    def __eq__(self, other):
        return type(self) == type(other)

class T_KEYWORD(TokenType):
    pass

class T_SYMBOL(TokenType):
    pass

class T_IDENTIFIER(TokenType):
    pass

class T_INT_CONST(TokenType):
    pass

class T_STRING_CONST(TokenType):
    pass

# EOF
