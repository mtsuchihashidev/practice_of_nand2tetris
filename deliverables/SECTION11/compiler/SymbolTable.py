#!/usr/bin/python3
# -*- coding: utf-8 -*-

class KindType:
    @staticmethod
    def __eq__(self, other):
        return type(self) == type(other)

class KIND_STATIC(KindType):
    pass
class KIND_FIELD(KindType):
    pass
class KIND_ARG(KindType):
    pass
class KIND_VAR(KindType):
    pass

class SymbolRecord:
    @property
    def name(self):
        return self.__name
    @property
    def id_type(self):
        return self.__id_type
    @property
    def kind(self):
        return self.__kind
    def __init__(self, name:str, id_type:str, kind:KindType):
        self.__name = name
        self.__id_type = id_type
        self.__kind = kind
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        is_same = True
        is_same = is_same & self.__name == other.__name
        is_same = is_same & self.__id_type == other.__id_type
        is_same = is_same & self.__kind == other.__kind
        return is_same
    def __hash__(self):
        result = 17
        result = 31 * result + hash(self.__name)
        result = 31 * result + hash(self.__id_type)
        result = 31 * result + hash(self.__kind)
        return result
    def __str__(self):
        return f"{self.name: <20}{self.id_type: <20}{self.kind: <20}"

class SymbolTable:
    def __init__(self):
        self.__class_symbols = {}
        self.__local_symbols = {}
        self.__counter = {
            KIND_STATIC: -1,
            KIND_FIELD: -1,
            KIND_ARG: -1,
            KIND_VAR: -1
            }

    def start_subroutine(self):
        self.__local_symbols = {}
        self.__counter[KIND_ARG] = -1
        self.__counter[KIND_VAR] = -1

    def define(self, name:str, id_type:str, kind:KindType):
        self.__counter[kind] += 1
        print(f"NAME: {name}, TYPE: {id_type}, KIND: {kind}, INDEX: {self.__counter[kind]}")
        recored = SymbolRecord(name, id_type, kind)
        if kind in (KIND_STATIC, KIND_FIELD):
            self.__class_symbols[recored] = self.__counter[kind]
        elif kind in (KIND_ARG, KIND_VAR):
            self.__local_symbols[recored] = self.__counter[kind]
        else:
            raise Exception()

    def var_count(self, kind:KindType)->int:
        return self.__counter[kind]

    def kind_of(self, name:str)->KindType:
        for k in self.__local_symbols.keys():
            if k.name != name:
                continue
            return k.kind
        for k in self.__class_symbols.keys():
            if k.name != name:
                continue
            return k.kind
        raise Exception()

    def type_of(self, name:str)->str:
        for k in self.__local_symbols.keys():
            if k.name != name:
                continue
            return k.id_type
        for k in self.__class_symbols.keys():
            if k.name != name:
                continue
            return k.id_type
        raise Exception()

    def index_of(self, name:str)->int:
        for k, v in self.__local_symbols.items():
            if k.name != name:
                continue
            return v
        for k, v in self.__class_symbols.keys():
            if k.name != name:
                continue
            return v
        raise Exception()

    def __str__(self):
        ret = []
        for i, k, v in enumerate(self.__class_symbols.items()):
            print(i, k, v)
            ret.append(f"{k}{v: <20}")
        return "\n".join(ret)

# EOF
