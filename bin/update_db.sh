#!/bin/bash

# Execute this with
# > ./update_db.sh <key_name> <path_to_local_db> 
# where <key_name> is the name of the private key in ~/.ssh authorised
# to access the miracle AWS server and <path_to_local_db> is the database
# file you have locally that you wish to push to miracle.

scp -i ~/.ssh/$1 $2 ec2-user@34.245.139.102:/home/ec2-user/distributed/miracle.sqlite
