#!/usr/bin/env python

import sys

# \see http://www.w3.org/TR/REC-xml/#charsets
class PathValidator:
	def __init__(self):
		self.encoding = "utf8"

	def validate(self, path):

		valid = True

		try:
			unicode(path, self.encoding)
		except:
			valid = False

		return valid

		i = 0
		theLength = len(path)

		print("Object: " + path)

		while i < theLength:
			character = path[i]

			print("Position " + str(i) + " ---> " + character + " " + str(len(character)) + " " + str(ord(character)))

			if not self.validateCharacter(character):
				return False
			i += 1

		return True

	def validateCharacter(self, character):

		valid = True

		try:
			value = unicode(character, self.encoding)
		except:
			valid = False

		return valid

	def validateCharacterWithValue(self, character, value):
		return character == value

	def validateCharacterWithRange(self, character, minimum, maximum):
		return minimum <= character and character <= maximum

	def validateCharacterOld(self, character):
		if len(character) == 1:
			character = ord(character)
			if self.validateCharacterWithValue(character, 0x9):
				return True
			if self.validateCharacterWithValue(character, 0xa):
				return True
			if self.validateCharacterWithValue(character, 0xd):
				return True
		if self.validateCharacterWithRange(character, 0x20, 0xd7ff):
			return True
		if self.validateCharacterWithRange(character, 0xe000, 0xfffd):
			return True
		if self.validateCharacterWithRange(character, 0x10000, 0x10ffff):
			return True

		return False

validator = PathValidator()

processed = 0

f = open(sys.argv[1] + "+invalid", "w")

for line in open(sys.argv[1]):
	path = line.rstrip("\n")

	valid = validator.validate(path)

	if processed % 10000 == 0:
		print("Processed: " + str(processed))

	if not valid:
		f.write(line)

	processed += 1

f.close()





