#!/usr/bin/env python
# encoding: UTF-8
# Bugs: does not work in Windows because the separator is not '/'
# author: Sébastien Boisvert

from elementtree.ElementTree import Element
from elementtree.ElementTree import parse
#from BeautifulSoup import BeautifulSoup as Soup
import sys

arguments=sys.argv

"""
<entry>
<path>./data-for-system-tests</path>
<user>sboisver12</user>
<group>nne-790-01</group>
<type>symbolic link</type>
<size>30</size>
<mount>m</mount>
<inode>241238200</inode>
</entry>

"""

fileName = arguments[1]

class Entry:
	def __init__(self, path, user, group, type, size, mount, inode):
		self.path = path
		self.user = user
		self.group = group
		self.type = type
		self.size = size
		self.mount = mount
		self.inode = inode
		self.recursiveSize = 0
		self.recursiveInodes = 0

	def getSize(self):
		return self.size

	def addChild(self, entry):
		size = entry.getSize()
		self.recursiveSize += size
		self.recursiveInodes += 1

	def getPath(self):
		return self.path

#tree = parse(fileName)
#element = tree.getroot()

#content = open(fileName).read()
#soup = Soup(content)

#for entry in soup.findAll("entry"):

tree = parse(fileName)
element = tree.getroot()

keys ={}

for entry in element.findall("entry"):
	path = entry.find("path").text
	user = entry.find("user").text
	group = entry.find("group").text
	type = entry.find("type").text
	size = int(entry.find("size").text)
	mount = entry.find("mount").text
	inode = int(entry.find("inode").text)

	entry = Entry(path, user, group, type, size, mount, inode)

	keys[path] = entry

for entry in keys.values():
	path = entry.getPath()

	elements = path.split("/")

	i = 0

	parentKey = ""

	while i < len(elements)-1:
		token = elements[i]

		if parentKey != "":
			parentKey += "/"

		parentKey += token

		if parentKey in keys:
			keys[parentKey].addChild(entry)

		i += 1


# dump
