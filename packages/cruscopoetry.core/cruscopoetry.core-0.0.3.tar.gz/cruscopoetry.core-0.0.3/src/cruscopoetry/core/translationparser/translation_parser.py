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
from ..base_parser import BaseParser
from .metadata_parser import TranslationMetadata
from .text_parser import TranslationText
from .source_notes_parser import TranslatedSourceNotes, NullTranslatedSourceNotes
from .translation_notes_parser import TranslationNotes, NullTranslationNotes
import os


class TranslationParser(BaseParser):
	"""Represents the parsing of a translation file.
	
	Attributes:
		metadata: the metadata of the translation
		text: the translated text body, line by line
		notes: the translations of the notes present in the source text
		translation_notes: the notes not present in the source and added in the translation
	"""

	def __init__(self, file_path: str):
		super().__init__(file_path)
		with open(self.path, 'r') as myfile:
			translation = myfile.read()
		
		parser = SectionsParser(translation)
		metadata, text, source_notes, translation_notes = parser.sections
		self.metadata = TranslationMetadata(metadata)
		self.text = TranslationText(text)
		self.source_notes = TranslatedSourceNotes(source_notes) if source_notes != None else NullTranslatedSourceNotes()
		self.translation_notes = TranslationNotes(translation_notes) if translation_notes != None else NullTranslationNotes()

	def json_dict(self):
		ret_dict = self.metadata.json_dict()
		ret_dict["lines"] = self.text.json_array()
		ret_dict["source_notes"] = self.source_notes.json_array()
		ret_dict["translation_notes"] = self.translation_notes.json_array()
		return ret_dict
		
	def __repr__(self):
		ret_str = "METADATA" + os.linesep + "%r"%self.metadata
		ret_str += os.linesep + "TEXT" + os.linesep + "%r"%self.text
		ret_str += os.linesep + "SOURCE_NOTES" + os.linesep + "%r"%self.source_notes
		ret_str += os.linesep + "TRANSLATION_NOTES" + os.linesep + "%r"%self.translation_notes
		return ret_str


class SectionsParser:

	def __init__(self, poem_translation: str):
		regex_pattern = "^.*?METADATA" + os.linesep + "\\s*(?P<metadata>.*?)" 
		regex_pattern += os.linesep + "TEXT" + os.linesep + "\\s*(?P<text>.*?)"
		regex_pattern += "(" + os.linesep + "SOURCE_NOTES" + os.linesep + "\\s*(?P<source_notes>.*?))?"
		regex_pattern += "(" +  os.linesep + "TRANSLATION_NOTES" + os.linesep + "\\s*(?P<translation_notes>.*?))?"
		regex_pattern += "$"
		regex = re.compile(regex_pattern, re.DOTALL)
		matches = regex.match(poem_translation)
		metadata = matches.group("metadata")
		text = matches.group("text")
		source_notes = matches.group("source_notes")
		translation_notes = matches.group("translation_notes")
		self.sections: tuple = (metadata, text, source_notes, translation_notes)
