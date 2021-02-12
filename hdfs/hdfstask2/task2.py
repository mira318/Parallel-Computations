#! /user/bin/env python3

from hdfs import Config
import sys

client = Config().get_client()
filename = sys.argv[1]
with client.read(filename) as reader:
    ans = reader.read(10)
    print(ans.decode())
