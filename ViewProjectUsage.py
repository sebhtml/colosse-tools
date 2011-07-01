#!/usr/bin/python
# encoding: utf-8
# written by Sébastien Boisvert
# Université Laval
# 2011-05-10
# updated on 2011-06-30

import os
import sys
import datetime

# paths that depend on the installation of Sun Grid Engine
sge_share_mon="/usr/local/ge6.2u5/utilbin/lx24-amd64/sge_share_mon"
pathToAccountingFile="/mnt/redlotus/usr/local/ge6.2u5/default/common"
currentYear=2011

# the rest should work as is
if len(sys.argv)!=2:
	print "You must provide a resource allocation project identifier (RAP Id)."
	print ""
	sys.exit()

years={}

projectIdentifier=sys.argv[1]

# get the target in core-years using sge_share_mon
os.system(sge_share_mon+" -c 1|grep "+projectIdentifier+"|awk '{print $5}' > tmp")
coreYears=int(open("tmp").read())

# compute the allowed core-hours
first=datetime.datetime(currentYear,1,1)
now=datetime.datetime.now()
diff=now-first
yearHours=diff.days*24+diff.seconds/60/60
allowedCoreHours=coreYears*yearHours

# update the cache
cache=os.getenv("HOME")+"/Accounting" 
os.system("mkdir -p "+cache)

cacheFiles={}

for i in os.listdir(cache):
	cacheFiles[i]=1

for file in os.listdir(pathToAccountingFile):
	if len(file)<5:
		continue
	extension=file[len(file)-4:len(file)]
	if extension==".bz2":
		base=file[0:len(file)-4]
		if base not in cacheFiles:
			cacheFiles[base]=1
			os.system("cp "+pathToAccountingFile+"/"+file+" "+cache)
			os.system("bunzip2 "+cache+"/"+file)

os.system("cp "+pathToAccountingFile+"/accounting "+cache)

print ""
print "Compute Canada Resource Allocation Project Identifier: "+projectIdentifier
print "Target: "+str(coreYears)+" core-years"
print ""
output="tmp"
print ""
command="cat "+cache+"/accounting*|grep "+projectIdentifier+"|sed 's/:/ /g'|awk '{print $10 \" \" $0}'|sort -n > "+output

os.system(command)

sumOfCoreMinutes=0

submissions={}

# list the jobs

print "Submitted\tStarted\tEnded\tJobIdentifier\tJobName\tUser\tWaitingHours\tCores\tMinutes\tCore-minutes"

firstDate=""
lastDate=""

for line in open(output):
	tokens=line.split()
	project=tokens[32]
	if project!=projectIdentifier:
		continue

	job=int(tokens[6])
	start=int(tokens[10])

	submission=(tokens[9])
	if submission=="sge":
		submission=start
	else:
		submission=int(submission)

	submitted=str(datetime.datetime.fromtimestamp(submission))
	hours=(start-submission)/60/60
	if hours<0:
		hours=0
	waitingTime=str(hours)
	date=str(datetime.datetime.fromtimestamp(start))
	submittedDate=str(datetime.datetime.fromtimestamp(submission))

	user=tokens[4]
	jobName=tokens[5]
	year=int(date.split("-")[0])

	# remove jobs before 2009 (bug in SGE ?)
	if year<2009:
		continue

	if year not in years:
		years[year]=0
	

	end=int(tokens[11])
	endDate=str(datetime.datetime.fromtimestamp(end))
	if job in submissions:
		continue
	submissions[job]=1
	
	if firstDate=="":
		firstDate=date
	lastDate=date

	seconds=end-start
	minutes=seconds/60
	computeCores=int(tokens[35])
	coreMinutes=minutes*computeCores
	years[year]+=coreMinutes
	sumOfCoreMinutes+=coreMinutes
	
	print str(submittedDate)+"\t"+date+"\t"+endDate+"\t"+str(job)+"\t"+jobName+"\t"+user+"\t"+waitingTime+"\t"+str(computeCores)+"\t"+" "+str(minutes)+"\t"+str(coreMinutes)

# print summary

print ""
print "Compute Canada Resource Allocation Project Identifier: "+projectIdentifier
print "Target: "+str(coreYears)+" core-years"

print ""

print "Project "+projectIdentifier+" has jobs from "+firstDate+" to "+lastDate
print ""
print "Allowed core-hours for 2011: "+str(allowedCoreHours)+" ("+str(first)+" to "+str(now)+")"

print ""
print "Consumption per year"

for i in years.items():
	year=i[0]
	coreHours=i[1]/60
	if year==currentYear:
		print "YEAR_ENTRY\t"+str(year)+"\t"+str(coreHours)+" ("+str(coreHours/(0.0+allowedCoreHours)*100)+"%, allowed: "+str(allowedCoreHours)+" core-hours, predictedAllocation: "+str(coreHours/yearHours)+" core-years)"
	else:
		print "YEAR_ENTRY\t"+str(year)+"\t"+str(coreHours)

		
coreHours=sumOfCoreMinutes/60
print "Core-hours consumed: "+str(coreHours)
coreDays=coreHours/24


