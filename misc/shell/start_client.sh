#!/bin/bash
rm -rf startclient
client=ys_service_static
mkdir startclient
file=startclient
killall $client
echo "All client killed"
sleep 5
echo "the number of client:"
read i
for((a=0;a<i;a++))
do  
    port=$[40000+$a*100]
    mkdir $file/$a
    cp $client $file/$a
    chmod u+x $file/$a/$client
    cd $file/$a
    nohup ./$client -p $port &
    cd ../..
done 

for((x=0;x<i;x++))
do
    peer_info=`cat $file/$x/yunshang/yunshang.conf| awk -F '"' '{printf $4}'`
    echo '"'$peer_info'"',
done
