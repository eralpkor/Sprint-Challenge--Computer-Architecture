#!/usr/bin/env python3

import sys
import os
from cpu import *

# if len(sys.argv) != 2:
#     print("ERR: No file given:\t python ls8.py examples/file_name")
#     sys.exit(1)

# script_dir = os.path.dirname(__file__)
# file_name = sys.argv[1]
# arg handed should be a file path ex: examples/file_name
# file_path = os.path.join(script_dir, file_name)

if len(sys.argv) != 2:
    print('Usage: ls8.py filename')
    sys.exit(1)

program = sys.argv[1]

cpu = CPU()
# cpu.load("sctest.ls8")
cpu.load(program)
cpu.run()
