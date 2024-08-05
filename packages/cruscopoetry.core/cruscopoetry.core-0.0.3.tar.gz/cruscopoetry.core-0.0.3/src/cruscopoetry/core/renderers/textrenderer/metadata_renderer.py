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
from ...jsonparser import JsonMetadata, JsonTranslations, JsonTranslation
from ..abstractrenderer import AbstractMetadataRenderer


class MetadataRenderer(AbstractMetadataRenderer):
	
	def __init__(self, metadata: JsonMetadata, translations: JsonTranslations):
		super().__init__(metadata, translations)
		
	def _render_source_metadata(self, indent):
		ret_str = indent + "mandatory fields:" + os.linesep
		ret_str += os.linesep.join("%s%s\t%s"%(indent*2, key, value) for key, value in self.metadata.mandatory_items())
		
		optional_items = self.metadata.optional_items()
		if len(optional_items) > 0:
			ret_str += indent + "additional fields:" + os.linesep
			ret_str += os.linesep.join("%s%s\t%s"%(indent*2, key, value) for key, value in optional_items)
		
		return ret_str
		
	def _render_translation_metadata(self, translation_id: str, indent):
		"""Returns the metadata of translation having id `translation_id`. If translation_id is None or no translation has been found, returns an empty string."""
		if indent == None:
			indent = "  "
		ret_str = ""
		
		if translation_id != None:
			translation = self.translations.get_translation_by_id(translation_id)
		else:
			translation = None

		if translation != None:
			ret_str = indent + "mandatory fields:" + os.linesep
			ret_str += os.linesep.join("%s%s\t%s"%(indent*2, key, value) for key, value in translation.mandatory_items)
			optional_items = translation.metadata
			if len(optional_items) > 0:
				ret_str += indent + "additional fields:" + os.linesep
				ret_str += os.linesep.join("%s%s\t%s"%(indent*2, key, value) for key, value in optional_items.items())
			
		
		return ret_str

	def render(self, translation_id: str, indent: str = None) -> str:
		"""Organizes the metadata in a string as tabular format.
		
		Returns
			view (str): the view of the text as string.
		"""
		if indent == None:
			indent = '  '
		ret_str = "SOURCE METADATA" + os.linesep
		ret_str += self._render_source_metadata(indent)
		translation = self._render_translation_metadata(translation_id, indent)
		if translation != '':
			ret_str += os.linesep + "TRANSLATION METADATA" + os.linesep
			ret_str += translation
		return ret_str
