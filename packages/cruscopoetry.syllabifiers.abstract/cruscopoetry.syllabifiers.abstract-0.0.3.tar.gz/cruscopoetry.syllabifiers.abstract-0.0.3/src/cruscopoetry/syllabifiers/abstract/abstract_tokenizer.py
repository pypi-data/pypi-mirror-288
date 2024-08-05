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
from typing import Tuple
from .markers import Markers
from .exceptions import UnknownChar, InvalidNucleumSyntax
import re
from mum import AbstractSingleton
import abc


class AbstractTokenizer(metaclass=AbstractSingleton):
	"""Utility class for syllable parasing in Cruscopoetry format. This class tokenizes the word string in single characters or character clusters, each one corresponding to a phoneme. If the phoneme
	is a vowel and it is preceded by an integer from 0 to 7 indicating its stress, the integer and the vowel will be grouped in the same token. Markers, such as the one for crasis, are instead 
	treated as separated tokens.
	This is an abstract class, and all its descendant will produce Singleton objects.
	
	Args:
		consonants (Tuple[str]): a tuple of strings representing each one the consonant phonemes.
		vowels (Tuple[str]): a tuple of strings representing each one the vowels phonemes. The strings contained here are expected to be found also next to stress markers.
	
	Attrs:
		consonants (Tuple[str]): a tuple of strings representing each one the consonant phonemes.
		vowels (Tuple[str]): a tuple of strings representing each one the vowels phonemes. The strings contained here are expected to be found also next to stress markers.
	"""

	def __init__(self, consonants: Tuple[str], vowels: Tuple[str]):

		#we need to order both these tuples by decreasing length of the string, in order to make the regular expression parsing work properly:
		self.consonants = self._order_by_length(consonants)
		self.vowels = self._order_by_length(vowels)

	def _order_by_length(self, seq: Tuple[str]) -> Tuple[str]:
		"""Takes a tuple of strings and orders it by decreasing length."""
		ret_seq = sorted(seq, key = lambda item: len(item), reverse = True)
		return tuple(ret_seq)
		

	@property
	def markers(self):
		return tuple(Markers.iter_all())
		
	@property
	def _tokens_regex(self) -> re.Pattern:
		"""The regex for tokenizing a string"""
		
		#once passed to re.findall, this regex will yield pairs: in each pair the first item will be a string if ti corresponds to one of the language's phonemes; if it is not, the unrecognized 
		#character will be in the second item.
		reg_string = "(" + "|".join(self.markers) + "|" + "|".join(self.consonants) + "|" + "([0-7]?(" + "|".join(self.vowels) + "))" + ")|(.)"
		return re.compile(reg_string)
	
	def tokenize(self, string: str) -> Tuple[str]:
		"""Tokenizes a string in a tuple of strings, each one representing a phoneme or a marker character."""
		ret_list = []
		for match in re.findall(self._tokens_regex, string):
			if match[0] != '':			#then there is a character or a cluster of them recognized as a phoneme:
				ret_list.append(match[0])
			else:							#then there is an unknown character:
				raise UnknownChar(match[-1])
		return tuple(ret_list)
		
