#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys


if __name__ == '__main__':
    # expected_file = sys.argv[1] or ''
    # actual_file = sys.argv[2] or ''
    file_base = sys.argv[1] or ''
    expected_file = f"{file_base}.xml.dest"
    actual_file = f"{file_base}.xml"

    expected_list, actual_list = [], []
    with open(expected_file, 'r') as fi:
        expected_list = fi.readlines()
    with open(actual_file, 'r') as fi:
        actual_list = fi.readlines()

    e_len = len(expected_list)
    a_len = len(actual_list)
    print(f"len -> e:{e_len}, a:{a_len}")
    term = min(e_len, a_len)
    for i in range(term):
        if i >= term - 1:
            break
        e = expected_list[i]
        a = actual_list[i]
        if a == e:
            continue
        print(f"{i: <3}: e{e}")
        print(f"{i: <3}: a{a}")
        
    


# EOF
