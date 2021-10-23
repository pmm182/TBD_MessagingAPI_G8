#!/bin/bash

echo "Terminando shard2..."
docker-compose -f shard2/docker-compose.yaml down

echo "Terminando mongos..."
docker-compose -f mongos/docker-compose.yaml down

echo "Terminando shard1..."
docker-compose -f shard1/docker-compose.yaml down

echo "Terminando config servers..."
docker-compose -f config-server/docker-compose.yaml down
