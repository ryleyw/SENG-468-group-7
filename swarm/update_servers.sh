#./build_web_image.sh
#./build_transaction_image.sh


#docker service update --force cluster_web_app
#docker service update --force cluster_transaction_server


./build_web_image.sh &
P1=$!
./build_transaction_image.sh &
P2=$!
wait $P1 $P2

docker service update --force cluster_web_app &
P3=$!
docker service update --force cluster_transaction_server &
P4=$!
wait $P3 $P4