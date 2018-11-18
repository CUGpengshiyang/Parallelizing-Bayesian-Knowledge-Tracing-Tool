for i in 10000 100000 1000000
do
	for j in 10 20 30
	do
		sed -i "s/^    observations_path.*/    observations_path=\"${i}_${j}.txt\"/g" sparkpybkt_hdfs_beta7.py
		spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 12 --executor-memory 1G sparkpybkt_hdfs_beta7.py
	done
done
for i in 10000 100000 1000000
do
	for j in 10 20 30
	do
		sed -i "s/^    observations_path.*/    observations_path=\"${i}_${j}.txt\"/g" sparkpybkt_hdfs_beta7.py
		spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 24 --executor-memory 1G sparkpybkt_hdfs_beta7.py
	done
done
for i in 10000 100000 1000000
do
	for j in 10 20 30
	do
		sed -i "s/^    observations_path.*/    observations_path=\"${i}_${j}.txt\"/g" sparkpybkt_hdfs_beta7.py
		spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 36 --executor-memory 1G sparkpybkt_hdfs_beta7.py
	done
done
for i in 10000 100000 1000000
do
	for j in 10 20 30
	do
		sed -i "s/^    observations_path.*/    observations_path=\"${i}_${j}.txt\"/g" sparkpybkt_hdfs_beta7.py
		spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 48 --executor-memory 1G sparkpybkt_hdfs_beta7.py
	done
done
for i in 10000 100000 1000000
do
	for j in 10 20 30
	do
		sed -i "s/^    observations_path.*/    observations_path=\"${i}_${j}.txt\"/g" sparkpybkt_hdfs_beta7.py
		spark-submit --master yarn-cluster  --driver-memory 10G --num-executors 56 --executor-memory 1G sparkpybkt_hdfs_beta7.py
	done
done
