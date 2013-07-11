#!/bin/bash

if test $# -eq 0
then
	echo "Commands: spawn, kill, connect"

	echo "Available:"
	
	for i in $(showq -w user=$(whoami)|grep $(whoami|cut -c 1-8)|awk '{print $1}')
	do
		node=$(checkjob $i|grep -A1 Node|tail -n1|sed 's/\[//g'|sed 's/:8\]//g')
		echo "$i	$(checkjob $i|grep AName|awk '{print $2}')	node= $node"
	done

	exit
fi

if test "$1" = "spawn"
then
	msub ~/start.sh
fi

if test "$1" = "kill"
then
	canceljob $2
fi

if test "$1" = "connect"
then
	node=$(checkjob $2|grep -A1 Node|tail -n1|sed 's/\[//g'|sed 's/:8\]//g')
#echo $node
	ssh $node
fi
