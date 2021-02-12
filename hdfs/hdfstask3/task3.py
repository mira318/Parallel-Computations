#! /user/bin/env python3

from hdfs import Config
import os, re, sys

client = Config().get_client()
filename = sys.argv[1]
stream = os.popen('hdfs fsck ' + filename + ' -blocks')
ans = stream.read()
string_found = re.findall(r"Total blocks [\w + \d + ( + ) + : + . + \t]*", ans)
set_found_number = re.findall(r"\d+", string_found[0])
print(set_found_number[0])
