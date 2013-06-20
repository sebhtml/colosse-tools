#!/usr/bin/env python
# encoding: UTF-8
# Author: Sébastien Boisvert
# BUGS:
# * This will not work if paths contain < or >  [FIXED]

import sys
import os
import os.path
import subprocess
from subprocess import Popen, PIPE

# get XML content for a bunch of paths
def getXMLContent(paths):

	pipeArguments = []
	pipeArguments.append("stat")
	pipeArguments.append("-c")
	pipeArguments.append("<entry>\n<path>%n</path>\n<user>%U</user>\n<group>%G</group>\n<type>%F</type>\n<size>%s</size>\n<mount>%m</mount>\n<inode>%i</inode>\n</entry>")
	i = 0
	while i < len(paths):
		pipeArguments.append(paths[i])
		i += 1

	process = Popen(pipeArguments, stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()

	content = stdout

	i = 0
	while i < len(paths):
		path = paths[i]
		newPath = path.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')

		if newPath != path:
			content = content.replace(path, newPath)
		i += 1

	return content

arguments = sys.argv

if len(arguments) != 2:
	print("You must provide a file with file paths (one per line)")
	sys.exit()

fileWithPaths = arguments[1]

directory = os.getcwd()

f = open(fileWithPaths+".xml", "w")

f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + "\n")
f.write("<report>\n")
f.write("<directory>" + directory + "</directory>\n")

toProcess = 128
elements = []

for line in open(fileWithPaths):
	path = line.strip()
	if len(path) == 0:
		continue
	if not os.path.exists(path):
		continue

	if len(elements) < toProcess:
		elements.append(path)
		continue

	content = getXMLContent(elements)
	elements = []
	f.write(content)

if len(elements) > 0:
	content = getXMLContent(elements)
	elements = []
	f.write(content)

f.write("</report>")

