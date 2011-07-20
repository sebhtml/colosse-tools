#!/usr/bin/python
# encoding: utf-8
# written by Sébastien Boisvert
# Université Laval
# 2011-07-20

import sys
import os

hostName="*"

if len(sys.argv)==2:
	hostName=sys.argv[1]

import os
from xml.dom.minidom import parse, parseString

os.system("qhost -j -xml>dump.xml")

dom=parse("dump.xml")

print "queue_name\tpe_master\tjob_owner\tjob_name\tjob_identifier\thost\thost_cores\thost_memory\tutilised_cores\tutilised_memory"

for host in dom.getElementsByTagName("host"):
	hostValues={}

	theHostName=host.getAttribute("name")


	if hostName!="*" and not (theHostName.find(hostName)>=0):
		continue

	print ""
	print "Host: "+theHostName
	print ""
	for hostvalue in host.getElementsByTagName("hostvalue"):
		name=hostvalue.getAttribute("name")

		value=hostvalue.childNodes[0].nodeValue
		hostValues[name]=value
	for job in host.getElementsByTagName("job"):
		jobValues={}
		for jobvalue in job.getElementsByTagName("jobvalue"):
			name=jobvalue.getAttribute("name")
			value=jobvalue.childNodes[0].nodeValue
			jobValues[name]=value
		
		print jobValues["queue_name"]+"\t"+jobValues["pe_master"]+"\t"+jobValues["job_owner"]+"\t"+jobValues["job_name"]+"\t"+job.getAttribute("name")+"\t"+host.getAttribute("name")+"\t"+hostValues["num_proc"]+"\t"+hostValues["mem_total"]+"\t"+hostValues["load_avg"]+"\t"+hostValues["mem_used"]

