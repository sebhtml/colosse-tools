#!/bin/bash

project=$1
year=$2

./ViewProjectUsage.py nne-790-ab > data

awk -F '\t' '{print $6}' data|sort|uniq|grep -v User > users

echo "Scheduler: Sun Grid Engine"
echo "Project: $project"
echo "Year: $year"
echo ""
for month in 01 02 03 04 05 06 07 08 09 10 11 12
do
	echo "$year-$month"

	for user in $(cat users)
	do
		token="$year-$month"
		coreMinutes=$(grep $user data |grep $token \
		| awk -F '\t' 'BEGIN {SUM = 0} {SUM = SUM + $10} END {print SUM}')

		coreHours=$(($coreMinutes / 60))
		echo "  $user $coreHours"
	done

	coreMinutes=$(cat data |grep $token \
	| awk -F '\t' 'BEGIN {SUM = 0} {SUM = SUM + $10} END {print SUM}')

	coreHours=$(($coreMinutes / 60))
	echo "  Total $coreHours"

	echo ""
done

#rm data
