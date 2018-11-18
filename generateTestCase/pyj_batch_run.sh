for i in "10000_10.txt" "10000_20.txt" "10000_30.txt" "100000_10.txt" "100000_20.txt" "100000_30.txt" "1000000_10.txt" "1000000_20.txt" "1000000_30.txt"
do
	sed -i "s/^    observations_path.*/    observations_path=\"$i\"/g" sparkpybkt_hdfs_beta3.py
	sh 3run.sh
done
for i in "10000_10.txt" "10000_20.txt" "10000_30.txt" "100000_10.txt" "100000_20.txt" "100000_30.txt" "1000000_10.txt" "1000000_20.txt" "1000000_30.txt"
do
	sed -i "s/^    observations_path.*/    observations_path=\"$i\"/g" sparkpybkt_hdfs_beta7.py
	sh 7run.sh
done


