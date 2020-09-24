#!/bin/bash

BACKUP_DB=/home/ec2-user/distributed/backup-miracle.sqlite
LIVE_DB=/home/ec2-user/distributed/miracle.sqlite
USER=ec2-user
SERVER=34.245.139.102
PUBLIC_KEY=$1
UPLOAD_DB=$2

#echo "Backing up existing live database to '$BACKUP_DB'"
#scp -v -i ~/.ssh/$1 $USER@$SERVER:$LIVE_DB $USER@$SERVER:$BACKUP_DB

echo "Uploading new live database to '$LIVE_DB'"
scp -v -i ~/.ssh/$1 $UPLOAD_DB $USER@$SERVER:$LIVE_DB
