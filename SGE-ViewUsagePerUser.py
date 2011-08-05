#!/usr/bin/python

import os

os.system("qstat -s r -u '*'|awk '{print $4\" \"$9}'|sort > tmp")

data={}

for line in open("tmp"):
	tokens=line.split()
	if len(tokens)<2:
		continue

	if tokens[1]=="slots":
		continue
	user=tokens[0]
	slots=int(tokens[1])
	if user not in data:
		data[user]=0
	data[user]+=slots

for i in data.items():
	print str(i[1])+" "+str(i[0])
