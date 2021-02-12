from __future__ import print_function
from pyspark.sql import SparkSession
from pyspark.sql.types import *

import pyspark.sql.functions as f

if __name__ == "__main__":
    spark_session = SparkSession.builder.master("yarn").appName(
            "157 hw").config("spark.ui.port", "18089").getOrCreate()

    broadcast_const = 13
    partition_const = 500

    follower_schema = StructType(fields = [
        StructField("user_id", IntegerType()), 
        StructField("follower_id", IntegerType())
        ])

    followers_df = spark_session.read.format("csv").schema(
            follower_schema).option("sep", "\t").load(
                    "/data/twitter/twitter_sample.txt").repartition(
                            partition_const).cache()

    one_step_df = followers_df.filter("follower_id == 12").select(
            f.col("follower_id").alias("way"), 
            f.col("user_id").alias("follower_id"))

    depth = 0
    true_checker = 1
    false_checker = 0

    while true_checker and not false_checker:
        if(depth <= broadcast_const):
            one_step_df = followers_df.join(
                    f.broadcast(one_step_df), on = 'follower_id', 
                    how = 'inner').select(f.concat("way", f.lit(","), 
                        "follower_id").alias("way"), 
                        f.col("user_id").alias("follower_id")).cache()

        else:
            one_step_df = followers_df.join(
                    one_step_df, on = 'follower_id', 
                    how = 'inner').select(f.concat("way", f.lit(","), 
                        "follower_id").alias("way"), 
                        f.col("user_id").alias("follower_id")).cache()
                        
        true_checker = one_step_df.select(f.col("follower_id")).take(1)
        false_checker = one_step_df.filter("follower_id == 34").select(
                f.col("follower_id")).take(1)
        depth += 1

    vals = one_step_df.filter("follower_id == 34").take(1)
    for val in vals:
        print(val["way"], val["follower_id"], sep = ",")
