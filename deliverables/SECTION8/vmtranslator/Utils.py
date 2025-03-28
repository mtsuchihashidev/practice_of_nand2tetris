#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import sys
from os.path import splitext, basename

class Utils:

    @staticmethod
    def get_corename(filename):
        return splitext(basename(filename))[0]

class Log:
    __can_output = False
    @staticmethod
    def init(can_output:bool):
        Log.__can_output = can_output
    @staticmethod
    def debug(msg:str):
        if not Log.__can_output:
            return
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
        print(f"{timestamp} [DEBUG] - {msg}", file=sys.stderr)

# EOF
