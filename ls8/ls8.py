#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


# print(sys.argv[1])


cpu = CPU()

# print(sys.argv[1])

cpu.load(sys.argv[1])

cpu.run()



# print(cpu.reg)