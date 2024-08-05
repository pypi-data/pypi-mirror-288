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


class TranslationNote:
	"""Represents the parsing of a note translation of the poem.
	
	Args:
		note_string (str): the string representing the note in Cruscopoetry format
	
	Attributes:
		label (str): the label attributed to the verse, or None if no label has been specified.
		reference (str): the note'sreference to a line, or to the whole text;
		text (str): the translated text
	"""
	
	LABEL_REGEX = re.compile("^\\s*(\\$(?P<reference>\\w+)\\s)?\\s*(?P<text>.+)$")
	
	def __init__(self, index: int, line_string: str):
		self.index = index
		match = self.__class__.LABEL_REGEX.match(line_string)
		self.reference = match.group("reference")
		self.text = match.group("text")

	@property
	def number(self):
		return self.index+1
		
	def __repr__(self):
		ret_str = "%d"%self.number
		if self.reference != None:
			ret_str += "-$%s"%self.reference
		ret_str += " " + self.text
		return ret_str
		

class TranslationNotes:
	"""Represents the parsing of the *NOTES* section of the translation of a poem.	

	Args:
		notes_string (str): the string representing the notes section in Cruscopoetry format
	
	Attributes:
		notes (tuple): a tuple of :class:`TranslationNote` instances, representing the translated lines of the poem.
	"""

	ONLY_WHITESPACES_LINES ="[^\\S\n\r]*" + os.linesep + "[^\\S\n\r]*"

	def __init__(self, notes_string: str):
	
		notes_string = re.sub(self.__class__.ONLY_WHITESPACES_LINES, os.linesep, notes_string)
		notes_string = re.sub("^[^\\S\n\r]*"+os.linesep, "", notes_string)
		notes_string = re.sub(os.linesep+"[^\\S\n\r]*$", "", notes_string)

		#after having trimmed the lines, we find the occurrences of three or more line separator characters and replace them with two occurrences of them (corresponding to notes boundaries):
		notes_string = re.sub("%s{3,}"%os.linesep, Markers.NOTES_SEP, notes_string)

		#then, we find comments and delete them and the newline they end with from the text:
		notes_string = re.sub("%s.*"%Markers.COMMENT, "", notes_string)
		
		#now we can split notes_string and obtain a tuple of Note Objects:
		notes = re.split(Markers.NOTES_SEP, notes_string, re.DOTALL)
		self.notes: tuple = tuple(TranslationNote(index, notes[index]) for index in range(len(notes)))
		
	def __repr__(self):
		return Markers.NOTES_SEP.join((note.__repr__() for note in self.notes))

	def __iter__(self):
		yield from self.notes
		
		
class NullTranslationNotes(TranslationNotes):
	"""Null class for translations without notes. It contains self.notes as an empty tuple."""
	
	def __init__(self):
		self.notes = tuple()
