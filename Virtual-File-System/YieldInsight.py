#!/usr/bin/env python
# encoding: UTF-8
# Bugs: does not work in Windows because the separator is not '/'
# author: Sébastien Boisvert

#from elementtree.ElementTree import Element
#from elementtree.ElementTree import parse
import xml.parsers.expat
#from BeautifulSoup import BeautifulSoup as Soup
import sys

# \see http://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

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

if len(arguments) != 2:
	print("Usage: YieldInsight.py data.xml")
	sys.exit()

fileName = arguments[1]

class Entry:
	def __init__(self):
		self.name = None
		self.path = ""
		self.user = ""
		self.group = ""
		self.size = 0
	
	def setName(self, name):
		self.name = name

	def setPath(self, path):
		self.path = path

	def setUser(self, user):
		self.user = user

	def getUser(self):
		return self.user

	def setGroup(self, group):
		self.group = group

	def getGroup(self):
		return self.group
	def setType(self, type):
		self.type = type

		if self.type == "directory":
			self.children = {}
			self.recursiveSize = 0
			self.recursiveInodes = 0
			self.size = 0

	def getType(self):
		return self.type

	def isDirectory(self):
		return self.type == "directory"

	def setSize(self, size):
		self.size = size

		#if self.isDirectory():
			#self.recursiveInodes += 1
			#self.recursiveSize += size

	def setMount(self, mount):
		#self.mount = mount
		a = 1

	def setInode(self, inode):
		#self.inode = inode
		a = 1

	def getRecursiveSize(self):
		if self.isDirectory():
			return self.recursiveSize
		return self.size

	def getRecursiveInodes(self):
		if self.isDirectory():
			return self.recursiveInodes
		return 1

	def getSize(self):
		return self.size

	def bindChild(self, name, entry):
		#print("type 1 --> " + self.getType() + " " + "type 2 --> " + self.getType())
		#self.recursiveSize += entry.getSize()
		#self.recursiveInodes += 1
		self.children[name] = entry

	def getPath(self):
		return self.path

	def hasChild(self, name):
		if name in self.children:
			return True
		return False

	def getChild(self, name):
		if not self.hasChild(name):
			return None
		return self.children[name]

	def compute(self):
		if self.isDirectory():
			children = self.children.values()
			for child in children:
				child.compute()
				self.recursiveSize += child.getRecursiveSize()
				self.recursiveInodes += child.getRecursiveInodes()

class Report:
	def __init__(self, fileName, name):
		self.fileName = fileName
		self.name = name

		self.file = open(self.fileName + "-" + name + ".xml", "w")
		self.file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
		self.file.write("\n<objects>\n")

	def close(self):
		self.file.write("</objects>")
		self.file.close()

	def append(self, name, score):
		self.file.write("<object><handle>" + name + "</handle><score>" + str(score) + "</score></object>\n")

#tree = parse(fileName)
#element = tree.getroot()

#content = open(fileName).read()
#soup = Soup(content)

#for entry in soup.findAll("entry"):


#tree = parse(fileName)
#element = tree.getroot()

globalGenerator = None

# \see http://docs.python.org/release/2.6.6/library/pyexpat.html
# 3 handler functions
def startElementHandler(name, attributes):
	globalGenerator.startElement(name, attributes)

def endElementHandler(name):
	globalGenerator.endElement(name)

def processDataHandler(data):
	globalGenerator.processData(data)


class ReportGenerator:
	def __init__(self, fileName):
		self.fileName = fileName
		self.verbose = False
		self.dryRun = False

	def enableDryRunMode(self):
		self.dryRun = True

	def enableVerbosity(self):
		self.verbose = True

	def startElement(self, name, attributes):
		if name == "entry":
			self.isInsideEntry = True
			self.attributes = {}

		self.stack.append(name)

	def endElement(self, name):
		if name == "entry":
			self.isInsideEntry = False
			#print("Got node")
			#print(self.attributes)

			self.addEntry()

			if self.verbose:
				if self.loaded % 10000 == 0:
					print("Loaded " + str(self.loaded) + " from " + self.fileName)

			self.loaded += 1


		self.stack.pop()

	def addEntry(self):

		if self.dryRun:
			return

		path = self.attributes["path"]
		user = self.attributes["user"]
		group = self.attributes["group"]
		type = self.attributes["type"]
		size = int(self.attributes["size"])
		mount = self.attributes["mount"]
		inode = int(self.attributes["inode"])

		# inqsert the node in the file system
		directories = path.split("/")

		currentNode = self.root

		iterator = 0

		while iterator < len(directories):
			directory = directories[iterator]

			if not currentNode.hasChild(directory):
				entry = Entry()
				entry.setName(directory)
				entry.setType("directory")
				self.entries.append(entry)

				if iterator == len(directories) - 1:
					entry.setUser(user)
					entry.setGroup(group)
					entry.setType(type)
					entry.setSize(size)
					entry.setMount(mount)
					entry.setInode(inode)
					entry.setPath(path)

				currentNode.bindChild(directory, entry)

			currentNode = currentNode.getChild(directory)
			iterator += 1


	def processData(self, data):
		if self.isInsideEntry:

			currentElement = self.stack.pop()
			self.stack.append(currentElement)

			if currentElement not in self.attributes:
				self.attributes[currentElement] = ""

			self.attributes[currentElement] += data

	def load(self):

		root = Entry()
		root.setName("root")
		root.setType("directory")
		self.root = root
		self.entries = []
		self.loaded = 0

		parser = xml.parsers.expat.ParserCreate()
		parser.StartElementHandler = startElementHandler
		parser.EndElementHandler = endElementHandler
		parser.CharacterDataHandler = processDataHandler

		file = open(self.fileName)

		self.isInsideEntry = False
		self.stack = []

		print("Parsing file")
		parser.ParseFile(file)

		print("Generating recursive counts")

		self.root.compute()

	def generateReport(self):
		# dump

		print("Generating reports")
		entries = self.entries

		report = Report(self.fileName, "byBytes")

		sortedEntries = sorted(entries, key = lambda entry: entry.size, reverse = True)
		i = 0
		while i < len(sortedEntries):
			entry = sortedEntries[i]
			report.append(entry.getPath(), entry.getSize())
			i += 1

		report.close()

		report = Report(self.fileName, "byRecursiveBytes")

		sortedEntries = sorted(entries, key = lambda entry: entry.recursiveSize, reverse = True)
		i = 0
		while i < len(sortedEntries):
			entry = sortedEntries[i]
			report.append(entry.getPath(), entry.getRecursiveSize())
			i += 1

		report.close()

		report = Report(self.fileName, "byRecursiveInodes")

		sortedEntries = sorted(entries, key = lambda entry: entry.recursiveInodes, reverse = True)

		i = 0
		while i < len(sortedEntries):
			entry = sortedEntries[i]
			report.append(entry.getPath(), entry.getRecursiveInodes())
			i += 1

		report.close()

		report = Report(self.fileName, "byUserInodes")

		users = {}
		for entry in entries:
			user = entry.getUser()
			if user not in users:
				users[user] = 0

			users[user] += 1

		theEntries = []
		for key in users.keys():
			theEntries.append([key, users[key]])

		sortedEntries = sorted(theEntries, key = lambda entry: entry[1], reverse = True)

		i = 0
		while i < len(sortedEntries):
			entry = sortedEntries[i]
			report.append(entry[0], entry[1])
			i += 1

		report.close()

		report = Report(self.fileName, "byUserBytes")

		users = {}
		for entry in entries:
			user = entry.getUser()
			if user not in users:
				users[user] = 0

			users[user] += entry.getSize()

		theEntries = []
		for key in users.keys():
			theEntries.append([key, users[key]])

		sortedEntries = sorted(theEntries, key = lambda entry: entry[1], reverse = True)

		i = 0
		while i < len(sortedEntries):
			entry = sortedEntries[i]
			report.append(entry[0], entry[1])
			i += 1

		report.close()


		report = Report(self.fileName, "byGroupBytes")

		users = {}
		for entry in entries:
			user = entry.getGroup()
			if user not in users:
				users[user] = 0

			users[user] += entry.getSize()

		theEntries = []
		for key in users.keys():
			theEntries.append([key, users[key]])

		sortedEntries = sorted(theEntries, key = lambda entry: entry[1], reverse = True)

		i = 0
		while i < len(sortedEntries):
			entry = sortedEntries[i]
			report.append(entry[0], entry[1])
			i += 1

		report.close()

		report = Report(self.fileName, "byGroupInodes")

		users = {}
		for entry in entries:
			user = entry.getGroup()
			if user not in users:
				users[user] = 0

			users[user] += 1

		theEntries = []
		for key in users.keys():
			theEntries.append([key, users[key]])

		sortedEntries = sorted(theEntries, key = lambda entry: entry[1], reverse = True)

		i = 0
		while i < len(sortedEntries):
			entry = sortedEntries[i]
			report.append(entry[0], entry[1])
			i += 1

		report.close()



reportGenerator = ReportGenerator(fileName)
globalGenerator = reportGenerator
reportGenerator.enableVerbosity()
#reportGenerator.enableDryRunMode()

reportGenerator.load()
reportGenerator.generateReport()

