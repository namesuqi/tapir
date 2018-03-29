#!/usr/bin/sh


Dir="/usr/local/named"
Conf="$Dir/etc/named.conf"
PID=`pgrep named`

echo $PID

if [ -z "$PID" ];then
    echo "Find named pid is $PID! Kill now"
    `kill -9 $PID` >/dev/null 2>&1
else
    echo "There is no named process!"
fi
echo "Start Named!"
`$Dir/sbin/named -c $Conf`
echo "Named PID now is `pgrep named`"
