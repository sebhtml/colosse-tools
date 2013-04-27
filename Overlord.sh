#!/bin/bash

if test $# -eq 0
then
	echo "To connect to a queen: Overlord.sh 12345678"

	echo "Available queens:"
	
	for i in $(showq -w user=$(whoami)|grep $(whoami|cut -c 1-8)|awk '{print $1}')
	do
		node=$(checkjob $i|grep -A1 Node|tail -n1|sed 's/\[//g'|sed 's/:8\]//g')
		echo "$i	$(checkjob $i|grep AName|awk '{print $2}')	node= $node"
	done

	exit
fi

node=$(checkjob $1|grep -A1 Node|tail -n1|sed 's/\[//g'|sed 's/:8\]//g')
#echo $node
ssh $node
