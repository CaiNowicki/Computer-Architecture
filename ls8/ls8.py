#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            program = sys.argv[1]
            cpu = CPU()
            cpu.load(program)
            cpu.run()
        except FileNotFoundError:
            print("File Not Found")
    else:
        print("No program specified")