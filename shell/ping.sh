#!/bin/sh

if [ $# -ne 2 ]
then
	echo "Usage: $0 <pre[x-y].host.com> <ping count>"
	echo "Example: $0 tw[1-20].lvdou321.com 2"
	exit 0
fi

agents=$1
ping_count=$2

echo "detect agents: $agents..."


function make_all_hosts() {
	start=`echo $1 | sed -n 's/^.*\[\(.*\)\].*$/\1/p' | awk -F'-' '{print $1}'`	
	end=`echo $1 | sed -n 's/^.*\[\(.*\)\].*$/\1/p' | awk -F'-' '{print $2}'`

	while [ $start -le $end ]
	do
		echo `echo $1 | sed -n "s/\[.*\]/$start/p"`
		start=`expr $start + 1`
	done

}

function avg_ping_rtt() {
	#set the ping arguments
	ping_host=$1
	ping_count=$2
	
	#ping the destination host
	result=`ping -q -c $ping_count $ping_host | sed -n 's/^.*min\/avg\/max\/stddev =\(.*\)ms/\1/p'`

	#extract average rtt from ping result
	avg_rtt=`echo $result | awk -F'/' '{print $2}'`
	
	echo $avg_rtt
}

hosts=`make_all_hosts $agents`

for host in $hosts
do
	rtt=`avg_ping_rtt $host $ping_count`
	echo $host: $rtt
done

