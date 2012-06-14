#!/bin/bash

echo "Identifier	Name	User	Tasks"

for i in $(showq  -w acct=nne-790-ab|grep Running|awk '{print $1}')
do
	name=$(checkjob $i|grep Name|awk '{print $2}')
	slots=$(checkjob $i|grep "Total Requested Ta"|awk '{print $4}')
	user=$(checkjob $i|grep "Creds"|awk '{print $2}'|sed 's/user://g')

	echo "$i	$name	$user	$slots"

done
