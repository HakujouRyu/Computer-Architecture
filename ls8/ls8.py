#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
program_filename = sys.argv[1]
# program_filename = 'ls8/examples/call.ls8'
cpu.load(program_filename)
cpu.run()

