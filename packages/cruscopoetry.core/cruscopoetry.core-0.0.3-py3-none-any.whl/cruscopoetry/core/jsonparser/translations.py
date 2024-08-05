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
from .exceptions import *
from .utils import MetadataDict, MetadataValidator
from .joiners import Joiners
from .text_parser import JsonLine
from .notes_parser import JsonNote


class JsonTranslationNote:
	"""Represent a translation note of in the Json file.
	
	Args:
		jdict (dict): the section of the JSON file representing the translation note

	Attrs:
		reference (str): the number or label of the line the note is referenced to
		text (str): the text of the note
	"""
	
	def __init__(self, jnote: dict):
		reference = str(jnote["reference"])
		self.reference = reference if reference[0] != '$' else reference[1:]
		self.text = jnote["text"]
		
	def __repr__(self):
		return "<" + self.__class__.__name__ + " (" + self.reference + ")" + " " + self.text + ">"


class JsonTranslation:
	"""Represents one of the possible translations of the poem.
	
	Args:
		jdict (dict): the section of the JSON file representing the translation's metadata
	
	Attrs:
		jdict (MetadataDict): the section of the JSON file representing the translation's metadata
	"""

	def __init__(self, jdict):
		#first we instantiate JsonTranslationNote instances from the items in the jdict["notes"] array:
		jdict["source_notes"] = [JsonTranslationNote(note) for note in jdict["source_notes"]]
		jdict["translation_notes"] = [JsonTranslationNote(note) for note in jdict["translation_notes"]]
		requirements = [
			("id", True, False, MetadataValidator.NO_CONTROL),
			("metadata", True, False, MetadataValidator.NO_CONTROL),
			("language", True, False, MetadataValidator.NO_CONTROL),
			("lines", True, False, MetadataValidator.NO_CONTROL),
			("source_notes", True, False, MetadataValidator.NO_CONTROL),
			("translation_notes", True, False, MetadataValidator.NO_CONTROL),
		] #since metadata and notes contain mutable objects (lists and dictionaries) we can set them as invariable
		validator = MetadataValidator(requirements)
		self.jdict = MetadataDict(jdict, validator)

	def json_dict(self):
		"""Returns the translation dictionary with eventual updates."""
		return self.jdict.dict
		
	@property
	def id(self):
		"""The id of the translation. This property can not be modified."""
		return self.jdict["id"]
	
	@id.setter
	def id(self, value):
		#forwards the exception raised by MetadataValidator
		try:
			self.jdict["id"] = value
		except InvariableFieldError as e:
			raise e
		
	@property
	def language(self):
		"""The language of the translation. This property can not be modified."""
		return self.jdict["language"]
	
	@language.setter
	def language(self, value):
		#forwards the exception raised by MetadataValidator
		try:
			self.jdict["id"] = value
		except InvariableFieldError as e:
			raise e
	
	@property
	def metadata(self):
		"""The keys of the optional metadata fields"""
		return self.jdict["metadata"]
	
	@metadata.setter
	def metadata(self, value):
		#forwards the exception raised by MetadataValidator
		try:
			self.jdict["id"] = value
		except InvariableFieldError as e:
			raise e
	
	@property
	def lines(self):
		"""The translated lines"""
		return self.jdict["lines"]

	@property
	def source_notes(self):
		"""Returns the translated source notes"""
		return self.jdict["source_notes"]

	@property
	def translation_notes(self):
		"""Returns the notes added in the translation"""
		return self.jdict["translation_notes"]

	@property
	def notes(self):
		"""Returns all the notes of the translation (both the translated notes from the source and the new ones added in the translation)"""
		ret_array = self.source_notes.extend(self.translation_notes)
		return ret_array
	
	@id.setter
	def id(self, value):
		#forwards the exception raised by MetadataValidator
		try:
			self.jdict["id"] = value
		except InvariableFieldError as e:
			raise e
	
	@property
	def mandatory_items(self):
		return (
			("id", self.id),
			("language", self.language)
		)
		
	def update_metadata(self, meta_dict: dict):
		"""Updates the translation metadata with the information enclosed in meta_dict."""
		self.jdict["metadata"].update(meta_dict)
		
	@property
	def as_text(self):
		"""A plain text representation of the translation's metadata (useful if one wants to build back the txt file)"""
		fields = ["id%s%s"%(Joiners.METADATA_FIELDS_INTERNAL, self.id), "language%s%s"%(Joiners.METADATA_FIELDS_INTERNAL, self.language)]
		fields.extend(["%s = %s"%(key, self.metadata[key]) for key in self.metadata.keys()])
		return Joiners.METADATA_FIELDS.join(fields)
		
	def __str__(self):
		return "%s(%r)"%(self.__class__.__name__, self.jdict.dict)
		
	def get_line_translation(self, jline: JsonLine) -> str:
		"""Takes a JsonLine instance and return the corresponding translated text if present, else None. If to the same line two translations correspond (one referenced by label and one by number) 
		the one referenced by label will be returned."""
		if jline.label != None:
			for line in self.lines:
				if line["reference"] == jline.label:
					return line["text"]
		for line in self.lines:
			if line["reference"] == jline.number_in_poem:
				return line["text"]
		print("\u001b[33mNo translation found for line number %d\u001b[0m"%jline.number_in_poem)
		return None
	
	def get_source_note_translation(self, jnote: JsonNote) -> str:
		"""Takes a JsonNote instance and return the corresponding translated text if present, else None. If to the same note two translations correspond (one referenced by label and one by number) 
		the one referenced by label will be returned."""
		if jnote.label != None:
			for note in self.source_notes:
				if note.reference == jnote.label:
					return note.text
		jnote_number = str(jnote.number)
		for note in self.source_notes:
			if note.reference == jnote_number:
				return note.text
		print("\u001b[33mNo translation found for source note number %s\u001b[0m"%jnote_number)
		return None					
		
		
class JsonTranslations:

	def __init__(self, jdict: dict):
		self.jdict = jdict
		self._iter_index = 0
		
	def __contains__(self, translation_id: str):
		"""Checks if the translation with id ``translation_id`` is in the translations list."""
		return translation_id in self.jdict.keys()
	
	def get_translation_by_id(self, tr_id: str):
		"""Returns the translation with the given id."""
		if tr_id in self:
			ret_dict = {"id": tr_id}
			data = self.jdict[tr_id]
			if data != None:
				ret_dict.update(data)
				return JsonTranslation(ret_dict)
		return None
		
	def __str__(self):
		return "%r"%self.jdict
		
	def __len__(self):
		"""Returns the number of translations contained in the instance."""
		return len(self.jdict)
	
	@property
	def translation_id_keys(self):
		return tuple(sorted(self.jdict.keys()))

	def __next__(self):
		if self._iter_index < len(self.jdict):
			tr_id = self.translation_id_keys[self._iter_index]
			to_yield = self.get_translation_by_id(tr_id)
			self._iter_index += 1
			return to_yield
		else:
			self._iter_index = 0
			raise StopIteration

	def __iter__(self):
		self._iter_index = 0
		return self
		
	def json_dict(self):
		"""Returns the metadata dictionaries of all the translations."""
		return self.jdict
		
	def append(self, translation_dict: dict):
		"Appends a new translation to self.jdict if there isn't already one with the same id. If there is, it will update it."
		tr_id = translation_dict["id"]
		tr_language = translation_dict["language"]
		tr_dict = {key: value for key, value in translation_dict["metadata"].items() if key != "id"}
		self.jdict[tr_id] = {
			"metadata": translation_dict["metadata"],
			"language": tr_language,
			"lines": translation_dict["lines"],
			"source_notes": translation_dict["source_notes"],
			"translation_notes": translation_dict["translation_notes"]
		}
			
	def delete(self, tr_id: str):
		"""Deletes the translation whose id is tr_id"""
		del self.jdict[tr_id]
		
	@property
	def as_text(self):
		ret_str = Joiners.LINES + "TRANSLATIONS:"
		for translation in self:
			ret_str += Joiners.LINES + translation.as_text
		return ret_str
