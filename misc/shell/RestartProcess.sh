#!/bin/bash
# Program:
#      This script contains some stiuation for testing
# History:
#      2017-06-27     Neo    First Release

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH


local_dir=`pwd` # script directory
log_file_name=$local_dir/restart.log  # log record directory

client_name=$1  # what is the name of client
porta=$2        # what is the start port of client
client_num=$3   # Client total number that you want to start

if [ -z $1 ]; then
    echo "Usage: start_client clientname | startport | clientNum"
else
    # Print all args
    echo clientname is: $client_name
    echo localDir: $local_dir
    echo clientNum: $client_num

    killall $client_name
    sleep 5

    echo Start $client_num $client_name from port -p $porta at `date` >> $log_file_name

    for i in $(seq 1 $client_num); do
        echo port a: $porta
        mkdir -p $local_dir/$i
        cd $local_dir/$i
        cp $local_dir/$client_name $local_dir/$i/$client_name
        nohup ./$client_name -p $porta -u 2 2>&1 &   # Define peer id prefix as 00000002
        echo "Client $i  Start on port $porta"
        porta=$[$porta+10]  # Incrase 10 of port number for next client
        sleep 2
    done
fi

# Show all peer id on screen
for i in $(seq 1 $client_num); do
    peer_info=`cat $local_dir/$i/yunshang/yunshang.conf| awk -F '"' '{printf $4}'`
    echo $peer_info
done