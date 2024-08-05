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


class SyllabificationException(Exception):

	def __init__(self):
		super().__init__()
		self.line_number = None


class UnknownChar(SyllabificationException):

	def __init__(self, char):
		super().__init__()
		self.char = char
		
	@property
	def quotation_mark(self):
		return "'" if self.char != "'" else '"'
	
	def __str__(self):
		return "Unrecognized character %s%s%s found at line %d"%(self.quotation_mark, self.char, self.quotation_mark, self.line_number)


class InvalidNucleumSyntax(SyllabificationException):

	def __init__(self, string):
		super().__init__()
		self.string = string
	
	def __str__(self):
		return "The string '%s' is not a valid token for a syllabic nucleum (either the phoneme is not a vowel or there is number before it out of the (0, 7) range."%self.string
