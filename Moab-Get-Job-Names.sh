#!/bin/bash

for argument in "$@"
do
	name=$(checkjob $argument|grep AName|awk '{print $2}')

	echo -e "$argument\t$name"
done
