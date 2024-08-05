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
import re
import os
from .. import utils
from ...markers import Markers


class Notes:
	"""Represents the notes section of a poem.
	
	Args:
		notes_string (str): the string containing the notes in Cruscopoetry format.
	"""

	ONLY_WHITESPACES_LINES ="[^\\S\n\r]*" + os.linesep + "[^\\S\n\r]*"

	def __init__(self, notes_string: str):
		notes_string = re.sub(self.__class__.ONLY_WHITESPACES_LINES, os.linesep, notes_string)
		notes_string = re.sub("^[^\\S\n\r]*"+os.linesep, "", notes_string)
		notes_string = re.sub(os.linesep+"[^\\S\n\r]*$", "", notes_string)
		#after having trimmed the lines, we find the occurrences of three or more line separator characters and replace them with two occurrences of them (corresponding to stanza boundaries):
		notes_string = re.sub("%s{3,}"%os.linesep, Markers.NOTES_SEP, notes_string)

		#then, we find comments and delete them and the newline they end with from the text:
		notes_string = re.sub("%s.*"%Markers.COMMENT, "", notes_string)
		
		#now we can split notes_string and obtain a tuple of Note Objects:
		notes = re.split(Markers.NOTES_SEP, notes_string, re.DOTALL)

		while '' in notes:
			notes.remove('')		
		self.notes = tuple(Note(note) for note in notes)
	
	def json_dict(self):
		return [note.json_dict() for note in self.notes]


class InvalidReferenceError(Exception):

	def __init__(self, reference):
		super().__init__()
		self.reference = reference
		
	def __str__(self):
		return "Invalid reference: '%s'."%self.reference


class InvalidLabelError(Exception):

	def __init__(self, label):
		super().__init__()
		self.label = label


class LabelError(Exception):

	def __init__(self):
		super().__init__()
		
	def __str__(self):
		return "Labels can not be set as 'all'"


class InvalidNoteError(Exception):

	def __init__(self, note):
		super().__init__()
		self.note = note
		
	def __str__(self):
		return "Invalid note (bad syntax) '%s'."%self.note


class Note:
	"""Represents a note of the poem.
	
	Args:
		note_string (str): the string containing the note in Cruscopoetry format.
		
	Attrs:
		reference (str): the reference of the verse (could be a label or a verse number) the note is about
		text (str): the note's text (in html format)
	"""
	
	PARSE_REGEX = re.compile("\\s*((?P<label>\\$\\w+))?\\s*(\\((?P<reference>\\$?\\w+)\\))\\s*(?P<text>.+)", re.DOTALL)
	
	def __init__(self, note_string):

		#first, we parse the note:
		match = self.__class__.PARSE_REGEX.match(note_string)
		if match == None:
			raise InvalidNoteError(note_string)
		self.label, self.reference, self.text = match.group("label"), match.group("reference"), match.group("text")

		#now we validate the labels and, if everything gets fine, we remove the '$' starting character from them:
		self._validate_labels()
		if self.label != None:
			self.label = self.label[1:] if self.label[0] == '$' else self.label
		self.reference = self.reference[1:] if self.reference[0] == '$' else self.reference
		
	@property
	def as_tuple(self) -> tuple:
		"""Returns a tuple with the values of self.label, self.reference and self.text."""
		return (self.label, self.reference, self.text)

	def _validate_labels(self):
		"""Checks if the note reference is a valid positive integer (referring to a verse number), a valid label (starting with '$' and then containing alphanumeric characters or underscore, or 
		the word `all` (referring to the poem in general). It also checks that the note's label, if exists is a valid label (starting with '$' and then containing alphanumeric characters or 
		underscore).
		
		Raises:
			InvalidLabelError: raised if the note's label exists and is not in a valid format.
			InvalidReferenceError: raised if the note's reference is not in a valid format.
		"""
		validator = utils.Validator()
		if self.label != None:
			if not validator.is_valid_label(self.label):
				raise InvalidLabelError(self.label)
			if self.label == "all":
				raise LabelError
				
		if self.reference.isnumeric():
			return
		if validator.is_valid_label(self.reference):
			return
		if self.reference == "all":
			return
		raise InvalidReferenceError(self.reference)
	
	def json_dict(self) -> dict:
		return {
			"label": self.label,
			"reference": self.reference,
			"text": self.text,
			"translations": {}
		}
