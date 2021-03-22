docker swarm leave --force

docker build -t mongo_conf ./mongo_conf_image/
docker build -t web_app ./web_image/
docker build -t transaction_server ./transaction_image/
docker build -t monitor_server ./monitor_image/
docker build -t frontend_server ./frontend_image/

docker swarm init

./startCluster.sh