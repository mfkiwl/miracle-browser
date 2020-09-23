#!/bin/bash

ssh -i ~/.ssh/$1 ec2-user@34.245.139.102 "cd distributed && ./run.sh && exit"
