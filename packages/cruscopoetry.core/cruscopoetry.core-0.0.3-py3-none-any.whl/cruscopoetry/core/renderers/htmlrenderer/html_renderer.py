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
from ...jsonparser import JsonParser
from .metadata_renderer import HtmlMetadataRenderer
from .notes_renderer import HtmlNotesRenderer
from .text_body_renderer import HtmlTextBodyRenderer
from ..abstractrenderer import AbstractRenderer, TranslationArrangement
import os
from .utils import *


class HtmlRenderer(AbstractRenderer):
	"""This class is a concrete implementation of :class:`cruscopoetry.renderers.AbstractRenderer` for plain text.
	
	Args:
		path (str): the path of the JSON file that must be rendered.
	"""
	METADATA_RENDERER = HtmlMetadataRenderer
	TEXT_BODY_RENDERER = HtmlTextBodyRenderer
	NOTES_RENDERER = HtmlNotesRenderer
	
	def __init__(self, poem: str):
		super().__init__(poem)

	def build_metadata_renderer(self, json: JsonParser):
		return super().build_metadata_renderer(json)

	def build_text_body_renderer(self, json: JsonParser):
		return super().build_text_body_renderer(json)

	def build_notes_renderer(self, json: JsonParser):
		return super().build_notes_renderer(json)

	def render(self, translation_id: str, translation_arrangement: TranslationArrangement, number_after: int, pretty_print: bool) -> str:
		"""Builds the view and returns it as a string (this function doesn't save it on a file.
		
		Args:
			translation_id (str): the id of the translation to insert into the view, or None if no translation is desired.
			translation_arrangement (int): an integer between AbstractViewer.NO_TRANSLATION , AbstractViewer.AFTER_TEXT , AbstractViewer.STANZA_BY_STANZA and AbstractViewer.LINE_BY_LINE.
		
		Returns
			view (str): the view of the text as string.
		"""
		
		charset_node = HtmlNode("meta", {"charset": "utf-8"})
		
		translation_id, translation_arrangement = self.adjust_translation_data(translation_id, translation_arrangement)
		metadata_rendering = self.metadata.render(translation_id)
		body_rendering = self.body.render(translation_id, translation_arrangement, number_after)
		notes_rendering = self.notes.render(translation_id)

		document = HtmlDocument.create_empty()
		document.head.append(charset_node)
		document.body.append(metadata_rendering)
		document.body.append(body_rendering)
		document.body.append(notes_rendering)
		if pretty_print:
			return document.pretty_print()
		else:
			return str(document)
