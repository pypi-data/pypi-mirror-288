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
from .metadata_renderer import MetadataRenderer
from .notes_renderer import NotesRenderer
from .text_body_renderer import TextBodyRenderer
from ..abstractrenderer import AbstractRenderer, TranslationArrangement
from ...jsonparser import JsonParser
from .joiners import Joiners


class TextRenderer(AbstractRenderer):
	"""This class is a concrete implementation of :class:`cruscopoetry.renderers.AbstractRenderer` for plain text.
	
	Args:
		path (str): the path of the JSON file that must be rendered.
	"""
	
	METADATA_RENDERER = MetadataRenderer
	TEXT_BODY_RENDERER = TextBodyRenderer
	NOTES_RENDERER = NotesRenderer
	
	def __init__(self, poem: str):
		super().__init__(poem)
		
	def build_metadata_renderer(self, json: JsonParser):
		return super().build_metadata_renderer(json)
		
	def build_text_body_renderer(self, json: JsonParser):
		return super().build_text_body_renderer(json)
		
	def build_notes_renderer(self, json: JsonParser):
		return super().build_notes_renderer(json)

	def render(self, translation_id: str = None, translation_arrangement: int = None, indent: str = None, number_after: int = None) -> str:
		"""Builds the view and returns it as a string (this function doesn't save it on a file.
		
		Args:
			translation_id (str): the id of the translation to insert into the view, or None if no translation is desired.
			translation_arrangement (int): an integer between AbstractViewer.NO_TRANSLATION , AbstractViewer.AFTER_TEXT , AbstractViewer.STANZA_BY_STANZA and AbstractViewer.LINE_BY_LINE.
		
		Returns
			view (str): the view of the text as string.
		"""
		translation_id, translation_arrangement = self.adjust_translation_data(translation_id, translation_arrangement)
		if translation_arrangement == None:
			if translation_id == None:
				translation_arrangement = TranslationArrangement.NO_TRANSLATION
			else:
				translation_arrangement = TranslationArrangement.AFTER_TEXT
		ret_str = ''
		ret_str += self.metadata.render(translation_id, indent)
		ret_str += Joiners.SECTION_TITLE + "TEXT" + Joiners.SECTION_TITLE
		ret_str += self.body.render(translation_id, translation_arrangement, number_after, indent)
		ret_str += Joiners.SECTION_TITLE + "NOTES" + Joiners.SECTION_TITLE
		#regarding notes, we will render only their source text if translation_arrangement != NO_TRANSLATION, else only their translated text.

		if ((translation_id == None) or (translation_arrangement == TranslationArrangement.NO_TRANSLATION)):
			ret_str += self.notes.render(None, indent)
		else:
			ret_str += self.notes.render(translation_id, indent)
		return ret_str
		
