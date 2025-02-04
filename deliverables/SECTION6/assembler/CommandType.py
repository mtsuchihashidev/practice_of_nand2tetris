#!/usr/bin/python
# -*- coding: utf-8  -*-


class CommandType:
    @staticmethod
    def __eq__(self, other):
        return type(self) == type(other)

class A_COMMAND(CommandType):
    pass

class C_COMMAND(CommandType):
    pass

class L_COMMAND(CommandType):
    pass


# EOF
