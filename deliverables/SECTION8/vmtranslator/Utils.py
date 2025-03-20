#!/usr/bin/python
# -*- coding: utf-8 -*-
from os.path import splitext, basename

class Utils:

    @staticmethod
    def get_corename(filename):
        return splitext(basename(filename))[0]

# EOF
