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
from .text_element import Joiners
from .exceptions import NullSourceNoteException


class JsonNote:
	"""Represent a note from a Cruscopoetry Json file.

	Attrs:
		jdict (dict): the dictionary from which the note is istantiated;
		index (integer): the index of the note in the array containing all the notes in the JSON file.
	"""

	def __init__(self, index, jdict, translations):
		self.index = index
		self.__jdict = jdict
		self._translations = translations
	
	def json_dict(self):
		return self.__jdict
	
	@property
	def number(self):
		"""The number of the note, that is, a progressive integer (starting from 1) which is assigned to each note following their order of occurrence in the txt source file."""
		return self.index+1
		
	@property
	def label(self):
		"""The note's label if it exists, else None."""
		return self.__jdict["label"]
		
	@property
	def reference(self):
		return self.__jdict["reference"]
		
	@property
	def text(self):
		return self.__jdict["text"]

	@property
	def as_text(self):
		return Joiners.NOTES.join((self.reference, self.text))
		
	def get_translation_by_id(self, translation_id: str):
		translation = self._translations.get_translation_by_id(translation_id)
		translated_text = translation.get_source_note_translation(self)
		return translated_text
			

class JsonNotes:
	"""Represents the all the notes of a CruscoPoetry json poem."""
	
	def __init__(self, jarray, translations):
		self.jarray = jarray
		self._translations = translations
		
	def json_dict(self):
		return self.jarray
	
	def iter_notes_dict(self):
		yield from self.jarray
	
	def iter_notes(self):
		for index, note in enumerate(self.iter_notes_dict()):
			yield JsonNote(index, note, self._translations)

	def __len__(self):
		return len(self.jarray)
			
	def _get_note_by_number(self, number: int) -> JsonNote:
		for note in self.iter_notes():
			if note.number == number:
				return note
		return None 
			
	def _get_note_by_label(self, label: str) -> JsonNote:
		for note in self.iter_notes():
			if note.label == label:
				return note
		return None 

	def get_source_note_translation(self, translation_note) -> bool:
		"""Return the source note instance if the translation note corresponds to a translated note in the source, else None"""
		if translation_note.label != None:
			source = self._get_note_by_label(translation_note.label)
		else:
			source = self._get_note_by_number(translation_note.number)
		#if the research has failed, source will be None
		return source
		
	@property
	def as_text(self):
		ret_string = "NOTES"
		for note in self.iter_notes():
			ret_string += "\n%s"%note.as_text
		return ret_string
