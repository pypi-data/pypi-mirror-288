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
from ...jsonparser import JsonText, JsonTranslations, JsonTranslation, JsonStanza, JsonLine, JsonColon
from ..abstractrenderer import AbstractTextBodyRenderer, TranslationArrangement
from .disposers import HtmlNoTranslationDisposer, HtmlAfterTextDisposer, HtmlEachStanzaDisposer, HtmlEachLineDisposer, HtmlSideBySideDisposer
from .line_renderer import HtmlLineRenderer
from .utils import *
from typing import Tuple
		

class HtmlTextBodyRenderer(AbstractTextBodyRenderer):

	LINE_RENDERER_CLASS = HtmlLineRenderer

	NO_TRANSLATION_DISPOSER = HtmlNoTranslationDisposer
	AFTER_TEXT_TRANSLATION_DISPOSER = HtmlAfterTextDisposer
	EACH_STANZA_TRANSLATION_DISPOSER = HtmlEachStanzaDisposer
	EACH_LINE_TRANSLATION_DISPOSER = HtmlEachLineDisposer
	SIDE_BY_SIDE_TRANSLATION_DISPOSER = HtmlSideBySideDisposer
	
	def __init__(self, body: JsonText):
		super().__init__(body)

	def build_line_renderer(self, line: JsonLine, translation_id: str):
		return super().build_line_renderer(line, translation_id)

	def build_disposer(self, line_renderers : Tuple[Tuple[HtmlLineRenderer]], translation_arrangement: TranslationArrangement):
		return super().build_disposer(line_renderers, translation_arrangement)

	def render(self, translation_id: str, translation_arrangement: TranslationArrangement, line_numbers_after: int) -> str:
		body_title = HtmlNode("h1", {"id": "text_body_title"}, "Text")
		text_table = super().render(translation_id, translation_arrangement, line_numbers_after)
		body_wrapper = HtmlNode("div", {"id": "text_body_wrapper"}, [body_title, text_table])
		return body_wrapper
