#!/bin/sh
spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 128 --executor-memory 10G sparkpybkt_hdfs_beta3.py
