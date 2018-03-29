#!/bin/bash
# Program:
#      This script contains some stiuation for testing
# History:
#      2017-06-27     Neo    First Release

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

porta=$1  # what is the start port of client
videoNum=$2  # Total number that you want to start
VIDEOURL="http://pl8.live.panda.tv/live_panda/8dd539552902c2ec70382e90bf67057d.flv"

if [ -z $1 ]; then
    echo "Usage: start_video  startport | videoNum"
else
    echo "Start video num: $videoNum"
    for i in $(seq 1 $videoNum)
    do
        
        curl  http://127.0.0.1:$porta/live_flv/user/xmtv?url=$VIDEOURL >/dev/null 2>&1 &
        echo " Client $i | Port $porta | Play file $VIDEOURL"
        porta=$[$porta+100] # Incrase 100 of port number for next player
        sleep 2
    done
fi
