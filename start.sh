#!/bin/bash

set -e

if [ -d /mnt/dump ]; then
  echo 'Restoring dump...'
  if [ ! -z "${MONGODB_USERNAME}" ]; then
    mongosh -u ${MONGODB_USERNAME} -p ${MONGODB_PASSWORD} --eval "db.dropDatabase();" ${MONGODB_SERVER}/messaging8
    mongorestore ${MONGODB_CONNECTION_STRING} /mnt/dump
  else
    mongosh --eval "db.dropDatabase();" ${MONGODB_SERVER}/messaging8
    mongorestore ${MONGODB_CONNECTION_STRING} /mnt/dump
  fi
fi

uwsgi --socket 0.0.0.0:8080 --logto /tmp/uwsgi.log --protocol http -w wsgi:app --lazy-apps --processes $UWSGI_PROCESSES_COUNT --threads $UWSGI_THREADS_COUNT --master