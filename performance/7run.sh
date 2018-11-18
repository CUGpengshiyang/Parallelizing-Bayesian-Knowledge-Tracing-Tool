#!/bin/sh
for j in 12 24 36 48 56
do
spark-submit --master yarn-cluster  --driver-memory 10G --num-executors $j --executor-memory 1G serial.py

done


