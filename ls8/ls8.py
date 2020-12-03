#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

if __name__ == '__main__':
    program = sys.argv[1]
    cpu = CPU()
    cpu.load(program)
    cpu.run()