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
import abc
from ...jsonparser import JsonMetadata, JsonTranslations


class AbstractMetadataRenderer(metaclass=abc.ABCMeta):
	"""Abstract class for the rendering of the metadata of a CruscoPoetry JSON file.
	
	Args:
		json_metadata (JsonMetadata): the object representing the metadata of the json parsing of the poem
		json_translations (JsonTranslations): the object representing the translations of the json parsing of the poem
	
	Attrs:
		metadata (JsonMetadata): the object representing the metadata of the json parsing of the poem
		translations (JsonTranslations): the object representing the translations of the json parsing of the poem
	"""

	def __init__(self, json_metadata: JsonMetadata, json_translations: JsonTranslations):
		self._metadata = json_metadata
		self._translations = json_translations
		self._added_rows = {}
	
	def add_row(self, key: str, value: str):
		"""Allows to render as metadatum a key-value pair which is not stored among the text metadata (but, for example, derives from a plugin). If this function has already been used with the same 
		key argument, the corresponding value will be updated

	Args:
		key (str): self-explanatory
		value (str): self-explanatory
		"""
		self._added_rows[key] = value
	
	@property
	def metadata(self):
		return self._metadata
	
	@property
	def translations(self):
		return self._translations
	
	@abc.abstractmethod
	def render(self) -> str:
		"""Provides the renderings of the metadata."""
		return ''
