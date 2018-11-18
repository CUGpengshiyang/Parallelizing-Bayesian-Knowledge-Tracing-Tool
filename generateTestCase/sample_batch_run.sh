for i in "100000_30.txt"
do
	sed -i "s/^    observations_path.*/    observations_path=\"$i\"/g" sparkpybkt_hdfs_beta3.py
	sh 3run.sh
done
for i in "100000_30.txt"
do
	sed -i "s/^    observations_path.*/    observations_path=\"$i\"/g" sparkpybkt_hdfs_beta5.py
	sh 5run.sh
done
for i in "100000_30.txt"
do
	sed -i "s/^    observations_path.*/    observations_path=\"$i\"/g" sparkpybkt_hdfs_beta6.py
	sh 6run.sh
done
