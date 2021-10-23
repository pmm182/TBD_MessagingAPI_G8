#!/bin/bash

echo "Iniciando config servers..."
docker-compose -f config-server/docker-compose.yaml up -d
sleep 10
./config-server/mongo_init.sh

echo "Iniciando shard1..."
docker-compose -f shard1/docker-compose.yaml up -d
sleep 10
./shard1/mongo_init.sh

echo "Iniciando mongos"
docker-compose -f mongos/docker-compose.yaml up -d
sleep 10
./mongos/mongo_init.sh

echo "Iniciando shard2..."
docker-compose -f shard2/docker-compose.yaml up -d
sleep 10
./shard2/mongo_init.sh

