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
from .utils import *


class HtmlMetadataRenderer(AbstractMetadataRenderer):
	
	def __init__(self, metadata: JsonMetadata, translations: JsonTranslations):
		super().__init__(metadata, translations)

	def _render_field(self, key: str, value, is_mandatory: bool) -> HtmlNode:
		field_class = "mandatory_metadata" if is_mandatory else "additional_metadata"
		field_id = '_'.join(key.split(' ')) + "_field"
		row = HtmlNode("tr", {"id": field_id, "class": field_class})
		row.append(HtmlNode("td", {"class": "key"}, key))
		row.append(HtmlNode("td", {"class": "value"}, str(value)))
		return row

	def _render_source_metadata(self) -> HtmlNode:
		table_node = HtmlNode("table", {"id": "source_metadata", "class": "metadata_table"})
		for key, value in self.metadata.mandatory_items():
			row = self._render_field(key, value, True)
			table_node.append(row)
		for key, value in self.metadata.optional_items():
			row = self._render_field(key, value, False)
			table_node.append(row)
		
		return table_node
		
	def _render_translation_metadata(self, translation_id: str) -> HtmlNode:
		translation = self.translations.get_translation_by_id(translation_id)
		if translation != None:
			table_node = HtmlNode("table", {"id": "translation_metadata", "class": "metadata_table"})
			for key, value in translation.mandatory_items:
				row = HtmlNode("tr", {"id": key+"_field", "class": "mandatory_metadata"})
				row.append(HtmlNode("td", {"class": "key"}, [key,]))
				row.append(HtmlNode("td", {"class": "value"}, [value,]))
				table_node.append(row)
			for key, value in translation.metadata.items():
				row = HtmlNode("tr", {"id": "additional_field", "class": "additional_metadata"})
				row.append(HtmlNode("td", {"class": "key"}, [key,]))
				row.append(HtmlNode("td", {"class": "value"}, [value,]))
				table_node.append(row)
			
			return table_node
		else:
			return NullNode()
	
	def _render_added_rows(self) -> HtmlNode:
		table_node = HtmlNode("table", {"id": "added_rows", "class": "metadata_table"})
		for key, value in self._added_rows.items():
			row = self._render_field(key, value, False)
			table_node.append(row)
		return table_node

	def render(self, translation_id: str) -> str:
		"""Organizes the metadata in a string as tabular format.
		
		Returns
			view (str): the view of the text as string.
		"""
		metadata_node = HtmlNode("div", {"id": "metadata_section"})
		metadata_node.append(HtmlNode("h1", {}, ["Metadata",]))
		metadata_node.append(HtmlNode("h2", {}, ["from source text:",]))
		metadata_node.append(self._render_source_metadata())
		translation_metadata = self._render_translation_metadata(translation_id) if translation_id != None else NullNode()
		if translation_metadata.is_not_null:
			metadata_node.append(HtmlNode("h2", {}, ["from translation:",]))
			metadata_node.append(translation_metadata)
		if len(self._added_rows) > 0:
			metadata_node.append(HtmlNode("h2", {}, ["other data:",]))
			metadata_node.append(self._render_added_rows())
		return metadata_node
