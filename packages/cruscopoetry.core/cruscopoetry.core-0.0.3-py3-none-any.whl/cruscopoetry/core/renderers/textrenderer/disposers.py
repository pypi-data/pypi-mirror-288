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
from .joiners import Joiners
from .line_renderer import PlainTextLineRenderer
from typing import Tuple
from .joiners import Joiners


class PlainTextDisposer:
	"""Provides utility methods for all the plain text disposer classes."""

	def _get_number_column_length(self, total_lines: int) -> int:
		"""Returns the number of digits of total_lines in base ten, plus two. In the rendering of the line, a space of this length will contain the line number if required, else blank spaces"""	
		ret_int = 0
		while total_lines > 0:
			total_lines //= 10
			ret_int += 1
		return ret_int + 2

	def _build_left_string(self, line_number: int, line_numbers_after: int, number_column_length: int):
		
		if line_numbers_after == None:
			return " "*number_column_length
		
		include_number = (line_number % line_numbers_after) == 0
		if include_number:
			left_string = "%" + str(number_column_length-1) + "d "
			left_string = left_string%line_number
		else:
			left_string = " "*number_column_length
		return left_string

	def render_line_source(self, line_renderer: PlainTextLineRenderer, number_column_length: int, line_numbers_after, indent: str) -> str:
		"""Gets the line's source and adds the line number if required."""
		
		left_string = self._build_left_string(line_renderer.number, line_numbers_after, number_column_length)
		source = line_renderer.get_source()
		
		return indent + left_string + source

	def render_line_translation(self, line_renderer: PlainTextLineRenderer, number_column_length: int, line_numbers_after, indent: str) -> str:
		"""Gets the line's source and adds the line number if required."""
		
		left_string = self._build_left_string(line_renderer.number, line_numbers_after, number_column_length)
		source = line_renderer.get_translation()
		
		return indent + left_string + source

	def render_stanza_source(self, stanza: Tuple[PlainTextLineRenderer], number_column_length: int, line_numbers_after: int, indent: str) -> str:
		"""Gets the renderings of the lines and groups them in a multiline string."""
		line_renderings = tuple(self.render_line_source(line_renderer, number_column_length, line_numbers_after, indent) for line_renderer in stanza)
		ret_str = Joiners.LINE.join(line_renderings)
		return ret_str		

	def render_stanza_translation(self, stanza: Tuple[PlainTextLineRenderer], number_column_length: int, line_numbers_after: int, indent: str) -> str:
		"""Gets the renderings of the lines and groups them in a multiline string."""
		line_renderings = tuple(self.render_line_translation(line_renderer, number_column_length, line_numbers_after, indent) for line_renderer in stanza)
		ret_str = Joiners.LINE.join(line_renderings)
		return ret_str		

	def render_text_source(self, line_renderers: Tuple[Tuple[PlainTextLineRenderer, ...]], number_column_length: int, line_numbers_after: int, indent: str) -> str:
		stanzas = tuple(self.render_stanza_source(stanza, number_column_length, line_numbers_after, indent) for stanza in line_renderers)
	
		ret_str = Joiners.STANZA.join(stanzas)
		return ret_str

	def render_text_translation(self, line_renderers: Tuple[Tuple[PlainTextLineRenderer, ...]], number_column_length: int, line_numbers_after: int, indent: str) -> str:
		stanzas = tuple(self.render_stanza_translation(stanza, number_column_length, line_numbers_after, indent) for stanza in line_renderers)
	
		ret_str = Joiners.STANZA.join(stanzas)
		return ret_str


class PlainTextNoTranslationDisposer(AbstractNoTranslationDisposer):

	def __init__(self, line_renderers: Tuple[Tuple[PlainTextLineRenderer, ...]]):
		super().__init__(line_renderers)
		self.utilities = PlainTextDisposer()
		self.number_column_length = self.utilities._get_number_column_length(self.total_lines)

	def render_stanza(self, stanza: Tuple[PlainTextLineRenderer], number_column_length: int, line_numbers_after: int, indent: str) -> str:
		"""Gets the renderings of the lines and groups them in a multiline string."""
		return self.utilities.render_stanza_source(stanza, number_column_length, line_numbers_after, indent)		
		
	def get_rendered_lines(self, line_numbers_after: int, indent: str) -> str:
		
		ret_str = Joiners.STANZA.join(self.render_stanza(stanza, self.number_column_length, line_numbers_after, indent) for stanza in self.iter_stanzas())
		return ret_str


class PlainTextAfterTextDisposer(AbstractNoTranslationDisposer):

	def __init__(self, line_renderers: Tuple[Tuple[PlainTextLineRenderer, ...]]):
		super().__init__(line_renderers)
		self.utilities = PlainTextDisposer()
		self.number_column_length = self.utilities._get_number_column_length(self.total_lines)
		
	def get_rendered_lines(self, line_numbers_after: int, indent: str):

		source = self.utilities.render_text_source(self.line_renderers, self.number_column_length, line_numbers_after, indent)
		translation = self.utilities.render_text_translation(self.line_renderers, self.number_column_length, line_numbers_after, indent)

		ret_str = source + Joiners.SOURCE_AND_TRANSLATION*3 + translation
		return ret_str
		

class PlainTextEachStanzaDisposer(AbstractNoTranslationDisposer):

	def __init__(self, line_renderers: Tuple[Tuple[PlainTextLineRenderer, ...]]):
		super().__init__(line_renderers)
		self.utilities = PlainTextDisposer()
		self.number_column_length = self.utilities._get_number_column_length(self.total_lines)

	def get_rendered_stanza(self, stanza: Tuple[PlainTextLineRenderer, ...], line_numbers_after: int, indent: str):

		source = self.utilities.render_stanza_source(stanza, self.number_column_length, line_numbers_after, indent)
		translation = self.utilities.render_stanza_translation(stanza, self.number_column_length, line_numbers_after, indent)
		
		return source + Joiners.SOURCE_AND_TRANSLATION*2 + translation
				
	def get_rendered_lines(self, line_numbers_after: int, indent: str):

		stanza_renderings = tuple(self.get_rendered_stanza(stanza, line_numbers_after, indent) for stanza in self.line_renderers)
		ret_str = (Joiners.LINE*3).join(stanza_renderings)
		return ret_str


class PlainTextEachLineDisposer(AbstractNoTranslationDisposer):

	def __init__(self, line_renderers: Tuple[Tuple[PlainTextLineRenderer, ...]]):
		super().__init__(line_renderers)
		self.utilities = PlainTextDisposer()
		self.number_column_length = self.utilities._get_number_column_length(self.total_lines)
		
	def get_rendered_line(self, line: PlainTextLineRenderer, line_number_after: int, indent: str):
		source = self.utilities.render_line_source(line, self.number_column_length, line_number_after, indent)
		#since the translation is immediately after the source text, there is no need to include the line number even at its row, so we pass None as number_after argument:
		translation = self.utilities.render_line_translation(line, self.number_column_length, None, indent)
		ret_str = source + Joiners.LINE + translation
		return ret_str
		
	def get_rendered_lines(self, line_number_after: int, indent: str):
		renderer_lines = tuple(self.get_rendered_line(line, line_number_after, indent) for line in self.iter_line_renderers())
		ret_str = Joiners.STANZA.join(renderer_lines)
		return ret_str


class PlainTextSideBySideDisposer(AbstractSideBySideDisposer):

	def __init__(self, line_renderers: Tuple[Tuple[PlainTextLineRenderer, ...]]):
		super().__init__(line_renderers)
		self.utilities = PlainTextDisposer()
		self.number_column_length = self.utilities._get_number_column_length(self.total_lines)
		
	def render_line(self, line: PlainTextLineRenderer, line_numbers_after: int, indent: str) -> str:
		source = self.utilities.render_line_source(line, self.number_column_length, line_numbers_after, indent)
		#since the translation is immediately after the source text, there is no need to include the line number even at its row, so we pass None as number_after argument:
		translation = line.get_translation()
		return source + "\t" + translation
		

	def render_stanza(self, stanza: Tuple[PlainTextLineRenderer], line_numbers_after: int, indent: str) -> str:
		"""Gets the renderings of the lines and groups them in a multiline string."""
		lines = tuple(self.render_line(line, line_numbers_after, indent) for line in stanza)
		return Joiners.LINE.join(lines)
		
	def get_rendered_lines(self, line_numbers_after: int, indent: str) -> str:
		
		ret_str = Joiners.STANZA.join(self.render_stanza(stanza, line_numbers_after, indent) for stanza in self.iter_stanzas())
		return ret_str

