#!/usr/bin/python
# encoding: utf-8
# written by Sébastien Boisvert

import sys
import os

import os
from xml.dom.minidom import parse, parseString

# qhost should be available
os.system("qhost -j -xml > dump.xml")

dom=parse("dump.xml")

counts={}

eraseXML=True
total=0
down=0

for host in dom.getElementsByTagName("host"):

	for hostValue in host.getElementsByTagName("hostvalue"):
		name=hostValue.getAttribute("name")
		value=hostValue.childNodes[0].nodeValue

		if value=='-':
			down+=1
			continue

		if name=="num_proc":
			total+=int(value)


for job in dom.getElementsByTagName("job"):

	type=None
	owner=None

	for jobValue in job.getElementsByTagName("jobvalue"):
		name=jobValue.getAttribute("name")
		value=jobValue.childNodes[0].nodeValue

		if name=="job_owner":
			owner=value
		elif name=="pe_master":
			type=value

	if type=="SLAVE":
		if owner not in counts:
			counts[owner]=0

		counts[owner]+=1


if eraseXML:
	os.system("rm dump.xml")

index={}

for i in counts.items():
	user=i[0]
	count=i[1]

	if count not in index:
		index[count]=[]
	index[count].append(user)

keys=index.keys()
keys.sort()

j=len(keys)-1

while j>=0:
	count=keys[j]
	for user in index[count]:
		proportion=100.0*count/total

		print user+"	"+str(count)+"	"+str(total)+"	"+str(proportion)+"%"

	j-=1
