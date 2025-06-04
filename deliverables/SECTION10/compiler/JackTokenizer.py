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
__KEYWORD__ = {
    'class': K_CLASS,
    'constructor': K_CONSTRUCTOR,
    'function': K_FUNCTION,
    'method': K_METHOD,
    'field': K_FIELD,
    'static': K_STATIC,
    'var': K_VAR,
    'int': K_INT,
    'char': K_CHAR,
    'boolean': K_BOOLEAN,
    'void': K_VOID,
    'true': K_TRUE,
    'false': K_FALSE,
    'null': K_NULL,
    'this': K_THIS,
    'let': K_LET,
    'do': K_DO,
    'if': K_IF,
    'else': K_ELSE,
    'while': K_WHILE,
    'return': K_RETURN
    }

RX_STR_CONST = re.compile(r'"[^"]*"', re.S)
RX_IDENTIFIER = re.compile(r'[A-Za-z][0-9A-Za-z]+', re.S)
RX_NUMBER = re.compile(r'[0-9]+', re.S)

class Tokenizer:
    def __init__(self, src:str):
        self.src = src
        self.limit = len(src)
        self.__tokens = []

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
            if j >= i:
                # print(f"identifier: (i, j) = ({i}, {j}): {self.fetch(i, j)}", file=sys.stderr)
                if j > i:
                    self.set_token(self.fetch(i, j))
                    i = j + 1
                else:
                    self.set_token(self.get(i))
                    i = i + 1
                continue
            j = self.fetch_blank(i)
            if j >= i:
                # print(f"blank: (i, j) = ({i}, {j})", file=sys.stderr)
                i = j
                continue
            i += 1

    def get_tokens(self):
        return self.__tokens

    def set_token(self, token:str):
        # print(token, file=sys.stderr)
        self.__tokens.append(token)

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
        if not self.is_upper_letter(c0) \
           and not self.is_lower_letter(c0):
            return -1
        j = s + 1
        while j < self.limit - 1:
            c1 = self.get(j)
            is_target = False
            is_target = is_target | self.is_lower_letter(c1)
            is_target = is_target | self.is_upper_letter(c1)
            is_target = is_target | self.is_number_letter(c1)
            if not is_target:
                return j - 1
            j += 1
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
        self.__tokens = tokenizer.get_tokens()
        print(self.__tokens)
        self.__cidx = -1
        self.__capacity = len(self.__tokens)
        self.__ctoken = ''


    def __is_symbol(self, char:str)->bool:
        return char in __SYMBOL__

    def has_more_tokens(self)->bool:
        return self.__cidx < self.__capacity

    def advance(self):
        self.__cidx += 1
        self.__ctoken = self.__tokens[self.__cidx]

    def token_type(self)->TokenType:
        if self.__cidx >= self.__capacity:
            raise Exception('no more token')
        if self.__ctoken in __KEYWORD__.keys():
            return T_KEYWORD
        elif self.__ctoken in __SYMBOL__:
            return T_SYMBOL
        elif RX_STR_CONST.match(self.__ctoken, re.S):
            return T_STRING_CONST
        elif RX_IDENTIFIER.match(self.__ctoken, re.S):
            return T_IDENTIFIER
        elif mo := RX_NUMBER.match(self.__ctoken, re.S):
            n = int(mo[0])
            if n >= 0 and n <= 32767:
                return T_INT_CONST
        raise Exepction(f"no support: {self.__ctoken}")

    def keyword(self)->KeywordType:
        if self.__ctoken not in __KEYWORD__.keys():
            raise Exception(f"no support: {self.__ctoken}")
        return __KEYWORD__[self.__ctoken]

    def symbol(self)->str:
        return self.__ctoken

    def identifier(self)->str:
        return self.__ctoken

    def int_val(self)->int:
        mo = RX_NUMBER.match(self.__ctoken, re.S)
        if not mo:
            raise Exception(f"no support: {self.__ctoken}")
        n = int(mo[0])
        if n < 0 or n > 32767:
            raise Exception(f"no support: {self.__ctoken}")
        return n

    def string_val(self)->str:
        # TODO remove "?
        return self.__ctoken




# EOF
