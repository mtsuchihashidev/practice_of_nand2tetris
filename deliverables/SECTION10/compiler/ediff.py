#!/usr/bin/python3
# -*- coding: utf-8 -*-
# easy differ
import sys
from os.path import basename


if __name__ == '__main__':
    if len(sys.argv) == 2:
        # expected_file = sys.argv[1] or ''
        # actual_file = sys.argv[2] or ''
        file_base = sys.argv[1] or ''
        expected_file = f"{file_base}.xml.dest"
        actual_file = f"{file_base}.xml"
    elif len(sys.argv) == 3:
        expected_file = sys.argv[1] or ''
        actual_file = sys.argv[2] or ''

    expected_list, actual_list = [], []
    with open(expected_file, 'r') as fi:
        expected_list = fi.readlines()
    with open(actual_file, 'r') as fi:
        actual_list = fi.readlines()

    is_ok = True
    e_len = len(expected_list)
    a_len = len(actual_list)
    if a_len != a_len:
        is_ok = False
        print(f"len -> e:{e_len}, a:{a_len}")
    term = min(e_len, a_len)
    for i in range(term):
        if i >= term - 1:
            break
        e = expected_list[i]
        a = actual_list[i]
        if a == e:
            continue
        is_ok = False
        print(f"{i: >3}: e{e}")
        print(f"{i: >3}: a{a}")
    
    print(f"{basename(actual_file): <20} result: {'OK' if is_ok else 'NG'}")

# EOF
