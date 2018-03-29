#!/bin/bash

count=40
startport=30000
lflist=""

function stop_lf {
    pkill -9 ys_service_stat
    rm -rf client-*
}

function stop_lf_only {
    pkill -9 ys_service_stat
}

function launch_lf {
    for id in {1..40}
    do
        portid=`expr $id \* 3`
        port=`expr $startport + $portid`
        mkdir client-$port
        cp ys_service_static client-$port
        cp -rf conf client-$port
        cd client-$port
        echo "Running at $port"
        (nohup ./ys_service_static -p $port -u 0x00000008 > /dev/null 2>&1) &
        cd -
        sleep 1
    done
}

function start_lf_only {
    for id in {1..40}
    do
        portid=`expr $id \* 3`
        port=`expr $startport + $portid`
        rm -rf client-$port/ys_service_static
        cp ys_service_static client-$port
        cp -rf conf client-$port
        cd client-$port
        echo "Running at $port"
        (nohup ./ys_service_static -p $port -u 0x00000008 > /dev/null 2>&1) &
        cd -
        sleep 1
    done
}

function list_peerid {
    lfreqcount=0
    lflist="["
    comma=""
    for dir in `ls client-* -d`
    do
        peeridstr=`cat ./$dir/yunshang/yunshang.conf`
        peerid=`echo $peeridstr | awk -F ":" '{print $2}' | awk -F "," '{print $1}'`
        peerid=`echo $peerid | sed -e 's/ //g'`
        [ ! "$lflist" = "[" ] && lflist=$lflist,
        lflist=$lflist"$peerid"
        ((lfreqcount++))
        if [ ! -z $1 ]; then
            [ $1 -lt $lfreqcount ] && break
        fi
    done
    lflist=$lflist"]"
    echo $lflist
}

joininterface="http://192.168.3.203:8000/join_lf"
leaveinterface="http://192.168.3.203:8000/leave_lf"
allpeerlist=`list_peerid`

function join_lf {
    joinlfbody="{\"file_id\":\"E6DB2423CE1D7461AFBDCCE7ED42097D\",
        \"file_url\":\"http://pl8.live.panda.tv/live_panda/012192e6277f7da070480d8ee32648fd.flv\",
        \"peer_ids\":$1}"
    echo "Request JOIN LF: $joinlfbody to $joininterface"
    curl -v -X POST -H 'Content-Type: application/json' -d "$joinlfbody" $joininterface
}

function leave_lf {
    leavelfbody="{\"file_id\":\"E6DB2423CE1D7461AFBDCCE7ED42097D\",
        \"file_url\":\"http://pl8.live.panda.tv/live_panda/012192e6277f7da070480d8ee32648fd.flv\",
        \"peer_ids\":$1}"
    echo "Request LEAVE LF: $leavelfbody to $leaveinterface"
    curl -v -X POST -H 'Content-Type: application/json' -d "$leavelfbody" $leaveinterface
}

function join_lf_repeadly {
    while true; do
        join_lf $1
        sleep 20
    done
}

function glich_lf {
    while true; do
        random=$RANDOM
        reqcount=$((random%count))
        peerlist=`list_peerid $reqcount`
        leave_lf $allpeerlist
        echo "Waiting LEAVE LF"
        sleep 10
        join_lf $peerlist
        echo "Waiting JOIN LF"
        sleep 180
    done
}

function cache_video {
    for id in {1..40}
    do
        portid=`expr $id \* 3`
        port=`expr $startport + $portid`
        curl -v "http://127.0.0.1:$port/vod/user/demo?url=http://vodtest.crazycdn.com:8088/4k/piano.mp4" > /dev/null
        [ ! -f "./client-$port/yunshang/yunshang.data" ] && echo "Error: cache file is not generated for $port"
        sleep 1
    done
}

case "$1" in
    launch)
        stop_lf
        sleep 1
        launch_lf
        ;;
    join) join_lf_repeadly $allpeerlist ;;
    stop) stop_lf_only ;;
    start) start_lf_only ;;
    glich) glich_lf ;;
    cache) cache_video ;;
    *) echo "Usage: $0 join|launch|stop|glich|cache"
esac