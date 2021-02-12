#!/user/bin/env python

import random, sys

inds = []
for line in sys.stdin:
    try:
        val_id, key = line.strip().split('\t', 1)
        inds.append(val_id)
    except ValueError as e:
        continue

    while len(inds) > 5:
        cur_print = random.randint(1, 5)
        for i in range(cur_print - 1):
            print(inds[i], end = ',')
        print(inds[cur_print - 1])
        for i in range(cur_print):
            del inds[0]

if inds:
    for i in range(len(inds) - 1):
        print(inds[i], end = ',')
    print(inds[len(inds) - 1])

