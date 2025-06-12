#!/usr/bin/python
# -*- coding: utf-8 -*-
from os.path import splitext
import sys

from TokenType import T_KEYWORD, T_SYMBOL, T_IDENTIFIER, \
    T_INT_CONST, T_STRING_CONST
from KeywordType import K_CLASS, K_METHOD, K_FUNCTION, \
    K_CONSTRUCTOR, K_INT, K_BOOLEAN, K_CHAR, K_VOID, \
    K_VAR, K_STATIC, K_FIELD, K_LET, K_DO, K_IF, K_ELSE, \
    K_WHILE, K_RETURN, K_TRUE, K_FALSE, K_NULL, K_THIS, \
    KeywordType
from JackTokenizer import JackTokenizer
from Structure import Term, Node, SKeyword, SSymbol, \
    SIntegerConstant, SStringConstant, SIdentifier, SClass, \
    SClassVarDec, SSubroutineDec, SParameterList, SSubroutineBody, \
    SVarDec, SStatements, SLetStatement, SDoStatement, SIfStatement, \
    SWhileStatement, SReturnStatement, SExpression, STerm, SExpressionList
# from Logic import XmlLogic2, VMCompiler, SymbolTableTest
from Utils import Utils, Log



class CompilationEngine:
    @property
    def logic(self):
        return self.__logic
    @logic.setter
    def logic(self, cls):
        self.__logic = cls(self.__basename)

    def __init__(self, tokenizer:JackTokenizer, file_basename):
        self.__tokenizer = tokenizer
        self.__basename = file_basename
        self.__root = None
        self.__logic = None

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

        # logic = XmlLogic2(self.__basename)
        # logic = SymbolTableTest(self.__basename)
        # sclass.operate(logic)
        # logic.write()
        sclass.operate(self.__logic)
        self.__logic.write()

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
        print(f"START: __compile_type", file=sys.stderr)
        if tkn.token_type() == T_KEYWORD:
            kwd = tkn.keyword()
            if kwd == K_INT:
                print(f"     : __compile_type: ini", file=sys.stderr)
                node.add(SKeyword('int'))
            elif kwd == K_CHAR:
                print(f"     : __compile_type: char", file=sys.stderr)
                node.add(SKeyword('char'))
            elif kwd == K_BOOLEAN:
                print(f"     : __compile_type: boolean", file=sys.stderr)
                node.add(SKeyword('boolean'))
            else:
                tkn.advance()
                print(f"END  : __compile_type: False", file=sys.stderr)
                return False
        elif tkn.token_type() == T_IDENTIFIER:
            print(f"     : __compile_type: {tkn.identifier()}", file=sys.stderr)
            node.add(SIdentifier(tkn.identifier()))
        else:
            tkn.advance()
            print(f"END  : __compile_type: False", file=sys.stderr)
            return False
        tkn.advance()
        print(f"END  : __compile_type: True", file=sys.stderr)
        return True

    def compile_subroutine(self):
        """メソッド、ファンクション、コンストラクタをコンパイルする
        """
        tkn = self.__tokenizer
        print(f"START: compile_subroutine.subroutineName: {tkn.token_type()}", file=sys.stderr)
        while True:
            # ('constructor', 'function', 'method')
            if tkn.token_type() != T_KEYWORD:
                raise Exception()
            kwd = tkn.keyword()
            ssbd = SSubroutineDec()
            self.__root.add(ssbd)
            print(f"     : compile_subroutine.keyword: {tkn.keyword()}", file=sys.stderr)
            if kwd == K_CONSTRUCTOR:
                print(f"     : compile_subroutine.constructor", file=sys.stderr)
                ssbd.add(SKeyword('constructor'))
            elif kwd == K_FUNCTION:
                print(f"     : compile_subroutine.function", file=sys.stderr)
                ssbd.add(SKeyword('function'))
            elif kwd == K_METHOD:
                print(f"     : compile_subroutine.method", file=sys.stderr)
                ssbd.add(SKeyword('method'))
            else:
                raise Exception(f"no support: {tkn.keyword()}")

            # ('void', type)
            tkn.advance()
            if tkn.token_type() == T_KEYWORD:
                kwd = tkn.keyword()
                if kwd == K_VOID:
                    print(f"     : compile_subroutine.type: void", file=sys.stderr)
                    ssbd.add(SKeyword('void'))
                    tkn.advance()
                else:
                    if not self.__compile_type(ssbd):
                        raise Exception()
            else:
                if not self.__compile_type(ssbd):
                    raise Exception()

            # subtoutineName
            print(f"     : compile_subroutine.subroutineName: {tkn.token_type()}", file=sys.stderr)
            if tkn.token_type() != T_IDENTIFIER:
                raise Exception()
            print(f"     : compile_subroutine.subroutineName: {tkn.identifier()}", file=sys.stderr)
            ssbd.add(SIdentifier(tkn.identifier()))
            # '('
            tkn.advance()
            if tkn.token_type() != T_SYMBOL:
                raise Exception()
            print(f"     : compile_subroutine: (", file=sys.stderr)
            ssbd.add(SSymbol(tkn.symbol()))

            # parameterList
            tkn.advance()
            print(f"     : compile_subroutine.parameterList:", file=sys.stderr)
            self.__call(ssbd, self.compile_parameter_list)

            # ')'
            if tkn.token_type() != T_SYMBOL:
                raise Exception()
            print(f"     : compile_subroutine: (", file=sys.stderr)
            ssbd.add(SSymbol(tkn.symbol()))

            # ** subroutineBody **
            ssbb = SSubroutineBody()
            ssbd.add(ssbb)
            print(f"     : compile_subroutine.subroutineBody:", file=sys.stderr)
            # '{'
            tkn.advance()
            if tkn.token_type() != T_SYMBOL:
                raise Exception()
            print("     : compile_subroutine.subroutineBody: {", file=sys.stderr)
            ssbb.add(SSymbol(tkn.symbol()))
            # varDec*
            tkn.advance()
            self.__call(ssbb, self.compile_var_dec)
            print(f"     : compile_subroutine.subroutineBody.varDec:", file=sys.stderr)

            # statements
            self.__call(ssbb, self.compile_statements)
            print(f"     : compile_subroutine.subroutineBody.statements:", file=sys.stderr)
            # '}'
            # tkn.advance()
            if tkn.token_type() != T_SYMBOL:
                raise Exception()
            ssbb.add(SSymbol(tkn.symbol()))
            print("     : compile_subroutine.subroutineBody: } ", file=sys.stderr)

            # '} is class terminal
            tkn.advance()
            if tkn.token_type() == T_SYMBOL \
               and tkn.symbol() == '}':
                break

    def compile_parameter_list(self):
        """パラメータのリスト（空の可能性あり）をコンパイルする。
        カッコ”（）”は含まない。
        """
        tkn = self.__tokenizer
        prms = SParameterList()
        self.__root.add(prms)
        if tkn.token_type() == T_SYMBOL and tkn.symbol() == ')':
            return

        # ((type varName) (',' type varName)*)?
        # type
        if not self.__compile_type(prms):
            raise Exception

        # varName
        if tkn.token_type() != T_IDENTIFIER:
            raise Exception()
        prms.add(SIdentifier(tkn.identifier()))

        tkn.advance()
        while tkn.token_type() == T_SYMBOL and tkn.symbol() == ',':
            prms.add(SSymbol(tkn.symbol()))
            # type
            tkn.advance()
            if not self.__compile_type(prms):
                raise Exception

            # varName
            if tkn.token_type() != T_IDENTIFIER:
                raise Exception()
            prms.add(SIdentifier(tkn.identifier()))

            tkn.advance()

    def compile_var_dec(self):
        """var宣言をコンパイルする
        """
        tkn = self.__tokenizer

        def is_var_dec():
            return tkn.token_type() == T_KEYWORD and tkn.keyword() == K_VAR

        while is_var_dec():
            svd = SVarDec()
            self.__root.add(svd)
            # 'var' type varName (',' varName)* ';'
            # 'var'
            # svd.add(SKeyword(tkn.keyword()))
            svd.add(SKeyword('var'))
            tkn.advance()

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
                tkn.advance()

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
        print(f"START: compile_statements", file=sys.stderr)

        def is_statement():
            if not tkn.token_type() == T_KEYWORD:
                return False
            return tkn.keyword() in (K_LET, K_IF, K_WHILE, \
                                     K_DO, K_RETURN)
            
        # statements*
        # --------------------
        # letStatement | ifStatement | whileStatement | doStatement | returnStatement
        pre = self.__root
        self.__root = sstmts
        print(f"LOOPS: compile_statements", file=sys.stderr)
        while is_statement():
            kwd = tkn.keyword()
            print(f"     : compile_statements.keyword: {kwd}", file=sys.stderr)
            if kwd == K_LET:
                print(f"CALL : compile_statements: compile_let", file=sys.stderr)
                self.compile_let()
            elif kwd == K_IF:
                print(f"CALL : compile_statements: compile_if", file=sys.stderr)
                self.compile_if()
            elif kwd == K_WHILE:
                print(f"CALL : compile_statements: compile_while", file=sys.stderr)
                self.compile_while()
            elif kwd == K_DO:
                print(f"CALL : compile_statements: compile_do", file=sys.stderr)
                self.compile_do()
            elif kwd == K_RETURN:
                print(f"CALL : compile_statements: compile_return", file=sys.stderr)
                self.compile_return()
        self.__root = pre
        print(f"LOOPE: compile_statements", file=sys.stderr)
        print(f"END  : compile_statements", file=sys.stderr)

    def __call(self, container:Node, fn):
        pre = self.__root
        self.__root = container
        fn()
        self.__root = pre
        
    def compile_let(self):
        """let文をコンパイルする
        """
        tkn = self.__tokenizer
        lstmt = SLetStatement()
        self.__root.add(lstmt)
        print(f"START: compile_let", file=sys.stderr)
        
        # 'let' varName ('[' expression ']' )? '=' expression ';'

        # 'let'
        lstmt.add(SKeyword('let'))
        print(f"     : compile_let.keyword: let", file=sys.stderr)

        # varName
        tkn.advance()
        lstmt.add(SIdentifier(tkn.identifier()))
        print(f"     : compile_let.varName: {tkn.identifier()}", file=sys.stderr)
        tkn.advance()
        if tkn.token_type() == T_SYMBOL and tkn.symbol() == '[':
            # '['
            lstmt.add(SSymbol(tkn.symbol()))
            print(f"     : compile_let.symbol[[]: {tkn.symbol()}", file=sys.stderr)
            tkn.advance()
            # expression
            print(f"CALL : compile_let[compile_expression]", file=sys.stderr)
            self.__call(lstmt, self.compile_expression)
            # pre = self.__root
            # self.__root = lstmt
            # self.compile_expression()
            # self.__root = pre

            # ']'
            lstmt.add(SSymbol(tkn.symbol()))
            print(f"     : compile_let.symbol[]]: {tkn.symbol()}", file=sys.stderr)
            tkn.advance()
        # '='
        lstmt.add(SSymbol(tkn.symbol()))
        print(f"     : compile_let.symbol[=]: {tkn.symbol()}", file=sys.stderr)
        tkn.advance()
        # expression
        print(f"CALL : compile_let[compile_expression]", file=sys.stderr)
        self.__call(lstmt, self.compile_expression)
        # ';'
        lstmt.add(SSymbol(tkn.symbol()))
        print(f"     : compile_let.symbol[;]: {tkn.symbol()}", file=sys.stderr)
        tkn.advance()

        print(f"END  : compile_let", file=sys.stderr)
        return 

    def compile_do(self):
        """do文をコンパイルする
        """
        # 'do' subroutineCall ';'
        tkn = self.__tokenizer
        dstmt = SDoStatement()
        self.__root.add(dstmt)

        # 'do'
        dstmt.add(SKeyword('do'))
        
        # ....
        # subroutineCall
        # ----
        # subroutineName '(' expressionList ')' |
        #    (className | varName) '.' subroutineName '(' expressionList ')'

        tkn.advance()
        identifier = tkn.identifier()
        tkn.advance()
        symbol = tkn.symbol()
        if symbol == '(':
            # subroutineName
            dstmt.add(SIdentifier(identifier))
            # '('
            dstmt.add(SSymbol(symbol))
            # expressionList
            tkn.advance()
            self.__call(dstmt, self.compile_expression_list)
            # ')'
            dstmt.add(SSymbol(tkn.symbol()))
        elif symbol == '.':
            # className | varName
            dstmt.add(SIdentifier(identifier))
            # '.'
            dstmt.add(SSymbol(symbol))
            # subroutineName
            tkn.advance()
            dstmt.add(SIdentifier(tkn.identifier()))
            # '('
            tkn.advance()
            dstmt.add(SSymbol(tkn.symbol()))
            # expressionList
            tkn.advance()
            self.__call(dstmt, self.compile_expression_list)
            # ')'
            dstmt.add(SSymbol(tkn.symbol()))
        else:
            raise Exception()
        # ';'
        tkn.advance()
        dstmt.add(SSymbol(tkn.symbol()))

        tkn.advance()

    def compile_while(self):
        """while文をコンパイルする
        """
        # 'while' '(' expression ')' '{' statements '}'
        tkn = self.__tokenizer
        wstmt = SWhileStatement()
        self.__root.add(wstmt)

        # 'while'
        wstmt.add(SKeyword('while'))

        # '('
        tkn.advance()
        wstmt.add(SSymbol(tkn.symbol()))
        # expression
        tkn.advance()
        self.__call(wstmt, self.compile_expression)
        # ')'
        wstmt.add(SSymbol(tkn.symbol()))
        # '{'
        tkn.advance()
        wstmt.add(SSymbol(tkn.symbol()))
        # statements
        tkn.advance()
        self.__call(wstmt, self.compile_statements)
        # '}'
        wstmt.add(SSymbol(tkn.symbol()))
        
        tkn.advance()

    def compile_return(self):
        """return文をコンパイルする
        """
        # 'return' expression? ';'
        tkn = self.__tokenizer
        rstmt = SReturnStatement()
        self.__root.add(rstmt)

        # 'return'
        rstmt.add(SKeyword('return'))
        # expression?
        tkn.advance()
        if self.__is_next_term():
            self.__call(rstmt, self.compile_expression)
        # ';'
        rstmt.add(SSymbol(tkn.symbol()))

        tkn.advance()

    def compile_if(self):
        """if文をコンパイルする
        """
        # 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        tkn = self.__tokenizer
        istmt = SIfStatement()
        self.__root.add(istmt)
        print(f"START: compile_if", file=sys.stderr)

        # 'if'
        istmt.add(SKeyword('if'))
        print(f"     : compile_if.keyword: if", file=sys.stderr)
        tkn.advance()
        # '('
        istmt.add(SSymbol(tkn.symbol()))
        print(f"     : compile_if.symbol: {tkn.symbol()}", file=sys.stderr)
        tkn.advance()
        # expression
        print(f"     : compile_if.call[compile_expression]", file=sys.stderr)
        self.__call(istmt, self.compile_expression)
        # ')'
        istmt.add(SSymbol(tkn.symbol()))
        print(f"     : compile_if.symbol: {tkn.symbol()}", file=sys.stderr)
        tkn.advance()
        # '{'
        istmt.add(SSymbol(tkn.symbol()))
        print(f"     : compile_if.symbol: {tkn.symbol()}", file=sys.stderr)
        tkn.advance()
        # statements
        print(f"     : compile_if.call[compile_statements]", file=sys.stderr)
        self.__call(istmt, self.compile_statements)
        # '}'
        istmt.add(SSymbol(tkn.symbol()))
        print(f"     : compile_if.symbol: {tkn.symbol()}", file=sys.stderr)
        tkn.advance()
        # else
        if tkn.token_type() != T_KEYWORD or tkn.keyword() != K_ELSE:
            print(f"END  : compile_if", file=sys.stderr)
            return
        istmt.add(SKeyword('else'))
        print(f"     : compile_if.keyword: else", file=sys.stderr)
        tkn.advance()
        # '{'
        istmt.add(SSymbol(tkn.symbol()))
        print(f"     : compile_if.symbol: {tkn.symbol()}", file=sys.stderr)
        tkn.advance()
        # statements
        print(f"     : compile_if.call[compile_statements]", file=sys.stderr)
        self.__call(istmt, self.compile_statements)
        # '}'
        istmt.add(SSymbol(tkn.symbol()))
        print(f"     : compile_if.symbol: {tkn.symbol()}", file=sys.stderr)
        tkn.advance()

    def compile_expression(self):
        """式をコンパイルする
        """
        # term (op term)*
        tkn = self.__tokenizer
        exps = SExpression()
        self.__root.add(exps)
        print(f"START: compile_expression", file=sys.stderr)
              
        # <<<op>>>
        # '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='

        print(f"CALL : compile_expression[compile_term]", file=sys.stderr)
        self.__call(exps, self.compile_term)

        print(f"     : compile_expression.token_type: {tkn.token_type()}", file=sys.stderr)
        if tkn.token_type() == T_SYMBOL \
           and tkn.symbol() in ('+', '-', '*', '/', '&', \
                                   '|', '<', '>', '='):
            # parse
            if tkn.symbol() == '<':
                parsed_symbol = '&lt;'
            elif tkn.symbol() == '&':
                parsed_symbol = '&amp;'
            elif tkn.symbol() == '>':
                parsed_symbol = '&gt;'
            else:
                parsed_symbol = tkn.symbol()
            exps.add(SSymbol(parsed_symbol))
            print(f"     : compile_expression.symbol: {parsed_symbol}", file=sys.stderr)
            tkn.advance()
            print(f"CALL : compile_expression[compile_term]", file=sys.stderr)
            self.__call(exps, self.compile_term)
        print(f"END  : compile_expression", file=sys.stderr)
        return

    def __is_next_term(self)->bool:
        tkn = self.__tokenizer
        ttype = tkn.token_type()
        if ttype in (T_INT_CONST, T_STRING_CONST):
            return True
        elif ttype == T_KEYWORD:
            valid_keywords = (K_TRUE, K_FALSE, K_NULL, K_THIS)
            return tkn.keyword() in valid_keywords
        elif ttype == T_IDENTIFIER:
            # valid_symbol = ('[', '.', '(')
            # next_token = tkn.dry_advance()
            # return next_token in valid_symbol
            return True
        elif ttype == T_SYMBOL:
            valid_symbol = ('(', '-', '~')
            return tkn.symbol() in valid_symbol
        return False
        
    def compile_term(self):
        """
        """
        # integerConstant |
        # stringConstant |
        # keywordConstant |
        # varName |
        # varName '[' expression ']' |
        # subroutineCall |
        # '(' expression ')' |
        # unaryOp term
        tkn = self.__tokenizer
        trm = STerm()
        self.__root.add(trm)

        print(f"START: compile_term", file=sys.stderr)
        ttype = tkn.token_type()
        if ttype == T_INT_CONST:
            print(f"     : compile_term.int_const: {tkn.int_val()}", file=sys.stderr)
            trm.add(SIntegerConstant(tkn.int_val()))
            tkn.advance()
            print(f"END  : compile_term", file=sys.stderr)
            return
        elif ttype == T_STRING_CONST:
            print(f"     : compile_term.str_const: {tkn.string_val()}", file=sys.stderr)
            trm.add(SStringConstant(tkn.string_val()))
            tkn.advance()
            print(f"END  : compile_term", file=sys.stderr)
            return
        elif ttype == T_KEYWORD:
            valid_keywords = (K_TRUE, K_FALSE, K_NULL, K_THIS)
            if tkn.keyword() not in valid_keywords:
                raise Exception()
            if tkn.keyword() == K_TRUE:
                trm.add(SKeyword('true'))
                print(f"     : compile_term.keyword: true", file=sys.stderr)
            elif tkn.keyword() == K_FALSE:
                trm.add(SKeyword('false'))
                print(f"     : compile_term.keyword: false", file=sys.stderr)
            elif tkn.keyword() == K_NULL:
                trm.add(SKeyword('null'))
                print(f"     : compile_term.keyword: null", file=sys.stderr)
            elif tkn.keyword() == K_THIS:
                trm.add(SKeyword('this'))
                print(f"     : compile_term.keyword: this", file=sys.stderr)
            tkn.advance()
            print(f"END  : compile_term", file=sys.stderr)
            return
        elif ttype == T_IDENTIFIER:
            # varName | varName '[' expression ']' | subroutineCall |
            # <<<subroutineCall>>>
            # subroutineName '(' expressionList ')' |
            #    (className | varName) '.' subroutineName '(' expressionList ')'
            # =>
            # varName | varName '[' ... |
            # subroutineName '(' ... | (className|varName) '.' subroutineName

            # varName | subroutineName | className
            trm.add(SIdentifier(tkn.identifier()))
            print(f"     : compile_term.identifier: {tkn.identifier()}", file=sys.stderr)
            tkn.advance()
            # is SYMBOL '[' or '(' or '.' ?
            if tkn.token_type() != T_SYMBOL or tkn.symbol() not in ('[', '(', '.'):
                print(f"END  : compile_term", file=sys.stderr)
                return
            trm.add(SSymbol(tkn.symbol()))
            pre_symbol = tkn.symbol()
            tkn.advance()
            # '[' ?
            if pre_symbol == '[':
                print(f"     : compile_term.symbol: [", file=sys.stderr)
                self.__call(trm, self.compile_expression)
                print(f"     : compile_term.call[compile_expression]", file=sys.stderr)
                # ']'
                if tkn.token_type() != T_SYMBOL or tkn.symbol() != ']':
                    raise Exception(f"expected ']' but '{tkn.symbol()}'")
                trm.add(SSymbol(tkn.symbol()))
                print(f"     : compile_term.symbol: {tkn.symbol()}", file=sys.stderr)
                tkn.advance()
                print(f"END  : compile_term", file=sys.stderr)
                return
            # '('
            if pre_symbol == '(':
                print(f"     : compile_term.symbol: (", file=sys.stderr)
                self.__call(trm, self.compile_expression_list)
                print(f"     : compile_term.call[compile_expression_list]", file=sys.stderr)
                # ')'
                if tkn.token_type() != T_SYMBOL or tkn.symbol() != ')':
                    raise Exception(f"expected ')' but '{tkn.symbol()}'")
                trm.add(SSymbol(tkn.symbol()))
                print(f"     : compile_term.symbol: {tkn.symbol()}", file=sys.stderr)
                tkn.advance()
                print(f"END  : compile_term", file=sys.stderr)
                return
            if pre_symbol == '.':
                print(f"     : compile_term.symbol: .", file=sys.stderr)
                # subroutineName
                trm.add(SIdentifier(tkn.identifier()))
                print(f"     : compile_term.subrutineName: {tkn.identifier()}", file=sys.stderr)
                tkn.advance()
                # '('
                if tkn.token_type() != T_SYMBOL or tkn.symbol() != '(':
                    raise Exception(f"expected '(' but '{tkn.symbol()}'")
                trm.add(SSymbol(tkn.symbol()))
                print(f"     : compile_term.symbol: {tkn.symbol()}", file=sys.stderr)
                tkn.advance()
                # expressionList
                self.__call(trm, self.compile_expression_list)
                print(f"     : compile_term.call[compile_expression_list]", file=sys.stderr)
                # ')'
                if tkn.token_type() != T_SYMBOL or tkn.symbol() != ')':
                    raise Exception(f"expected ')' but '{tkn.symbol()}'")
                trm.add(SSymbol(tkn.symbol()))
                print(f"     : compile_term.symbol: {tkn.symbol()}", file=sys.stderr)
                tkn.advance()
                print(f"END  : compile_term", file=sys.stderr)
                return
            raise Exception()            
        elif ttype == T_SYMBOL:
            symbol = tkn.symbol()
            if symbol not in ('(', '-', '~'):
                raise Exception(f"term not support: [{symbol}]")
            # '(' expression ')' |
            if symbol == '(':
                # '('
                if tkn.token_type() != T_SYMBOL or tkn.symbol() != '(':
                    raise Exception(f"expected '(' but '{tkn.symbol()}'")
                trm.add(SSymbol(symbol))
                print(f"     : compile_term.symbol[(]: {tkn.symbol()}", file=sys.stderr)
                tkn.advance()

                # expression
                self.__call(trm, self.compile_expression)
                print(f"     : compile_term.call[compile_expression]", file=sys.stderr)

                # ")"
                if tkn.token_type() != T_SYMBOL or tkn.symbol() != ')':
                    raise Exception(f"expected ')' but '{tkn.symbol()}'")
                trm.add(SSymbol(tkn.symbol()))
                print(f"     : compile_term.symbol[)]: {tkn.symbol()}", file=sys.stderr)
                tkn.advance()
                print(f"END  : compile_term", file=sys.stderr)
                return
            # unaryOp term
            if symbol in ('-', '~'):
                if tkn.token_type() != T_SYMBOL or tkn.symbol() not in ('-', '~'):
                    raise Exception(f"expected '-' or '~'  but '{tkn.symbol()}'")
                trm.add(SSymbol(symbol))
                print(f"     : compile_term.symbol[-|~]: {tkn.symbol()}", file=sys.stderr)
                tkn.advance()
                self.__call(trm, self.compile_term)
                print(f"     : compile_term.call[compile_term]", file=sys.stderr)
                print(f"END  : compile_term", file=sys.stderr)
                return
            raise Exception()
        else:
            raise Exception()

        # <<<keyrowdConstant>>>
        # 'true' | 'false' | 'null' | 'this'

        # <<<subroutineCall>>>
        # subroutineName '(' expressionList ')' |
        #    (className | varName) '.' subroutineName '(' expressionList ')'

        # <<<unaryOp>>>
        # '-' | '~'

    def compile_expression_list(self):
        """
        """
        tkn = self.__tokenizer
        explst = SExpressionList()
        self.__root.add(explst)
        if not self.__is_next_term():
            return
        # (expression (',' expression)* )?

        # expression
        self.__call(explst, self.compile_expression)
        # ','
        while tkn.token_type() == T_SYMBOL and tkn.symbol() == ',':
            explst.add(SSymbol(tkn.symbol()))
            tkn.advance()
            # expression
            self.__call(explst, self.compile_expression)


# EOF
