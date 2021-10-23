#!/bin/bash

mongo mongodb://127.0.0.1:60000 --eval "sh.addShard('shard1rs/shard1svr1:27017,shard1svr2:27017,shard1svr3:27017')"

