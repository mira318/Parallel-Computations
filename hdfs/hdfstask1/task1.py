#! /user/bin/env python

from hdfs import Config
import os, re, sys

client = Config().get_client()
filename = sys.argv[1]
stream = os.popen('hdfs fsck ' + filename + ' -blocks -files -locations')
output = stream.readlines()
if len(output) < 2:
    print("don't have that file")
else:
    trying_list = output[2].split(':')[1].split('_')
    stream = os.popen('hdfs fsck -blockId ' + trying_list[0] + '_' + trying_list[1])
    output = stream.read()
    healthy_node_list = re.findall(r"[\w + \d + . + / + -]+ is HEALTHY", output)
    if not healthy_node_list:
        print("no healthy nodes") 
    else:
        print(healthy_node_list[0].split('/')[0].strip())
