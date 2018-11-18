#!/bin/sh
spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 36 --executor-memory 3G sparkpybkt_hdfs_beta6.py
