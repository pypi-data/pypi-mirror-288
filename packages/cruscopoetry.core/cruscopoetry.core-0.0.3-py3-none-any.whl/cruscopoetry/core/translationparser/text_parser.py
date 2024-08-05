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
import os
import re
from ..markers import Markers


class TranslationLine:
	"""Represents the parsing of the line translation of a poem. This class splits the line in cola and builds :class:`Cola` instances from them.
	
	Args:
		line_string (str): the string representing the line in Cruscopoetry format
	
	Attributes:
		cola (tuple): a tuple of :class:`Cola` instances, representing the cola of the poem.
		label (str): the label attributed to the verse, or None if no label has been specified.
	"""
	
	LABEL_REGEX = re.compile("^\\s*(\(\\$(?P<label>\\w+)\))?\\s*(?P<line>.+)$")
	
	def __init__(self, index: int, line_string: str):
		self.index = index
		match = self.__class__.LABEL_REGEX.match(line_string)
		self.label = match.group("label")
		self.line = match.group("line")

	@property
	def number(self):
		return self.index+1
		
	def __repr__(self):
		ret_str = "%d"%self.number
		if self.label != None:
			ret_str += "-$%s"%self.label
		ret_str += " " + self.line
		return ret_str
		
	def json_dict(self):
		"""Returns a JSON-serializable dictionary with two fields: `reference`, containing the label of the source line of the translation or, if not specified, the number, and `text`, containing 
		the text of the translation"""
		ret_dict = {}
		ret_dict["reference"] = self.label if self.label != None else self.number
		ret_dict["text"] = self.line
		return ret_dict
		

class TranslationText:
	"""Represents the parsing of a *TEXT* section of the translation of a poem. This class adjust the whitespace formatting of the text string and parses its lines 
	in :class:`TranslationLine` instances.
	
	Args:
		text_string (str): the string representing the text in Cruscopoetry format
	
	Attributes:
		lines (tuple): a tuple of :class:`TranslationLine` instances, representing the translated lines of the poem.
	"""

	LINE_SEP = os.linesep	

	#this regex exception, employed with re.sub,  trims all the lines internal in the string:
	ONLY_WHITESPACES_LINES ="[^\\S\n\r]*" + os.linesep + "[^\\S\n\r]*"

	def __init__(self, text_string: str):
		text_string = re.sub(self.__class__.ONLY_WHITESPACES_LINES, self.__class__.LINE_SEP, text_string)
		text_string = re.sub(re.compile("^[^\\S\n\r]*" + self.__class__.LINE_SEP), "", text_string)
		text_string = re.sub(re.compile(self.__class__.LINE_SEP + "[^\\S\n\r]*$"), "", text_string)

		#after having trimmed the lines, we find the occurrences of three or more line separator characters and replace them with one occurrence (corresponding to a line boundariy):
		text_string = re.sub("%s{2,}"%self.__class__.LINE_SEP, self.__class__.LINE_SEP, text_string)

		#then, we find comments and delete them and the newline they end with from the text:
		text_string = re.sub("%s.*"%Markers.COMMENT, "", text_string)
		
		#now we can split text_string and obtain a tuple of TranslationLine Objects.		
		self.lines: tuple = tuple(TranslationLine(index, line) for index, line in enumerate(text_string.split(self.__class__.LINE_SEP)))
		
	def __repr__(self):
		return self.__class__.LINE_SEP.join((line.__repr__() for line in self.lines))

	def iter_lines(self):
		yield from self.lines
	
	def json_array(self):
		"""Returns a JSON-serializable array representing the translation"""
		return [line.json_dict() for line in self.lines]
