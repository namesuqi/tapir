#!/bin/bash
# Program:
#         This script used for monitor (process and thread) cpu and memory
# History:
# 2017-08-22    suqi    First Release

for((;;))
do
    PROCESS="livepush"
    result=`ps aux|grep livepush |grep -v grep|awk -F " " '{print "PID:"$2,"CPU:"$3, "Mem:"$4}' `
    datetime=`date`
    echo "-----------------------------------------"
    echo $datetime
    echo ${result}
    sleep 5
done
