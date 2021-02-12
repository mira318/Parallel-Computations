#!/usr/bin/env bash
OUT_DIR="streaming_task1_result"
NUM_REDUCERS=8

hadoop fs -rm -r -skipTrash ${OUT_DIR} >> /dev/null

hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar >> /dev/null \
    -D mapreduce.job.name="task1_try_redo" \
    -D mapreduce.job.reducers=${NUM_REDUCERS} \
    -files mapper1.py,reducer1.py \
    -mapper 'python3 mapper1.py' \
    -reducer 'python3 reducer1.py' \
    -input /data/ids_part \
    -output ${OUT_DIR}

sum_count=0

for num in `seq 0 $(($NUM_REDUCERS - 1))`
do
    if [ $sum_count -lt 50 ]
    then 
        count=$(hadoop fs -cat ${OUT_DIR}/part-0000$num | wc -l)
	sum_count=$[$sum_count + $count]
        hdfs dfs -cat ${OUT_DIR}/part-0000$num | head -50
    fi
done
