#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
program_filename = sys.argv[1]

cpu.load(program_filename)
cpu.run()

