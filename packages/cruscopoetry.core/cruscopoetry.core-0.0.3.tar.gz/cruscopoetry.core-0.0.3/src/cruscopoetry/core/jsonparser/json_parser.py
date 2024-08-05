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
import json
from ..base_parser import *	
from .metadata_parser import JsonMetadata
from .notes_parser import JsonNotes
from .text_parser import JsonText
from .translations import JsonTranslations
from ..translationparser.translation_parser import TranslationParser
from functools import singledispatchmethod


class JsonPoemCore:
	"""Represents the core section, which is read-only, of the poem.
	
	Args:
		poem_core (dict): the dictionary representing the poem's core
	
	Attrs:
		self.translations (JsonTranslations): the translations of the poem;
		self.metadata (JsonMetadata): the metadata of the poem;
		self.text (JsonText): the text of the poem;
		self.notes (JsonNotes): the notes of the poem;
	"""
	
	def __init__(self, poem_core: dict):
		self.translations = JsonTranslations(poem_core["translations"])
		self.metadata = JsonMetadata(poem_core["metadata"])
		self.text = JsonText(poem_core["text"], self.translations)
		self.notes = JsonNotes(poem_core["notes"], self.translations)
		
	@property
	def title(self):
		return self.metadata["title"]
			
	@property
	def as_text(self):
		ret_str = os.linesep.join((self.metadata.as_text, self.text.as_text, self.notes.as_text))
		ret_str += os.linesep*3 + "Translations:" + os.linesep*2
		for translation in self.translations.iter():
			ret_str += translation.as_text
			for line in self.text.iter_lines():
				ret_str +=  os.linesep + "\t"
				tr_line = line.get_translation_by_id(translation.translation_id)
				if tr_line != None:
					ret_str += tr_line
		return ret_str


	def _add_translation(self, translation_object: TranslationParser):
		"""Protected method wrapped by :method`add_translation`. Adds the dictionary representing the translation to the document."""
		self.translations.append(translation_object.json_dict())
			

	@singledispatchmethod
	def add_translation(self, tr_object):
		"""Adds a translation to this file from a document written in Cruscopoetry format.
		If a translation with the same id is already in the poem, this function will update it
		"""
		raise RuntimeError("Not implemented for objects of type '%s'"%tr_object.__class__.__name__)
	
	@add_translation.register(str)
	def add_translation_from_str_path(self, translation_path: str):
		translation_object = TranslationParser(translation_path)
		self._add_translation(translation_object)
	
	@add_translation.register(TranslationParser)
	def add_translation_from_parser_object(self, translation_object: TranslationParser):
		self._add_translation(translation_object)
	
	def delete_translation(self, tr_id: str) -> bool:
		"""Search in the poem a translation by its and deletes it if it exists. Returns True if it has deleted the translation, False 
		if it was not there."""
		if tr_id in self.translations:
			self.translations.delete(tr_id)
			self.text.delete_translation(tr_id)
			self.notes.delete_translation(tr_id)
			return True
		return False
			
	def list_translations(self) -> tuple:
		"""Returns a tuple with pairs of id and language for each of the translations inserted in the document."""
		ids = tuple((translation.id, translation.language) for translation in self.translations)
		return ids
		
	def has_translation(self, tr_id: str):
		return tr_id in self.translations
	
	def json_dict(self) -> dict:
		ret_dict = {
			"metadata": self.metadata.json_dict(),
			"text": self.text.json_dict(),
			"notes": self.notes.json_dict(),
			"translations": self.translations.json_dict()
		}
		return ret_dict	

class JsonParser(BaseParser):
	"""Represent the parsing of a json file produced by a poem in Cruscopoetry format.
	Json files should not be used for editing of a poem, but for parsing and analyzing. An exception is represented by the addition of translations, which is done directly to these files.
	
	Args:
		json_path (str): the path of the file to be parsed.
	
	Attrs:
		path (str): the path of the parsed file.
		json (json.JsonParser): the parsing of the json file.	
		
	Raises:
		InvalidPathError: raised if the file doesn't exist or is a directory.
	"""
	
	def __init__(self, json_path: str):
		super().__init__(json_path)
		self._json = None
		with open(self.path, 'r') as myfile:
			self._json: json.JsonParser = json.load(myfile)

		self._core = JsonPoemCore(self._json["core"])
		self._plugins = self._json["plugins"]
		
	@property
	def core(self):
		return self._core
		
	@property
	def plugins(self):
		return self._plugins
	
	@property
	def title(self):
		return self.core.title
		
	@property
	def translations(self):
		return self.core.translations
		
	@property
	def metadata(self):
		return self.core.metadata
		
	@property
	def text(self):
		return self.core.text
		
	@property
	def notes(self):
		return self.core.notes
		
	def save(self, path=None):
		"""Save all the updates on the JSON file. If the path to save is the same of the orginal JSON document (as default), after saving it is no longer possible to undo the editing.
		
		Args:
			path (str): the path to save the updated JSON poem on. Default is self.path (that is, the path, of the original file).
		"""
		if path == None:
			path = self.path
		with open(path, 'w') as outfile:
			json.dump(self.json_dict(), outfile)
			
	@property
	def as_text(self):
		return self.core.as_text
		
	def add_translation(self, tr_object):
		self.core.add_translation(tr_object)	

	def delete_translation(self, tr_id: str) -> bool:
		return self.core.delete_translation(tr_id)
	
	def list_translations(self) -> tuple:
		return self.core.list_translations()
	
	def has_translation(self, tr_id: str) -> bool:
		return self.core.has_translation(tr_id)
	
	def json_dict(self) -> dict:
		ret_dict = {
			"core": self.core.json_dict(),
			"plugins": self.plugins
		}
		return ret_dict	
