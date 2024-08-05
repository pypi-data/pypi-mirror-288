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
from ..abstractrenderer import AbstractNoTranslationDisposer, AbstractAfterTextDisposer, AbstractEachStanzaDisposer, AbstractEachLineDisposer, AbstractSideBySideDisposer
from .utils import *
from typing import Tuple
from .line_renderer import HtmlLineRenderer
from mum import Singleton


class HtmlDisposer(metaclass=Singleton):

	def build_blank_cell(self):
		return HtmlNode("td", {"class": "blank_cell"}, "")

	def build_blank_row(self):
		blank_cell = self.build_blank_cell()
		blank_cell.attribs["colspan"] = "100%"
		return HtmlNode("tr", {"class": "blank_row"}, blank_cell)
	
	def build_text_table(self):
		return HtmlNode("table", {"id": "text_body"})

	def get_number_cell(self, number: int, line_numbers_after: int) -> HtmlNode:

		if line_numbers_after == None:
			return HtmlNode("td", {"class": "number"}, "")

		if number % line_numbers_after == 0:
			return HtmlNode("td", {"class": "number"}, str(number))
		else:
			return HtmlNode("td", {"class": "number"}, "")

	def get_line_source(self, line: HtmlLineRenderer, line_numbers_after: int) -> HtmlNode:
		"""Returns a line's source text in html format.
		
		Args:
			line (HtmlLineRenderer): the line whose source is needed
			line_numbers_after (int): if line.number % line_numbers_after == 0, then also the line number will be inserted in the rendering.
		
		Returns:
			line_row: tr-tagged HtmlNode containing the line's source text and eventually the number.
		"""
		number_cell = self.get_number_cell(line.number, line_numbers_after)
		line_cell = line.get_source()

		line_row = HtmlNode("tr", {"id": "line_%d"%line.number,  "class": "line"}, [number_cell, line_cell])
		return line_row

	def get_stanza_source(self, stanza: Tuple[HtmlLineRenderer, ...], line_numbers_after: int) -> Tuple[HtmlNode]:
		"""Returns the renderings of the source texts of the lines composing the stanza as a tuple of tr-tagged HtmlNode instances"""

		stanza_rendering = tuple(self.get_line_source(line, line_numbers_after) for line in stanza)
		return stanza_rendering

	def get_text_source(self, line_renderers: Tuple[Tuple[HtmlLineRenderer, ...]], line_numbers_after) -> Tuple[HtmlNode]:
		"""Returns the renderings of the source texts of the lines composing the text as a tuple of tr-tagged HtmlNode instances"""

		stanza_renderings = tuple(self.get_stanza_source(stanza, line_numbers_after) for stanza in line_renderers)
		text_rendering = []
		for i, stanza in enumerate(stanza_renderings):
			if i > 0:
				text_rendering.append(self.build_blank_row())
			text_rendering.extend(stanza)
		return text_rendering

	def get_line_translation(self, line: HtmlLineRenderer, line_numbers_after: int) -> HtmlNode:
		"""Returns a line's translation text in html format.
		
		Args:
			line (HtmlLineRenderer): the line whose translation is needed
			line_numbers_after (int): if line.number % line_numbers_after == 0, then also the line number will be inserted in the rendering.
		
		Returns:
			line_row: tr-tagged HtmlNode containing the line's translation text and eventually the number.
		"""
		number_cell = self.get_number_cell(line.number, line_numbers_after)
		line_cell = line.get_translation()

		line_row = HtmlNode("tr", {"id": "line_%d_tr"%line.number, "class": "line"}, [number_cell, line_cell])
		return line_row

	def get_stanza_translation(self, stanza: Tuple[HtmlLineRenderer, ...], line_numbers_after: int) -> Tuple[HtmlNode]:
		"""Returns the renderings of the translations of the lines composing the stanza as a tuple of tr-tagged HtmlNode instances"""

		stanza_rendering = tuple(self.get_line_translation(line, line_numbers_after) for line in stanza)
		return stanza_rendering

	def get_text_translation(self, line_renderers: Tuple[Tuple[HtmlLineRenderer, ...]], line_numbers_after) -> Tuple[HtmlNode]:
		"""Returns the renderings of the translations of the lines composing the text as a tuple of tr-tagged HtmlNode instances"""

		stanza_renderings = tuple(self.get_stanza_translation(stanza, line_numbers_after) for stanza in line_renderers)
		text_rendering = []
		for i, stanza in enumerate(stanza_renderings):
			if i > 0:
				text_rendering.append(self.build_blank_row())
			text_rendering.extend(stanza)
		return text_rendering
		
	def get_line_source_and_translation(self, line: HtmlLineRenderer, line_numbers_after: int) -> HtmlNode:
		"""Returns a tr-tagged HtmlNode which contains both the source text and the translation"""

		number_cell = self.get_number_cell(line.number, line_numbers_after)
		line_source_cell = line.get_source()
		line_translation_cell = line.get_translation()
		line_row = HtmlNode("tr", {"id": "line_%d"%line.number,  "class": "line"}, [number_cell, line_source_cell, line_translation_cell])
		return line_row

	def get_stanza_source_and_translation(self, stanza: Tuple[HtmlLineRenderer], line_numbers_after: int) -> HtmlNode:
		"""Returns the renderings of the source and translation of each line composing a stanza as a tuple of tr-tagged HtmlNode instances"""
		stanza_rendering = tuple(self.get_line_source_and_translation(line, line_numbers_after) for line in stanza)
		return stanza_rendering
	
	def get_text_source_and_translation(self, line_renderers: Tuple[Tuple[HtmlLineRenderer, ...]], line_numbers_after: int) -> Tuple[HtmlNode]:
		"""Returns the renderings of the source and translation of each line composing the text as a tuple of tr-tagged HtmlNode instances"""

		stanza_renderings = tuple(self.get_stanza_source_and_translation(stanza, line_numbers_after) for stanza in line_renderers)
		text_rendering = []
		for i, stanza in enumerate(stanza_renderings):
			if i > 0:
				text_rendering.append(self.build_blank_row())
			text_rendering.extend(stanza)
		return text_rendering


class HtmlNoTranslationDisposer(AbstractNoTranslationDisposer):

	UTILITIES = HtmlDisposer()
	
	@property
	def utilities(self):
		return self.__class__.UTILITIES

	def __init__(self, line_renderers: Tuple[Tuple[HtmlLineRenderer, ...]]):
		super().__init__(line_renderers)

	def get_rendered_lines(self, line_numbers_after: int):
		source_text = self.utilities.get_text_source(self.line_renderers, line_numbers_after)
		text_table = self.utilities.build_text_table()
		text_table.extend(source_text)		
		return text_table


class HtmlAfterTextDisposer(AbstractAfterTextDisposer):

	UTILITIES = HtmlDisposer()
	
	@property
	def utilities(self):
		return self.__class__.UTILITIES

	def __init__(self, line_renderers: Tuple[Tuple[HtmlLineRenderer, ...]]):
		super().__init__(line_renderers)

	def get_rendered_lines(self, line_numbers_after: int):
		source_text = self.utilities.get_text_source(self.line_renderers, line_numbers_after)
		translation_text = self.utilities.get_text_translation(self.line_renderers, line_numbers_after)

		text_table = self.utilities.build_text_table()
		text_table.extend(source_text)
		text_table.append(self.utilities.build_blank_row())
		text_table.append(self.utilities.build_blank_row())
		text_table.extend(translation_text)
		return text_table


class HtmlEachStanzaDisposer(AbstractEachStanzaDisposer):

	UTILITIES = HtmlDisposer()
	
	@property
	def utilities(self):
		return self.__class__.UTILITIES

	def __init__(self, line_renderers: Tuple[Tuple[HtmlLineRenderer, ...]]):
		super().__init__(line_renderers)

	def get_rendered_stanza(self, stanza: Tuple[HtmlLineRenderer, ...], line_numbers_after: int):
		source_stanza = self.utilities.get_stanza_source(stanza, line_numbers_after)
		translation_stanza = self.utilities.get_stanza_translation(stanza, line_numbers_after)
		
		stanza_rendering = []
		stanza_rendering.extend(source_stanza)
		stanza_rendering.append(self.utilities.build_blank_row())
		stanza_rendering.extend(translation_stanza)
		return stanza_rendering

	def get_rendered_lines(self, line_numbers_after: int):
		stanza_renderings = tuple(self.get_rendered_stanza(stanza, line_numbers_after) for stanza in self.line_renderers)
		text_table = self.utilities.build_text_table()
		
		for i, stanza in enumerate(stanza_renderings):
			if i > 0:
				for j in range(2):
					text_table.append(self.utilities.build_blank_row())
			text_table.extend(stanza)
		
		return text_table
		

class HtmlEachLineDisposer(AbstractEachLineDisposer):

	UTILITIES = HtmlDisposer()
	
	@property
	def utilities(self):
		return self.__class__.UTILITIES

	def __init__(self, line_renderers: Tuple[Tuple[HtmlLineRenderer, ...]]):
		super().__init__(line_renderers)

	def get_rendered_line(self, line: HtmlLineRenderer, line_numbers_after: int):
		source_line = self.utilities.get_line_source(line, line_numbers_after)
		#since the translation is immediately after the source text, there is no need to include the line number even at its row, so we pass None as number_after argument:
		translation_line = self.utilities.get_line_translation(line, None)
		
		line_rendering = []
		line_rendering.append(source_line)
		line_rendering.append(self.utilities.build_blank_row())
		line_rendering.append(translation_line)
		return tuple(line_rendering)

	def get_rendered_stanza(self, stanza: Tuple[HtmlLineRenderer, ...], line_numbers_after: int):
		line_renderings = tuple(self.get_rendered_line(line, line_numbers_after) for line in stanza)
		stanza_rendering = []
		for i, line in enumerate(line_renderings):
			if i > 0:
				for j in range(2):
					stanza_rendering.append(self.utilities.build_blank_row())
			stanza_rendering.extend(line)
		return stanza_rendering

	def get_rendered_lines(self, line_numbers_after: int):
		stanza_renderings = tuple(self.get_rendered_stanza(stanza, line_numbers_after) for stanza in self.line_renderers)
		text_table = self.utilities.build_text_table()
		
		for i, stanza in enumerate(stanza_renderings):
			if i > 0:
				for j in range(3):
					text_table.append(self.utilities.build_blank_row())
			text_table.extend(stanza)
		
		return text_table
		

class HtmlSideBySideDisposer(AbstractSideBySideDisposer):
	
	UTILITIES = HtmlDisposer()
	
	@property
	def utilities(self):
		return self.__class__.UTILITIES

	def __init__(self, line_renderers: Tuple[Tuple[HtmlLineRenderer, ...]]):
		super().__init__(line_renderers)
	
	def get_rendered_lines(self, line_numbers_after: int):
		lines_renderings = self.utilities.get_text_source_and_translation(self.line_renderers, line_numbers_after)
		text_table = self.utilities.build_text_table()
		text_table.extend(lines_renderings)
		return text_table		

