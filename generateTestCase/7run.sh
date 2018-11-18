#!/bin/sh
spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 56 --executor-memory 1G sparkpybkt_hdfs_beta7.py
