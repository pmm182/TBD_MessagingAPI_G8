#!/bin/bash

ADDITIONAL_PARAM=$1

echo "Terminando shard2..."
docker-compose -f shard2/docker-compose.yaml down ${ADDITIONAL_PARAM}

echo "Terminando mongos..."
docker-compose -f mongos/docker-compose.yaml down ${ADDITIONAL_PARAM}

echo "Terminando shard1..."
docker-compose -f shard1/docker-compose.yaml down ${ADDITIONAL_PARAM}

echo "Terminando config servers..."
docker-compose -f config-server/docker-compose.yaml down ${ADDITIONAL_PARAM}
