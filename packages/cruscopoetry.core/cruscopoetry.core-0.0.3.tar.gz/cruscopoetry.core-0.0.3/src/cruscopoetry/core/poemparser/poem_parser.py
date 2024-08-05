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
import json
import os
from .metadataparser.metadata_parser import Metadata
from .textparser.text_parser import Text
from .notesparser.notes_parser import Notes
from ..base_parser import *	

class Poem(BaseParser):
	"""Represents a poem. This class performs the operation of parsing the poem and building an json document representing it. The input file must be in cruscopoetry format.
	This class parses the poem up to the word level.
	
	Args:
		poem_path: the path of the poem file, in cruscopoetry format.
	
	Attrs:
		metadata (Metadata): the poem's metadata.
		text (Text): the poem's parsed text.
		notes (Notes): the poem's notes.
		
	Raises:
		InvalidPathError: raised if the file doesn't exist or is a directory.
	"""
	
	def __init__(self, poem_path: str):
		super().__init__(poem_path)
		with open(self.path, 'r') as myfile:
			poem_text = myfile.read()

		parsed = SectionsParser(poem_text)
		metadata, text, notes = parsed.sections
		self.metadata: Metadata = Metadata(metadata)
		self.text: Text = Text(text)
		self.notes: Notes = Notes(notes)

	def json_dict(self) -> dict:
		ret_dict = {
			"core": {#dictionary containing all the data of the text. It is read-only: to modify it one should edit the source first and then rebuild the json dictionary.
				"metadata": self.metadata.json_dict(),
				"text": self.text.json_dict(),
				"notes": self.notes.json_dict(),
				"translations": {}#here general information relative to translations will be stored.
			},
			"plugins": {}#contains the data stored by the plugin applications. This section can be written by the user.
		}
		return ret_dict
		
	def deploy(self, output: str):
		print("Deploying on %s..."%output)
		with open(output, 'w') as outfile:
			json.dump(self.json_dict(), outfile)
		
	def __repr__(self):
		return self.metadata.__repr__() + "\n" + self.text.__repr__()


class SectionsParser:

	def __init__(self, poem_text: str):
		elements = re.split("(METADATA)|(TEXT)|(NOTES)", poem_text)
		elements = [element for element in elements if element not in ("", None)]
		meta_index = elements.index("METADATA") + 1
		metadata = elements[meta_index]
		text = ""
		if "TEXT" in elements:
			text_index = elements.index("TEXT") + 1
			if text_index < len(elements):
				if elements[text_index] not in ("METADATA", "NOTES"):
					text = elements[text_index]
		notes = ""
		if "NOTES" in elements:
			notes_index = elements.index("NOTES") + 1
			if notes_index < len(elements):
				if elements[notes_index] not in ("METADATA", "TEXT"):
					notes = elements[notes_index]
			
		self.sections: tuple = (metadata, text, notes)
###		print("\u001b[1;31m")
###		print(self.sections[0])
###		print("\u001b[1;32m")
###		print(self.sections[1])
###		print("\u001b[1;33m")
###		print(self.sections[2])
###		print("\u001b[0m")
