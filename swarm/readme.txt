Troubleshooting:


To add more MongoDB shards, use the ./addShard.sh script.
(Run the command 'mongo'. If it doesn't connect you, keep waiting and try again.
 If it does connect you, from within the mongos shell, run the command 'sh.status()'
 and look for the 'shards' attribute to make sure s0 has been added already.
 If s0 has been added succesfully, you are safe to add more shards.)

To use the addShard.sh script, you must include the shard number:
$ shard=1 ./addShard.sh
If the shard number has already been created, the script will not run.
Use 'docker service ls' to get a list of all the currently running services.

To check if your shard has been added successfully, run the 'mongo' command then
from within the mongos shell, run the 'sh.status()' command and look at the 'shards'
attribute to see if your shard has been added yet.
It may take a few minutes but shouldn't take longer than 2-3 minutes.
If it isn't being added, you can use the following troubleshooting techniques:
docker service ls 	# find the conf service for your recently added shard number.
docker service logs <service_id>	# if this return blank, the mongo_conf image isn't even being created


From within the mongos router
use stocks
db.users.getShardDistribution() # this shows how the data has been distributed between the shards
sh.status() # this shows the status of your cluster (make sure all your shards show up)


If you want to deploy the swarm in a distributed fashion:
On the manager node, run > docker swarm init
Copy the full join token command that is printed.
On all other machines that you want to be worker nodes, paste that join token command.
(On the VMs, we first need to set them all to the same time since their times will be wildly different and the swarm won't work properly).
Once all the worker nodes are in the swarm, on the manager node, execute > ./startCluster.sh
This will start all of the services and containers across all of the nodes in the swarm.
(On the VMs, you may need to first run the swarm independently on each of them so that they download the necessary docker images first)

Troubleshooting:

# these are executed within the mongo shell
db.users.find() 	# view all current user documents in the db
db.users.remove({}) # delete all current user documents in the db

# these are executed within the terminal on the same machine as the swarm leader
docker service ps --no-trunc {serviceName}  # see why a service is crashing
docker service ls
docker service logs <service id>
docker logs <container_id>
docker system prune --volumes 	# delete many of your docker files which can fix certain problems
docker system prune -a --volumes 	# same as above but also deletes all your docker images
docker node ls 	# see all the nodes connected to the swarm
docker node inspect <node_id>
docker service ps <service_name> -- pretty	# shows you which node the service is currently running on
docker ps # lists the services
docker exec -it <service_id_from_ps> bash # opens a bash terminal within that specific container
docker service update --force <service_name> # reloads the service with updated image (first build the new image)
			(service name ex. cluster_web_app) this is good for when you update something but don't want to reload the whole swarm