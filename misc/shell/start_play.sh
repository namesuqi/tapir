#!/bin/bash

echo "play whitch file: please input "file1" or "file2" or "file3""
read file
if [ "$file" = "file1" ];then
url=http://flv.srs.cloutropy.com/wasu/test.flv
elif [ "$file" = "file2" ];then
url=http://flv.srs.cloutropy.com/wasu/test2.flv
else
url=http://flv.srs.cloutropy.com/wasu/test3.flv
fi
 
echo "choose start port of client"
read port
echo "number of client"
read number

for((i=1;i<=number;i++))
do
   nohup curl http://127.0.0.1:$port/live_flv/user/wasu?url=$url > /dev/null 2>&1 &
   echo "http://127.0.0.1:$port/live_flv/user/wasu?url=$url"
   echo "client $i | port $port | play $file"
   port=$[$port+100]
done
