#./build_web_image.sh
#./build_transaction_image.sh


#docker service update --force cluster_web_app
#docker service update --force cluster_transaction_server


./build_transaction_image.sh &
P2=$!
./build_monitor_image.sh &
P5=$!
wait $P2 $P5

docker service update --force cluster_transaction_server &
P4=$!
docker service update --force cluster_monitor_server &
P6=$!
wait $P4 $P6