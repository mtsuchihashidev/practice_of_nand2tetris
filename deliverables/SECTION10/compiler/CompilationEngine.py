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
from Logic import XmlLogic
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
        self.compile_subroutine()
        
        self.__root = pre_root

        # # }
        sclass.add(SSymbol(tkn.symbol()))

        logic = XmlLogic(self.__basename)
        sclass.operate(logic)
        logic.write()

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

            # type
            tkn.advance()
            if not self.__compile_type(scvd):
                raise Exception()

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

    def __compile_type(self, node):
        tkn = self.__tokenizer
        if tkn.token_type() == T_KEYWORD():
            kwd = tkn.kewword()
            if kwd == K_INT:
                node.add(SKeyword('int'))
            elif kwd == K_CHAR:
                node.add(SKeyword('char'))
            elif kwd == K_BOOLEAN:
                node.add(SKeyword('boolean'))
            else:
                return False
        elif tkn.token_type() == T_IDENTIFIER:
            node.add(SIdentifier(tkn.identifier()))
        else:
            return False
        return True

    def compile_subroutine(self):
        """メソッド、ファンクション、コンストラクタをコンパイルする
        """
        tkn = self.__tokenizer
        while True:
            # ('constructor', 'function', 'method')
            if tkn.token_type() != T_KEYWORD:
                raise Exception()
            kwd = tkn.keyword()
            ssbd = SSubroutineDec()
            self.__root.add(ssbd)
            if kwd = K_CONSTRUCTOR:
                ssbd.add(SKeyword('constructor'))
            elif kwd == K_FUNCTION:
                ssbd.add(SKeyword('function'))
            elif kwd == K_METHOD:
                ssbd.add(SKeyword('method'))
            else:
                raise Exception()

            # ('void', type)
            tkn.advance()
            if tkn.token_type() == T_KEYWORD:
                kwd = tkn.kewword()
                if kwd == K_VOID:
                    ssbd.add(SKeyword('void'))
                else:
                    if not self.__compile_type(ssbd):
                        raise Exception()
            else:
                if not self.__compile_type(ssbd):
                    raise Exception()

            # subtoutineName
            tkn.advance()
            if tkn.token_type() != T_IDENTIFIER:
                raise Exception()
            ssbd.add(SIdentifier(tkn.identifier()))
            # '('
            tkn.advance()
            if tkn.token_type() != T_SYMBOL:
                raise Exception()
            ssbd.add(SSymbol(tkn.symbol()))
            # parameterList
            pre = self.__root
            tkn.advance()
            self.compile_parameter_list()
            self.__root = pre
            # ')'
            if tkn.token_type() != T_SYMBOL:
                raise Exception()
            ssbd.add(SSymbol(tkn.symbol()))

            # ** subroutineBody **
            # '{'
            tkn.advance()
            if tkn.token_type() != T_SYMBOL:
                raise Exception()
            ssbd.add(SSymbol(tkn.symbol()))
            # varDec*
            tkn.advance()
            pre = self.__root
            self.compile_varDec()
            self.__root = pre

            # statements
            pre = self.__root
            self.compile_statements()
            self.__root = pre
            # '}'
            tkn.advance()
            if tkn.token_type() != T_SYMBOL:
                raise Exception()
            ssbd.add(SSymbol(tkn.symbol()))

            tkn.advance()
            if tkn.token_type() == T_SYMBOL \
               and tkn.symbol() == '}':
                break

    def compile_parameter_list(self):
        """パラメータのリスト（空の可能性あり）をコンパイルする。
        カッコ”（）”は含まない。
        """
        tkn = self.__tokenizer

        # ((type varName) (',' type varName)*)?
        prms = SParameterList()
        self.__root.add(prms)

        # type
        if not self.__compile_type(prms):
            raise Exception

        # varName
        tkn.advance()
        if tkn.token_type() != T_IDENTIFIER:
            raise Exception()
        prms.add(SIdentifier(tkn.identifier()))

        tkn.advance()
        while tkn.token_type() == T_SYMBOL and tkn.symbol() == ',':
            prms.add(SSymbol(tkn.symbol()))
            # type
            if not self.__compile_type(prms):
                raise Exception

            # varName
            tkn.advance()
            if tkn.token_type() != T_IDENTIFIER:
                raise Exception()
            prms.add(SIdentifier(tkn.identifier()))

            tnk.advance()

    def compile_var_dec(self):
        """var宣言をコンパイルする
        """
        tkn == self.__tokenizer

        def is_var_dec():
            return tkn.token_type() == T_KEYWORD() and tkn.keyword() == K_VAR

        while is_var_dec():
            svd = SVarDec()
            self.__root.add(svd)
            # 'var' type varName (',' varName)* ';'
            # 'var'
            svd.add(SKeyword(tkn.keyword()))

            # type
            if not self.__compile_type(svd):
                raise Exception()

            # varName
            if tkn.token_type() != T_IDENTIFIER:
                raise Exception()
            svd.add(SIdentifier(tkn.identifier()))

            tkn.advance()
            while tkn.token_type() == T_SYMBOL and tkn.symbol() == ',':
                # ','
                svd.add(SSymbol(','))

                # varName
                if tkn.token_type() != T_IDENTIFIER:
                    raise Exception()
                svd.add(SIdentifier(tkn.identifier()))

                tkn.advance()
            # ';'
            svd.add(SSymbol(tkn.symbol()))

            tkn.advance()

    def compile_statements(self):
        """一連の文をコンパイルする。波括弧は含まない。
        """
        tkn = self.__tokenizer

        sstmts = SStatements()
        self.__root.add(sstmts)

        def is_statement():
            if not tkn.token_type() == T_KEYWORD:
                return False
            if tkn.keyrowd() not in (K_LET, K_IF, K_WHILE, \
                                     K_DO, K_RETURN):
                return False
            return True
            
        # statements*
        # --------------------
        # letStatement | ifStatement | whileStatement | doStatement | returnStatement
        pre = self.__root
        self.__root = sstmts
        while is_statement():
            kwd = tkn.keyword()
            if kwd == K_LET:
                self.compile_let()
            elif kwd == K_IF:
                self.compile_if()
            elif kwd == K_WHILE:
                self.compile_while()
            elif kwd == K_DO:
                self.compile_do()
            elif kwd == K_RETURN:
                self.compile_return()
        self.__root = pre
        

    def compile_let(self):
        """let文をコンパイルする
        """
        tkn = self.__tokenizer
        lstmt = SLetStatement()
        self.__root.add(lstmt)
        
        # 'let' varName ('[' expression ']' )? '=' expression ';'

        # 'let'
        lstmt.add(SKeyword('let'))

        # varName
        tkn.advance()
        lstmt.add(SIdentifier(tkn.identifier()))
        tkn.advance()
        if tkn.token_type() == T_SYMBOL and tkn.symbol() == '[':
            # '['
            lstmt.add(SSymbol(tkn.symbol()))
            # expression
            tkn.advance()
            pre = self.__root
            self.__root = lstmt
            self.compile_expression()
            self.__root = pre
            # ']'
            lstmt.add(SSymbol(tkn.symbol()))

            tkn.advance()
        # '='
        lstmt.add(SSymbol(tkn.symbol()))
        # expression
        tkn.advance()
        pre = self.__root
        self.__root = lstmt
        self.compile_expression()
        self.__root = pre
        # ';'
        lstmt.add(SSymbol(tkn.symbol()))

        tkn.advance()
        

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
