#!/usr/bin/env python

import sys

# \see http://www.w3.org/TR/REC-xml/#charsets
class PathValidator:
	def __init__(self):
		return

	def validate(self, path):
		i = 0
		theLength = len(path)

		while i < theLength:
			character = path[i]
			if not self.validateCharacter(character):
				print(character + " is invalid " + str(ord(character)))
				return False
			i += 1

		return True

	def validateCharacterWithValue(self, character, value):
		return character == value

	def validateCharacterWithRange(self, character, minimum, maximum):
		return minimum <= character and character <= maximum

	def validateCharacter(self, character):
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

for line in open(sys.argv[1]):
	path = line.rstrip("\n")

	valid = validator.validate(path)

	if not valid:
		print(path)




