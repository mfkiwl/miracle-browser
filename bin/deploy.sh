#!/bin/bash

# Execute this with 
# > ./deploy.sh <key_name> 
# where <key_name> is the name of the private key in ~/.ssh 
# authorised to access the miracle AWS server. Once executed,
# the latest changes from miracle-browser and miracle-db will
# be pulled and deployed instantly to the public website.

ssh -i ~/.ssh/$1 ec2-user@34.245.139.102 "cd distributed && ./run.sh && exit"
