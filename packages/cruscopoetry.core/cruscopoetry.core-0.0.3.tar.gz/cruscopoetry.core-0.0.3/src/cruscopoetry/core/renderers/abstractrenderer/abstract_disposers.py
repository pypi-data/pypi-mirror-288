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
from typing import Tuple
from .translation_arrangement import TranslationArrangement
from .abstract_line_renderer import AbstractLineRenderer
	
	
class AbstractDisposer(metaclass=abc.ABCMeta):
	"""Abstract class for all disposers. A disposer is an object that takes a tuple of tuples of instances of AbstractLineRenderer concrete implementations and returns a view of them which is built
	according to the translation_arrangement parametre. This class implements the Singleton Pattern.
	Rather than inheriting from this class, it is recommended to inherit directly by the descendant classes AbstractNoTranslationDisposer, AbstractAfterTextDisposer, AbstractEachStanzaDisposer and 
	AbstractEachLineDisposer.
	
	This class is indexable: its associated integer value is the one of the enum member of TranslationArrangement that is stored in self.translation_arrangement.
	
	Args:
		line_renderers (Tuple[Tuple[AbstractLineRenderer, ...]]): a tuple of tuples (each one corresponding to a stanza of the poem) of AbstractLineRenderer instances
		translation_arrangement (TranslationArrangement): the integer representing the translation arrangement, as in :class:`TranslationArrangement`.
	
	Attrs:
		line_renderers (Tuple[Tuple[AbstractLineRenderer, ...]]): a tuple of tuples (each one corresponding to a stanza of the poem) of AbstractLineRenderer instances
		translation_arrangement (TranslationArrangement): the integer representing the translation arrangement, as in :class:`TranslationArrangement`.
	"""

	ARRANGEMENT_INDEX = TranslationArrangement.UNDEFINED
	
	def __init__(self, line_renderers: Tuple[Tuple[AbstractLineRenderer, ...]]):
		self._line_renderers = line_renderers
	
	@property
	def line_renderers(self):
		return self._line_renderers
		
	@property
	def total_lines(self):
		"""Returns the quantity of lines passed to the disposer."""
		
		total_lines = 0
		for stanza in self._line_renderers:
			total_lines += len(stanza)
		return total_lines
		
	@abc.abstractmethod
	def get_rendered_lines(self, line_numbers_after: int):
		"""Returns the rendered lines.
		
		Args:
			numbers_after (int): says after how many lines the line number must be included in the rendering. If it is None, line numbers will be added to no line. If it is None, no line number 
				will be included.
		"""
		pass
		
	def iter_stanzas(self):
		for stanza in self._line_renderers:
			yield stanza
	
	def iter_line_renderers(self):
		for stanza in self._line_renderers:
			yield from stanza


class AbstractNoTranslationDisposer(AbstractDisposer):

	ARRANGEMENT_INDEX = TranslationArrangement.NO_TRANSLATION

	def __init__(self, line_renderers: Tuple[Tuple[AbstractLineRenderer, ...]]):
		super().__init__(line_renderers)


class AbstractAfterTextDisposer(AbstractDisposer):

	ARRANGEMENT_INDEX = TranslationArrangement.AFTER_TEXT

	def __init__(self, line_renderers: Tuple[Tuple[AbstractLineRenderer, ...]]):
		super().__init__(line_renderers)


class AbstractEachStanzaDisposer(AbstractDisposer):

	ARRANGEMENT_INDEX = TranslationArrangement.EACH_STANZA

	def __init__(self, line_renderers: Tuple[Tuple[AbstractLineRenderer, ...]]):
		super().__init__(line_renderers)


class AbstractEachLineDisposer(AbstractDisposer):

	ARRANGEMENT_INDEX = TranslationArrangement.EACH_LINE

	def __init__(self, line_renderers: Tuple[Tuple[AbstractLineRenderer, ...]]):
		super().__init__(line_renderers)

class AbstractSideBySideDisposer(AbstractDisposer):

	ARRANGEMENT_INDEX = TranslationArrangement.SIDE_BY_SIDE
	
	def __init__(self, line_renderers: Tuple[Tuple[AbstractLineRenderer, ...]]):
		super().__init__(line_renderers)
