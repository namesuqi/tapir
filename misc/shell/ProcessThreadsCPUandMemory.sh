#!/bin/bash
# Program:
#         This script used for monitor (process and thread) cpu and memory
# History:
# 2017-07-23    Neo    First Release
# 2017-08-09    Neo    Second Release Update log records formats

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

log_date=`date +%y%m%d_%H%M`
for((;;))
do
    IFS_old=$IFS
    IFS=$'\n'

    PROCESS="ys_ser"
    pid=`pgrep ${PROCESS}`

    datetime=`date`
    mem_info=`cat /proc/$pid/status|grep -v grep|grep VmRSS| awk -F " " '{print "VmRss Memory Now: "$2" KB"}'`

    echo ""
    echo "-----------------------------------------"
    echo ${mem_info}
    echo "["${datetime}"]: "${mem_info} >> ${log_date}memory_monitor.log

    cpu_pro=`top -p $pid  -n 1 |grep ${PROCESS} | grep -v grep`
    cpu_thr=`top -H -p $pid  -n 1 |grep ${PROCESS} | grep -v grep | head -n 3`
    cpu_pro_info=`echo ${cpu_pro} | awk -F " " '{print "PID:"$1,"CPU :"$10"%    "}'`
    echo -n ${cpu_pro_info}
    echo "["${datetime}"]: "${cpu_pro_info} >> ${log_date}cpu_monitor.log

    for line in  $cpu_thr;
        do
            cpu_thr_info=`echo ${line} | awk -F " " '{print "Thread ID:"$1,"CPU:"$10"%"}'`
            echo -n ${cpu_thr_info}
            echo "["${datetime}"]: "${cpu_thr_info} >> ${log_date}cpu_monitor.log
        done
    IFS=$IFS_old
    sleep 3
done