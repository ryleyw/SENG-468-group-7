
if [ $type = "mongos_conf" ]
then

	sleep 90

	mongo s0rs0:27017 << EOF
use stocks;
db.users.createIndex({ username:1 });
db.quotes.createIndex({ stock:1 });
EOF

	sleep 15

	mongo mongos0:27017 << EOF
db.adminCommand({ addShard: "s0/s0rs0:27017" });
db.adminCommand({ enableSharding: "stocks" });
db.adminCommand({ shardCollection: "stocks.users", key: {"username":1}});
db.adminCommand({ shardCollection: "stocks.quotes", key: {"stock":1}});
db.settings.save( {_id:"chunksize", value: 2} );
EOF
	
elif [ $type = "rs_conf" ]
then

	sleep 25

	if [ $shard = "conf" ]
	then
		mongo ${shard}rs0:27017 << EOF
config = { _id: "$shard", members: [
	{ _id: 0, host: "${shard}rs0" },
	{ _id: 1, host: "${shard}rs1" },
	{ _id: 2, host: "${shard}rs2" }]};
rs.initiate(config)
EOF
	else
		mongo ${shard}rs0:27017 << EOF
config = { _id: "$shard", members: [
	{ _id: 0, host: "${shard}rs0" },
	{ _id: 1, host: "${shard}rs1" },
	{ _id: 2, host: "${shard}rs2", arbiterOnly: true }]};
rs.initiate(config)
EOF
	fi

elif [ $type = "add_shard" ]
then

	sleep 15

	mongo ${shard}rs0:27017 << EOF
config = { _id: "$shard", members: [
    { _id: 0, host: "${shard}rs0" },
    { _id: 1, host: "${shard}rs1" },
    { _id: 2, host: "${shard}rs2", arbiterOnly: true }]};
rs.initiate(config)
EOF

	sleep 15

	mongo mongos0:27017 << EOF
db.adminCommand( {addShard: "${shard}/${shard}rs0:27017"} );
EOF
	
fi