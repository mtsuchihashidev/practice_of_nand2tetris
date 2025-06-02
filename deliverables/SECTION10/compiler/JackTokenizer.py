#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re

from TokenType import T_KEYWORD, T_SYMBOL, T_IDENTIFIER, \
    T_INT_CONST, T_STRING_CONST, TokenType
from KeywordType import K_CLASS, K_METHOD, K_FUNCTION, \
    K_CONSTRUCTOR, K_INT, K_BOOLEAN, K_CHAR, K_VOID, \
    K_VAR, K_STATIC, K_FIELD, K_LET, K_DO, K_IF, K_ELSE,\
    K_WHILE, K_RETURN, K_TRUE, K_FALSE, K_NULL, K_THIS, \
    KeywordType
from Utils import Utils

__SYMBOL__ = set([
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', 
    '*', '/', '&', '|', '<', '>', '=', '~'
    ])
class Tokenizer:
    def __init__(self, src:str):
        self.src = src
        self.limit = len(src)
        self.tokens = []

    def tokenize(self):
        i = 0
        while i < self.limit:
            j = self.fetch_comment(i)
            if j >= i:
                # print(f"comment: (i, j) = ({i}, {j}): |{self.fetch(i,j)}|", file=sys.stderr)
                i = j + 1
                continue
            j = self.fetch_string_const(i)
            if j >= i:
                # print(f"string_const: (i, j) = ({i}, {j}): |{self.fetch(i, j )}|", file=sys.stderr)
                self.set_token(self.fetch(i, j))
                i = j
                continue
            j = self.fetch_symbol(i)
            if j >= i:
                # print(f"symbol: (i, j) = ({i}, {j}): {self.get(i)}", file=sys.stderr)
                self.set_token(self.get(i))
                i += 1
                continue
            j = self.fetch_identifier(i)
            if j > i:
                # print(f"identifier: (i, j) = ({i}, {j}): {self.fetch(i, j)}", file=sys.stderr)
                self.set_token(self.fetch(i, j))
                i = j
                continue
            j = self.fetch_blank(i)
            if j >= i:
                # print(f"blank: (i, j) = ({i}, {j})", file=sys.stderr)
                i = j
                continue
            i += 1

    def set_token(self, token:str):
        # print(token, file=sys.stderr)
        self.tokens.append(token)

    def get(self, i:int)->str:
        self.valid_range(i)
        return self.src[i]

    def fetch(self, s:int, e:int)->str:
        self.valid_range(s)
        self.valid_range(e)
        if s == e:
            raise Exception()
        return self.src[s:e+1] if s < e else self.src[e:s+1]

    def fetch_comment(self,s:int)->int:
        if s + 1 >= self.limit:
            return -1
        c0 = self.get(s)
        if c0 != '/':
            return -1
        c1 = self.get(s + 1)
        if c1 == '/':
            return self.fetch_line_comment(s + 1)
        elif c1 == '*':
            return self.fetch_block_comment(s + 1)
        return -1

    def fetch_line_comment(self, s:int)->int:
        i = s + 1
        while i < self.limit:
            c = self.get(i)
            if c == "\n":
                return i
            i += 1
        return -1

    def fetch_block_comment(self, s:int)->int:
        i = s + 1
        while i < self.limit - 1:
            c0 = self.get(i)
            if c0 != "*":
                i += 1
                continue
            c1 = self.get(i + 1)
            if c1 != "/":
                i += 1
                continue
            return i + 1
        return -1

    def fetch_symbol(self, i:int)->int:
        if self.get(i) not in __SYMBOL__:
            return -1
        return i

    def fetch_string_const(self, s:int)->int:
        c0 = self.get(s)
        if c0 != '"':
            return -1
        i = s + 1
        while i < self.limit:
            c1 = self.get(i)
            if c1 != '"':
                i += 1
                continue
            return i
        return -1

    def fetch_blank(self, s:int)->int:
        c0 = self.get(s)
        mo = re.match(r'[\s\n\r\t]+', c0, re.S)
        if not mo:
            return -1
        return mo.span()[1]

    def fetch_identifier(self, s:int)->int:
        c0 = self.get(s)
        if not self.is_upper_letter(c0) and not self.is_lower_letter(c0):
            return -1
        j = s + 1
        while j < self.limit - 1:
            c1 = self.get(j)
            if self.is_lower_letter(c1):
                j += 1
                continue
            if self.is_upper_letter(c1):
                j += 1
                continue
            if self.is_number_letter(c1):
                j += 1
                continue
            return j - 1
        return -1

    def is_upper_letter(self, s:str)->bool:
        return ord('A') <= ord(s) and ord(s) <= ord('Z')

    def is_lower_letter(self, s:str)->bool:
        return ord('a') <= ord(s) and ord(s) <= ord('z')

    def is_number_letter(self, s:str)->bool:
        return ord('0') <= ord(s) and ord(s) <= ord('9')
    
    def valid_range(self, i:int):
        if 0 <= i and i < self.limit:
            return
        raise Exception(f"out of index: index: {i}")
    
class JackTokenizer:

    def __init__(self, filename:str):
        with open(filename, 'r') as fi:
            contents = fi.read()
        tokenizer = Tokenizer(contents)
        tokenizer.tokenize()
        self.__tokens = tokenizer.tokens
        print(self.__tokens)


    def __is_symbol(self, char:str)->bool:
        return char in __SYMBOL__

    def has_more_tokens(self)->bool:
        pass

    def advance(self):
        pass

    def token_type(self)->TokenType:
        pass

    def keyword(self)->KeywordType:
        pass

    def symbol(self)->str:
        pass

    def idenfitier(self)->str:
        pass

    def int_val(self)->int:
        pass

    def string_val(self)->str:
        pass


# EOF
