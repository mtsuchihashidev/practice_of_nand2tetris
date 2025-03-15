#!/usr/bin/python
# -*- coding: utf-8 -*-

class CommandType:
    @staticmethod
    def __eq__(self, other):
        return type(self) == type(other)

class C_ARITHMETIC(CommandType):
    pass

class C_PUSH(CommandType):
    pass

class C_POP(CommandType):
    pass

class C_LABEL(CommandType):
    pass

class C_GOTO(CommandType):
    pass

class C_IF(CommandType):
    pass

class C_FUNCTION(CommandType):
    pass

class C_RETURN(CommandType):
    pass

class C_CALL(CommandType):
    pass

# EOF
