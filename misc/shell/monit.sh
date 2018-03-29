#!/bin/sh

Pro_3_id="8417"
#Pro_4_id="1"
Pro_3="SDK_3.17.1"
#Pro_4="SDK_3.17.2"
while true; do
	date_time=`date`
	Pro_3_Mem=`cat /proc/$Pro_3_id/status |grep VmRSS`
	#Pro_4_Mem=`cat /proc/$Pro_4_id/status |grep VmRSS`
    echo "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
    echo $date_time
	echo "$Pro_3 "$Pro_3_Mem
	#echo "$Pro_4 "$Pro_4_Mem
	echo "//////////////////////////////////////////"
	echo ""
	echo $date_time >> Mem_monitor_log.log
	echo "$Pro_3 "$Pro_3_Mem >> Mem_monitor_log.log
	#echo "$Pro_4 "$Pro_4_Mem >> Mem_monitor_log.log
	echo "----------------------------------------" >> Mem_monitor_log.log
	sleep 3s
done
