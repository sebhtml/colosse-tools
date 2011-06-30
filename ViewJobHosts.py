#!/usr/bin/python
# encoding: utf-8
# written by Sébastien Boisvert
# Université Laval
# 2010-11-02
# updated on 2011-06-30

import sys
import os

if len(sys.argv)!=2:
	print "You must provide a SGE job identifier currently running."
	print "qstat output follows."
	os.system("qstat")
	sys.exit()

jobId=sys.argv[1]
import os
from xml.dom.minidom import parse, parseString

# qhost should be available
os.system("qhost -j -xml>dump.xml")

dom=parse("dump.xml")

print "Queue name\tMode\tJob name\tJob identifier\tHost\tNumber of cores\tMemory\tAverage load\tUtilised memory"

for host in dom.getElementsByTagName("host"):
	hostValues={}
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
		if job.getAttribute("name")==jobId:
			print jobValues["queue_name"]+"\t"+jobValues["pe_master"]+"\t"+jobValues["job_name"]+"\t"+job.getAttribute("name")+"\t"+host.getAttribute("name")+"\t"+hostValues["num_proc"]+"\t"+hostValues["mem_total"]+"\t"+hostValues["load_avg"]+"\t"+hostValues["mem_used"]

