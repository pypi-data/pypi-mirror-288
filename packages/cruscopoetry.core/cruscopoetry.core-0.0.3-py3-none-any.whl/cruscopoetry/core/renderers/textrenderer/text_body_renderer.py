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
from ...jsonparser import JsonText, JsonLine
from ..abstractrenderer import TranslationArrangement, AbstractTextBodyRenderer
from .line_renderer import PlainTextLineRenderer
from .disposers import PlainTextNoTranslationDisposer, PlainTextAfterTextDisposer, PlainTextEachStanzaDisposer, PlainTextEachLineDisposer, PlainTextSideBySideDisposer
from typing import Tuple


class TextBodyRenderer(AbstractTextBodyRenderer):

	
	LINE_RENDERER_CLASS = PlainTextLineRenderer

	NO_TRANSLATION_DISPOSER = PlainTextNoTranslationDisposer
	AFTER_TEXT_TRANSLATION_DISPOSER = PlainTextAfterTextDisposer
	EACH_STANZA_TRANSLATION_DISPOSER = PlainTextEachStanzaDisposer
	EACH_LINE_TRANSLATION_DISPOSER = PlainTextEachLineDisposer
	SIDE_BY_SIDE_TRANSLATION_DISPOSER = PlainTextSideBySideDisposer

	
	def __init__(self, body: JsonText):
		super().__init__(body)
		
	@property
	def total_lines(self):
		#for a proper formatting, we also need to know the total number of lines in the poem
		return self.body.count_lines()
		
	def build_disposer(self, line_renderers: Tuple[Tuple[PlainTextLineRenderer]], translation_arrangement: TranslationArrangement):
		return super().build_disposer(line_renderers, translation_arrangement)

	def build_line_renderer(self, line: JsonLine, translation_id: str):
		return super().build_line_renderer(line, translation_id)

	def render(self, translation_id: str, translation_arrangement: int, line_numbers_after: int, indent: str) -> str:
		"""Organizes the metadata in a string as tabular format.
		
		Args:
			translation_id (str): the id of the translation that needs to be included in the rendering (or None, if no translation is desired)
			translation_arrangement (TranslationArrangement): the arrangement of the translation
			line_numbers_after (int): every after line_number_after lines, the line rendering will include the line's number.
			indent (str): the indentation string that shall be use in renderint the plain text.
			
		
		Returns
			view (str): the view of the text as string.
		"""
		if indent == None:
			indent = ''
		
		line_renderers = self._build_line_renderers(translation_id)
		disposer = self.build_disposer(line_renderers, translation_arrangement)
		return disposer.get_rendered_lines(line_numbers_after, indent)
