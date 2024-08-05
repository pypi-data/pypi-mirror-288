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
	"""Represents the parsing of a note added in the translation.
	
	Args:
		note_string (str): the string representing the note in Cruscopoetry format
	
	Attributes:
		reference (str): the translation's reference to a line in the original;
		text (str): the note's text
	"""
	
	LABEL_REGEX = re.compile("\\s*(\\((?P<reference>\\$?[\\w\\d]+)\\))\\s*(?P<text>.+)", re.DOTALL)
	
	def __init__(self, note_string: str):
		match = self.__class__.LABEL_REGEX.match(note_string)
		if match == None:
			raise RuntimeError("Syntax error in translation note: '%s'"%note_string)
		self.reference = match.group("reference")
		self.text = match.group("text")
		
	def __repr__(self):
		ret_str = ""
		ret_str += "(%s)"%self.reference
		ret_str += " " + self.text
		return ret_str
	
	def json_dict(self):
		ret_dict = {
			"reference": self.reference,
			"text": self.text
		}
		return ret_dict
		

class TranslationNotes:
	"""Represents the parsing of the *TRANSLATION_NOTES* section of the translation of a poem.	

	Args:
		notes_string (str): the string representing the notes section in CruscoPoetry format
	
	Attributes:
		notes (tuple): a tuple of :class:`TranslatedSourceNote` instances, representing the translated lines of the poem.
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
		#it is important that re.DOTALL is passed as keyword argument. This because is integer
		#value is 2. If it was passed as the third positional argument it would correspond 
		#to maxsplit, that is, the maximum number of splits we want to do (unlimited if 0):
		#therefore, the function would split only two elements and leave the rest all joined.
		notes = re.split(Markers.NOTES_SEP, notes_string, flags=re.DOTALL) 
		self.notes: tuple = tuple(TranslationNote(note) for note in notes)
		
	def json_array(self):
		return tuple(note.json_dict() for note in self.notes)
		
	def __repr__(self):
		return Markers.NOTES_SEP.join((note.__repr__() for note in self.notes))

	def __iter__(self):
		yield from self.notes
		
		
class NullTranslationNotes(TranslationNotes):
	"""Null class, instantiated if no translation note is present in the document."""
	
	def __init__(self):
		self.notes = tuple()
