for i in "10000_20.txt"
do
	for pt in 1 2 3 4 5 6 7 8 9
	do
		for pg in 1 2 3 4 5 6 7 8 9
		do
			sed -i "s/^    observations_path.*/    observations_path=\"$i\"/g" sparkpybkt_hdfs_beta3.py
			spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 56 --executor-memory 1G sparkpybkt_hdfs_beta3.py $pt $pg
		done
	done
done
