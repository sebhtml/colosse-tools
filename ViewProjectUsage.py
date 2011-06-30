#!/usr/bin/python
# encoding: utf-8
# written by Sébastien Boisvert
# Université Laval
# 2011-05-10

import os
import sys
import datetime

if len(sys.argv)!=2:
	print "You must provide a resource allocation project identifier (RAP Id)."
	print ""
	os.system("/clumeq/bin/colosse-info|grep ID")
	sys.exit()

years={}

os.system("/usr/local/ge6.2u5/utilbin/lx24-amd64/sge_share_mon -c 1|grep nne-790-ab|awk '{print $5}' > tmp")

coreYears=int(open("tmp").read())

first=datetime.datetime(2011,1,1)
now=datetime.datetime.now()
diff=now-first
yearHours=diff.days*24+diff.seconds/60/60
allowedCoreHours=coreYears*yearHours

projectIdentifier=sys.argv[1]

pathToAccountingFile="/mnt/redlotus/usr/local/ge6.2u5/default/common"

cache=os.getenv("HOME")+"/Accounting" 
os.system("mkdir -p "+cache)

cacheFiles={}

for i in os.listdir(cache):
	#print "Caching "+i
	cacheFiles[i]=1

#print "Accounting directory is "+pathToAccountingFile
#print "Cache directory is "+cache
#print "Syncing accounting files to the cache"
for file in os.listdir(pathToAccountingFile):
	if len(file)<5:
		continue
	extension=file[len(file)-4:len(file)]
	if extension==".bz2":
		#print "Checking "+file
		base=file[0:len(file)-4]
		if base not in cacheFiles:
			#print "Not cached"
			cacheFiles[base]=1
			os.system("cp "+pathToAccountingFile+"/"+file+" "+cache)
			os.system("bunzip2 "+cache+"/"+file)
			#print "Created "+cache+"/"+base

os.system("cp "+pathToAccountingFile+"/accounting "+cache)

print ""
print "Compute Canada Resource Allocation Project Identifier: "+projectIdentifier

output="tmp"
print ""
command="cat "+cache+"/accounting*|grep "+projectIdentifier+"|sed 's/:/ /g'|awk '{print $10 \" \" $0}'|sort -n > "+output

os.system(command)

sumOfCoreMinutes=0

submissions={}

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

	#print tokens
	#print ""

	seconds=end-start
	minutes=seconds/60
	computeCores=int(tokens[35])
	coreMinutes=minutes*computeCores
	years[year]+=coreMinutes
	sumOfCoreMinutes+=coreMinutes
	
	print str(submittedDate)+"\t"+date+"\t"+endDate+"\t"+str(job)+"\t"+jobName+"\t"+user+"\t"+waitingTime+"\t"+str(computeCores)+"\t"+" "+str(minutes)+"\t"+str(coreMinutes)

print ""

print "Project "+projectIdentifier+" has jobs from "+firstDate+" to "+lastDate
print ""
print "Allowed core-hours for 2011: "+str(allowedCoreHours)+" ("+str(first)+" to "+str(now)+")"

print ""
print "Consumption per year"

for i in years.items():
	year=i[0]
	coreHours=i[1]/60
	if year==2011:
		print "YEAR_ENTRY\t"+str(year)+"\t"+str(coreHours)+" ("+str(coreHours/(0.0+allowedCoreHours)*100)+"%, allowed: "+str(allowedCoreHours)+" core-hours, predictedAllocation: "+str(coreHours/yearHours)+" core-years)"
	else:
		print "YEAR_ENTRY\t"+str(year)+"\t"+str(coreHours)

		
coreHours=sumOfCoreMinutes/60
print "Core-hours consumed: "+str(coreHours)
coreDays=coreHours/24


