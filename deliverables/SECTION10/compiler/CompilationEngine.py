#!/usr/bin/python
# -*- coding: utf-8 -*-
from os.path import splitext
import sys

from KeywordType import K_CLASS, K_METHOD, K_FUNCTION, \
    K_CONSTRUCTOR, K_INT, K_BOOLEAN, K_CHAR, K_VOID, \
    K_VAR, K_STATIC, K_FIELD, K_LET, K_DO, K_IF, K_ELSE,\
    K_WHILE, K_RETURN, K_TRUE, K_FALSE, K_NULL, K_THIS, \
    KeywordType
from JackTokenizer import JackTokenizer
from Structure import SKeyword, SSymbol, SIntegerConstant, \
    SStringConstant, SIdentifier, SClass, SClassVarDec

from Utils import Utils, Log



class CompilationEngine:
    
    def __init__(self, tokenizer:JackTokenizer, file_basename):
        self.__tokenizer = tokenizer
        self.__basename = file_basename
        self.__root = None

    def compile_class(self):
        tkn = self.__tokenizer
        sclass = SClass()

        # class
        tkn.advance()
        tkn.keyword()
        sclass.add(SKeyword('class'))
        self.__root = sclass

        # className
        tkn.advance()
        class_name = tkn.identifier()
        sclass.add(SIdentifier(class_name))

        # {
        tkn.advance()
        sclass.add(SSymbol(tkn.symbol()))



        pre_root = self.__root
        # classVarDec*
        tkn.advance()
        self.compile_class_var_dec()

        # subroutineDec*
        #self.compile_subroutine()
        
        self.__root = pre_root

        # # }
        # tkn.advance()
        # sclass.add(SSymbol(tkn.symbol()))

    def compile_class_var_dec(self):
        tkn = self.__tokenizer
        while True:
            kwd = tkn.keyword()
            scvd = SClassVarDec()
            key = None
            if kwd == K_STATIC:
                scvd.add(SKeyword('static'))
            elif kwd == K_FIELD:
                scvd.add(SKeyword('field'))
            else:
                return
        
            tkn.advance()
            var_type = tkn.identifier()
            scvd.add(SIdentifier(var_type))

            tkn.advance()
            var_name = tkn.identifier()
            scvd.add(SIdentifier(var_name))
        
            tkn.advance()
            sym = tkn.symbol()
            while sym == ',':
                scvd.add(SSymbol(sym))
                tkn.advance()
                scvd.add(SIdentifier(tkn.identifier()))
                tkn.advance()
                sym = tkn.symbol()
            scvd.add(SSymbol(sym))
            self.__root.add(scvd)
            tkn.advance()
        

    def compile_subroutine(self):
        """メソッド、ファンクション、コンストラクタをコンパイルする
        """
        # ('constructor', 'function', 'method')
        # ('void', type)
        # subtoutineName
        # '('
        # parameterList
        # self.compile_parameter_list()
        # ')'
        # ** subroutineBody **
        # '{'
        # varDec*
        # self.compile_varDec()
        # statements
        # self.compile_statements()
        # '}'
        pass

    def compile_parameter_list(self):
        """パラメータのリスト（空の可能性あり）をコンパイルする。
        カッコ”（）”は含まない。
        """
        # ((type varName) (',' type varName)*)?
        pass

    def compile_var_dec(self):
        """var宣言をコンパイルする
        """
        # 'var' type varName (',' varName)* ';'
        pass

    def compile_statements(self):
        """一連の文をコンパイルする。波括弧は含まない。
        """
        # statements*
        # --------------------
        # letStatement | ifStatement | whileStatement | doStatement | returnStatement
        pass

    def compile_do(self):
        """do文をコンパイルする
        """
        # 'do' subroutineCall ';'

        # 'do'
        # ....
        # subroutineCall
        # ----
        # subroutineName '(' expressionList ')' |
        #    (className | varName) '.' subroutineName '(' expressionList ')'

        # ';'
        pass

    def compile_let(self):
        """let文をコンパイルする
        """
        # 'let' varName ('[' expression ']' )? '=' expression ';'
        pass

    def compile_while(self):
        """while文をコンパイルする
        """
        # 'while' '(' expression ')' '{' statements '}'
        pass

    def compile_return(self):
        """return文をコンパイルする
        """
        # 'return' expression? ';'
        pass

    def compile_if(self):
        """if文をコンパイルする
        """
        # 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        pass

    def compile_expression(self):
        """式をコンパイルする
        """
        # term (op term)*

        # <<<op>>>
        # '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        pass

    def compile_term(self):
        """
        """
        # integerConstant |
        # stringConstant |
        # keywordConstant |
        # varNaem |
        # varName '[' expression ']' |
        # subroutineCall |
        # '(' expression ')' |
        # unaryOp term


        # <<<subroutineCall>>>
        # subroutineName '(' expressionList ')' |
        #    (className | varName) '.' subroutineName '(' expressionList ')'

        # <<<unaryOp>>>
        # '-' | '~'

        # <<<keyrowdConstant>>>
        # 'true' | 'false' | 'null' | 'this'

        pass

    def compile_expression_list(self):
        """
        """
        # (expression (',' expression)* )?
        pass

    
# EOF
