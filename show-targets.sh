#!/bin/bash

for i in $(ls /rap)
do
	target=$(cat $i.txt|grep Target|head -n1|awk '{print $2}')
	echo "$target $i"
done|sort -n -r|awk '{print $2" "$1}'
