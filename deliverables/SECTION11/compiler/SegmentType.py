#!/usr/bin/python
# -*- coding: utf-8 -*-

class SegmentType:
    @staticmethod
    def __eq__(self, other):
        return type(self) == type(other)

class SEG_CONST(SegmentType):
    def __str__(self):
        return "constant"
class SEG_ARG(SegmentType):
    def __str__(self):
        return "argument"
class SEG_LOCAL(SegmentType):
    def __str__(self):
        return "local"
class SEG_STATIC(SegmentType):
    def __str__(self):
        return "static"
class SEG_THIS(SegmentType):
    def __str__(self):
        return "this"
class SEG_THAT(SegmentType):
    def __str__(self):
        return "that"
class SEG_POINTER(SegmentType):
    def __str__(self):
        return "pointer"
class SEG_TEMP(SegmentType):
    def __str__(self):
        return "temp"

# EOF
