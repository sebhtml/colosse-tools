#!/bin/bash

if test $# -eq 0
then
	echo "Available jobs:"
	
	for i in $(showq|grep $(whoami|cut -c 1-8)|awk '{print $1}')
	do
		echo "$i	$(checkjob $i|grep AName|awk '{print $2}')"
	done

	exit
fi

node=$(checkjob $1|grep -A1 Node|tail -n1|sed 's/\[//g'|sed 's/:8\]//g')
#echo $node
ssh $node
