#!/bin/bash

mongo mongodb://127.0.0.1:60000 --eval "sh.addShard('shard2rs/shard2svr1:27017,shard2svr2:27017,shard2svr3:27017')"

