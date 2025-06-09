#!/usr/bin/python
# -*- coding: utf-8 -*-

class KeywordType:
    @staticmethod
    def __eq__(self, other):
        return type(self) == type(other)

class K_CLASS(KeywordType):
    pass

class K_METHOD(KeywordType):
    pass

class K_FUNCTION(KeywordType):
    pass

class K_CONSTRUCTOR(KeywordType):
    pass

class K_INT(KeywordType):
    pass

class K_BOOLEAN(KeywordType):
    pass

class K_CHAR(KeywordType):
    pass

class K_VOID(KeywordType):
    pass

class K_VAR(KeywordType):
    pass

class K_STATIC(KeywordType):
    pass

class K_FIELD(KeywordType):
    pass

class K_LET(KeywordType):
    pass

class K_DO(KeywordType):
    pass

class K_IF(KeywordType):
    pass

class K_ELSE(KeywordType):
    pass

class K_WHILE(KeywordType):
    pass

class K_RETURN(KeywordType):
    pass

class K_TRUE(KeywordType):
    pass

class K_FALSE(KeywordType):
    pass

class K_NULL(KeywordType):
    pass

class K_THIS(KeywordType):
    pass

# EOF
