#!/usr/bin/env python
# encoding: utf-8

import sys
from tool import Tool

USAGE = '''
Use this script as:
    ./main.py <source file path>

    Example:
    ./main.py sample.pdf
'''

def process(source):
    try:
        tool = Tool(source)
        for each in tool.files:
            print(each)
    except Exception as e:
        print(e)
        return 2
    return 0

def main(_, source = None, *args):
    if args or not source:
        print (USAGE)
        return 1
    return process(source)

if __name__ == "__main__":
    exit(main(*list(sys.argv or [])))