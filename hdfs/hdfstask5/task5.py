#! /user/bin/env pyhton3

from hdfs import Config
import os, re, sys

client = Config().get_client()
file_size = sys.argv[1]
stream = os.popen('dd if=/dev/zero of=myfile.txt bs=' + file_size + ' count=1')
output = stream.read()
stream_hdfs = os.popen('hdfs dfs -put myfile.txt myfile.txt')
output_hdfs = stream_hdfs.read()
stream_fsck = os.popen('hdfs fsck /user/$USER/myfile.txt -blocks -files -locations')
output_fsck = stream_fsck.read()
blocks_set = re.findall(r"blk_[0-9]*", output_fsck)
size = 0
for block_name in blocks_set:
    block_stream = os.popen('hdfs fsck -blockId ' + block_name)
    block_output = block_stream.read()
    replicas = re.findall(r"Block replica on datanode/rack: [\w + . + -]*/default is HEALTHY", block_output)
    if replicas:
        using_replica = replicas[0].split(" ")[4].split("/")[0]
        place_on_node_stream = os.popen('sudo -u hdfsuser ssh hdfsuser@' 
                + using_replica + ' find /dfs -name ' + block_name)
        output_place = place_on_node_stream.read()
        size_stream = os.popen('sudo -u hdfsuser ssh hdfsuser@' + using_replica + ' wc -c ' + output_place)
        size_output = size_stream.read()
        get = int(size_output.split(" ")[0])
        size += get
additional_inf = int(file_size) - size
stream_hdfs = os.popen('hdfs dfs -rm -skipTrash myfile.txt')
stream = os.popen('rm myfile.txt')
print(additional_inf)

