#!/bin/bash
# Program:
#      This script contains some stiuation for testing
# History:
#      2017-06-27     Neo    First Release

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

PROCESS="ys_service"

# [function 1]Get the process id of process
process_id=`pgrep $PROCESS` >/dev/null 2>&1

# [function 2]Get the process id of process
# process_id=`ps aux |grep $PROCESS |grep -v grep | awk -F ' ' '{print $2}'`

# Clent record log file
echo "" > Mem_monitor_log.log

# Judge whether process is exists
if [ ! $process_id ];then
	echo "There is no such process: $PROCESS"
	exit 0
fi

# loop print process meminfo
while true; do
	date_time=`date`
    # Get the memory of process
	process_mem=`cat /proc/$process_id/status |grep VmRSS`
    echo "[$date_time] Process $PROCESS Memory is: $process_mem"
	echo ""
	echo $date_time >> Mem_monitor_log.log
	# Record memory info to log file
	echo "Process $PROCESS Memory is: $process_mem" >> Mem_monitor_log.log
	echo "--------------------------------------------" >> Mem_monitor_log.log
	sleep 3
done