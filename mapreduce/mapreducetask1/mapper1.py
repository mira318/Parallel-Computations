#!/user/bin/env python

import sys
import random


for line in sys.stdin:
    inds = line.split(" ")
    for ind in inds:
        val = random.randint(0, 13)
        print("%s\t%d" % (ind.strip(), val))
