#!/bin/bash

scp -i ~/.ssh/$1 $2 ec2-user@34.245.139.102:/home/ec2-user/distributed/miracle.sqlite
