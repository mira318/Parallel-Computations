#! /user/bin/env python3

from hdfs import Config
import os, re, sys

client = Config().get_client()
block_name = sys.argv[1]
stream = os.popen('hdfs fsck -blockId ' + block_name)
output = stream.read()
replicas = re.findall(r"Block replica on datanode/rack: [\w + . + -]*/default is HEALTHY", output)
if replicas:
    using_replica = replicas[0].split(" ")[4].split("/")[0]
    node_stream = os.popen('sudo -u hdfsuser ssh hdfsuser@' + using_replica + ' find /dfs -name ' + block_name)
    output_node = node_stream.read()
    print(using_replica + ':' + output_node.rstrip())

