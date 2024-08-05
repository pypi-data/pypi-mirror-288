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
from .exceptions import SyllabificationException, UnknownChar
from typing import Tuple


class AbstractPhoneme(metaclass=abc.ABCMeta):
	"""Abstract class for all the phoneme objects that can be instantiated from the tokens returned by AbstractTokenizer.tokenize() (and the same method of descendants)."""

	def __init__(self, string: str):
		self._base = string

	@property
	def base(self):
		"""Returns the base sound of the phoneme, without taking into account processes such as prenasalization, labialization, aspiration, etc."""
		return self._base
	
	@abc.abstractproperty
	def string(self):
		"""Represents both the phoneme's base sound and the processes that could have affected it."""
		return self._base
		
	@property
	def plain_text_string(self) -> str:
		"""Returns a string representing the phoneme in CruscoPoetry txt format."""
		return self._base
		
	@abc.abstractproperty
	def json_dict(self):
		"""Returns the dictionary that will represent the phoneme in the json file"""
		return {"base": self._base}
	
	
class AbstractConsonant(AbstractPhoneme):
	"""Abstract class for all the consonantal phonemes."""
	def __init__(self, string: str):
		super().__init__(string)
		

class AbstractVowel(AbstractPhoneme):
	"""Abstract class for all the vowel phonemes. As vowel, here is meant any phoneme which can be the nucleum of a syllable, and thus bear indications about the syllabic stress."""

	STRESS_REGEX = re.compile("(?P<stress>[0-7])?(?P<vowel>[^_\\W]{1,2})(_(?P<crasis_vowel>\\w{1,2}))?")

	def __init__(self, string):
		stress, vowel, crasis_vowel = self.parse_nucleum(string)
		super().__init__(vowel)
		self._stress = stress
		self._crasis_vowel = crasis_vowel
		
	@property
	def stress(self):#we don't code a stress.setter, but we will code getters and setters for each of the three stress types
		return self._stress
		
	@property
	def phonetic_stress(self) -> bool:
		#we return True if self.stress & 1 == 1
		return (self._stress & 1) == 1
	
	@phonetic_stress.setter
	def phonetic_stress(self, value: bool):
		#if value is True, the last bit of self.stress must be set to 1, else to 0:
###		print("setting phonetic stress:", self.stress, "->", end=" ")
		if value:
			self._stress = self._stress | 1
		else:
			self._stress = self._stress & ~1
###		print(self.stress)

	@property
	def metric_stress(self):
		#we return True if self.stress & 2 == 2
		return self._stress & 2 == 2
	
	@metric_stress.setter
	def metric_stress(self, value: bool):
		#if value is True, the penultimate bit of self.stress must be set to 1, else to 0:
		if value:
			self._stress = self._stress | 2
		else:
			self._stress = self._stress & ~2

	@property
	def semantic_stress(self):
		#we return True if self.stress & 4 == 4
		return self._stress & 4 == 4
	
	@semantic_stress.setter
	def semantic_stress(self, value: bool):
		#if value is True, the thirs-last bit of self.stress must be set to 1, else to 0:
		if value:
			self._stress = self._stress | 4
		else:
			self._stress = self._stress & ~4
	
	@property
	def crasis_vowel(self):
		return self._crasis_vowel
	
	@crasis_vowel.setter
	def crasis_vowel(self, value):
		self._crasis_vowel = value
		
	@abc.abstractproperty
	def json_dict(self):
		"""Returns the dictionary that will represent the phoneme in the json file"""
		ret_dict =  {
			"base": self._base,
			"stress": self.stress,
		}
		
		if self.is_from_crasis:
			ret_dict["crasis"] = [self._base, self._crasis_vowel]
		else:
			ret_dict["crasis"] = None
		
		return ret_dict
	
	@property
	def is_from_crasis(self):
		return self.crasis_vowel != None
		
	@property
	def plain_text_string(self) -> str:
		"""Returns a string composed by self.stress if self.stress != 0, self._base, and if self.crasis_vowel != None also '_' + self.crasis_vowel. It would be the representation of the vowel 
		in CruscoPoetry txt format."""
		ret_str = ""
		if self.stress > 0:
			ret_str += str(self.stress)
		ret_str += self._base
		if self.is_from_crasis:
			ret_str += "_%s"%self.crasis_vowel
		return ret_str

	def parse_nucleum(self, token: str) -> Tuple[int, str, str]:
		"""This function parses the token string representing a syllabic nucleum (and that thus be preceded by a number from 0 to 7 representing its stress). It returns the vowel phoneme and the 
		stress as a pair.
		
		Args:
			token (str): the token to be parsed. It can be just a vowel or a 0-7 number followed by a vowel.
		
		Returns:
			stress (int): the stress number if specified, else 0
			vowel (str): the vowel represented in the token
			crasis_vowel (str): the second vowel tied to the first by crasis if exists, else None
		
		Raises:
			InvalidNucleumSyntax: raised is the stress number is not between 0 and 7.
		"""
		match = self.__class__.STRESS_REGEX.match(token)

		stress = match.group("stress")
		stress = int(stress) if stress != None else 0

		vowel = match.group("vowel")
		crasis_vowel = match.group("crasis_vowel")
		if ((stress < 0) or (stress > 7)):
			raise InvalidNucleumSyntax(token)
			
		return stress, vowel, crasis_vowel


class AbstractSyllable(abc.ABC):
	"""Represents an abstract class for syllables. Children of this class must implement the method json_dict, which returns the syllable's data in a dictionary that can be JSONified."""
	
	@abc.abstractmethod
	def iter_phonemes(self):
		"""Iterates over the syllable's phonemes."""
		pass

		
	@abc.abstractproperty
	def stress(self) -> int:
		pass
		
	@abc.abstractproperty
	def json_dict(self):
		"""Returns the dictionary that represents the syllable and that will be stored in the json file.
		While implementing this function, it is recommended to return from AbstractSyllable.json_dict. The super() property in fact will return a dictionary containing the basic information about 
		the syllable that should be found in the JSON file for any language."""
		ret_dict = {
			"stress": self.stress,
			"phonemes": tuple(phoneme.json_dict for phoneme in self.iter_phonemes())
		}
		return ret_dict
	
	@abc.abstractproperty	
	def as_string(self):
		"""Returns the syllable represented in a human legible string. If the str() function is called on the instance, the value given by this method is returned."""
		return ""
		
	def __str__(self):
		return self.as_string
		
	#the following properties are delegated to self.nucleum:
	@property
	def phonetic_stress(self) -> bool:
		return self.nucleum.phonetic_stress
	
	@phonetic_stress.setter
	def phonetic_stress(self, value: bool):
###		print("setting phonetic stress:", self.stress, "->", end=" ")
		self.nucleum.phonetic_stress = value
###		print(self.stress)

	@property
	def metric_stress(self):
		#we return True if self.stress & 2 == 2
		return self.nucleum.metric_stress
	
	@metric_stress.setter
	def metric_stress(self, value: bool):
		self.nucleum.metric_stress = value

	@property
	def semantic_stress(self):
		#we return True if self.stress & 4 == 4
		return self.nucleum.semantic_stress
	
	@semantic_stress.setter
	def semantic_stress(self, value: bool):
		self.nucleum.semantic_stress = value


class AbstractSyllabifier(metaclass=AbstractSingleton):
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
		text = json_dict["core"]["text"]
		for stanza in text["stanzas"]:
			for line in stanza["lines"]:
				yield line

	def syllabify(self, jdict: dict):
		"""Takes the loaded dictionary of a CruscoPoetry json file, parses it adding to each word its syllabification (if the word is manually syllabified, it also removes brackets and pipeline from the word 
		string) and saves the changes."""

		#we get the text section and iterate over the lines and words:
		for line_index, line in enumerate(self.iter_lines(jdict)):
			try:
				for colon in line["cola"]:
					for word in colon["words"]:
						word["syllables"] = self.syllabify_word(word["string"])
						
						#if the word is manually syllabified, we can remove the brackets now:
						if "[" in word["string"]:
							new_string = word["string"][1:-1]
							new_string = ''.join(new_string.split("|"))
							word["string"] = new_string
			except UnknownChar as e:
				e.line_number = line_index+1
				print("\u001b[1;33mWarning: %s. I'll just skip it.\u001b[0m"%str(e))
			except SyllabificationException as e:
				e.line_number = line_index+1
				raise e
			except Exception:
				print("\u001b[1;31mUnexpected exception at line %d, word '%s'\u001b[0m"%(line_index+1, word["string"]))
				raise


class AbstractMain:
	"""Provides user interface to syllabification."""
	
	_SYLLABIFIER = AbstractSyllabifier
	
	@classmethod
	def syllabify(cls, json_dict: dict):
		"""Takes a json dictionary (not a file path) and syllabifies it"""
		syllabifier = cls._SYLLABIFIER()
		syllabifier.syllabify(json_dict)

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

