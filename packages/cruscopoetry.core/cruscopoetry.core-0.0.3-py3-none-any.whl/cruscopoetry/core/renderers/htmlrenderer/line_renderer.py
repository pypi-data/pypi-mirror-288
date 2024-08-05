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
from ...jsonparser import JsonLine, JsonColon
from ..abstractrenderer import AbstractLineRenderer
from .utils import *
	

class HtmlColonRenderer:

	def __init__(self, jcolon: JsonColon):
		self._jcolon = jcolon
	
	@property
	def jcolon(self):
		return self._jcolon

	def render(self) -> str:
		node = TextNode(self.jcolon.transcription)
		return node
	
	@property
	def transcription(self) -> str:
		return self._jcolon.transcription


class HtmlLineRenderer(AbstractLineRenderer):

	COLON_RENDERER = HtmlColonRenderer

	def __init__(self, jline: JsonLine, translation_id: str):
		super().__init__(jline, translation_id)
		self.cola = tuple(self.build_colon_renderer(colon) for colon in jline.iter_cola())
	
	def build_colon_renderer(self, jcolon: JsonColon):
		return self.__class__.COLON_RENDERER(jcolon)
		
	@property
	def blank_colon(self):
		return HtmlNode("td", {}, "")
	
	@property
	def colon_separator(self):
		return TextNode(" · ")

	def get_source(self) -> str:

		cola = [colon.render() for colon in self.cola]
		cola = self.colon_separator.join(cola)
		cell = HtmlNode("td", {"class": "source"}, cola)
		return cell

	def get_translation(self) -> str:
		translation = self.translation if self.translation != None else ''
		cell = HtmlNode("td", {"class": "translation"}, translation)
		return cell
