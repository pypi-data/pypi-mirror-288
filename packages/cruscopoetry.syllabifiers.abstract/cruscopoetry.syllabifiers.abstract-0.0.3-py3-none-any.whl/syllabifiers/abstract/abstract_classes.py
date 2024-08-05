# This file is part of CruscoPoetry.
# 
# CruscoPoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CruscoPoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CruscoPoetry. If not, see <http://www.gnu.org/licenses/>.
#    This file is part of CruscoPoetry.
#
#    CruscoPoetry is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CruscoPoetry is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CruscoPoetry.  If not, see <http://www.gnu.org/licenses/>.
import abc
import re
import json
import os
import sys, argparse
from mum import AbstractSingleton
from .exceptions import SyllabificationException


class AbstractSyllable(abc.ABC):
	"""Represents an abstract class for syllables. Children of this class must implement the method json_dict, which returns the syllable's data in a dictionary that can be JSONified."""

	@abc.abstractmethod
	def json_dict(self) -> dict:
		pass
	
	@abc.abstractmethod
	def iter_phonemes(self):
		"""Iterates over the syllable's phonemes."""
		pass


class AbstractSyllabificator(metaclass=AbstractSingleton):
	"""Represents an abstract class for syllabifying words. Children of this class must implement two methods: :method:`auto_syllabify`, for the automatic syllabification of the word, and 
	:method:`manually_syllabify` if the word has been split manually into syllables. Both methods must return a tuple of instances of a descendant class from AbstractSyllable.
	This class is both an abstract class and a singleton: that is, it must be implemented as an abstract class, and its children will be automatically Singleton classes
	"""	

	_MANUAL_SYLLABIFICATION_REGEX = re.compile("\\[(\\w+\\|)*\\w+\\]")

	#here I implement however some utility functions:
	def syllabify_word(self, word: str):
		"""Checks if the word has been manually syllabified and if yes returns the results of :method:`self.manually_syllabify(word)`; else, returns :method:`self.auto_syllabify(word)`"""

		#we just control whether the word is syllabified. If not, we do not need to do syntax controls, because they have been done already during text parsing.
		if self.__class__._MANUAL_SYLLABIFICATION_REGEX.fullmatch(word):
			return self.manually_syllabify(word)
		else:
			return self.auto_syllabify(word)
	
	@abc.abstractmethod
	def auto_syllabify(self, word: str):
		"""Takes a string representing a word and returns a list of :class:`AbstractSyllable` child class instances."""
		return []
	
	@abc.abstractmethod
	def manually_syllabify(self, word: str):
		"""Takes a string representing a manually syllabified word and returns a list of :class:`AbstractSyllable` child class instances."""
		return []
		
	def iter_lines(self, json_dict: dict):
		"""Iterates over the lines, yielding both their index and their dictionary representation."""
		text = json_dict["text"]
		for stanza in text["stanzas"]:
			for line in stanza["lines"]:
				yield line
		
		
	def syllabify(self, jdict: dict):
		"""Takes the loaded dictionary of a CruscoPoetry json file, parses it adding to each word its syllabification (if the word is manually syllabified, it also removes brackets and pipeline from the word 
		string) and saves the changes."""

		#we get the text section and iterate over the lines and words:
		for index_line, line in enumerate(self.iter_lines(jdict)):
			try:
				for colon in line["cola"]:
					for word in colon["words"]:
						word["syllables"] = self.syllabify_word(word["string"])
						
						#if the word is manually syllabified, we can remove the brackets now:
						if "[" in word["string"]:
							new_string = word["string"][1:-1]
							new_string = ''.join(new_string.split("|"))
							word["string"] = new_string
			except SyllabificationException as e:
				e.line_number = line_index+1
				raise e


class AbstractMain:
	"""Provides user interface to syllabification."""
	
	_SYLLABIFICATOR = AbstractSyllabificator
	
	@classmethod
	def syllabify(cls, json_dict: dict):
		"""Takes a json dictionary (not a file path) and syllabifies it"""
		syllabificator = cls._SYLLABIFICATOR()
		syllabificator.syllabify(json_dict)

	@classmethod
	def syllabify_file(cls, json_file):

		#we see if the file exists:
		if (not os.path.exists(json_file) or os.path.isdir(json_file)):
			raise RuntimeError("Path '%s' doesn't exist or is a directory."%json_path)
		with open(json_file, 'r') as myfile:
			json_parsing: dict = json.load(myfile)
			cls.syllabify(json_parsing)

		#finally, we save:
		with open(json_file, 'w') as outfile:
			json.dump(json_parsing, outfile)
		print("File '%s' successfully syllabified."%json_file)
		
			
	@classmethod
	def main(cls):
		"""Takes a file name from sys.argv and does the syllabification."""
		parser = argparse.ArgumentParser(prog="syllabifier")
		parser.add_argument("json_file", type=str, help="the path of the json file to syllabify")
		args = parser.parse_args()
		json_file = args.json_file
		cls.execute(json_file)

