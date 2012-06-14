#!/bin/bash

project=nne-790-ab

echo "Identifier	Name	User	Tasks	State"

showq  -w acct=$project > dump

for state in Running Idle Starting Deferred BatchHold
do
	for i in $(cat dump|grep $state|awk '{print $1}')
	do
		name=$(checkjob $i|grep Name|awk '{print $2}')
		slots=$(checkjob $i|grep "Total Requested Ta"|awk '{print $4}')
		user=$(checkjob $i|grep "Creds"|awk '{print $2}'|sed 's/user://g')

		echo "$i	$name	$user	$slots	$state"
	done
done


