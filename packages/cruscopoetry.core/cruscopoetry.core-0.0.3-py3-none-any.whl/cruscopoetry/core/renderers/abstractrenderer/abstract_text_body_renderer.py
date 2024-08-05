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
from ...jsonparser import JsonText, JsonStanza, JsonLine
from ..exceptions import MissingTranslationError
from typing import Tuple
from .translation_arrangement import TranslationArrangement
from .abstract_disposers import AbstractNoTranslationDisposer, AbstractAfterTextDisposer, AbstractEachStanzaDisposer, AbstractEachLineDisposer, AbstractSideBySideDisposer
from .abstract_line_renderer import AbstractLineRenderer
from .exceptions import DisposerException


class AbstractTextBodyRenderer(metaclass=abc.ABCMeta):
	"""This class provides an interface for all the viewers. A viewer's role is that of parsing the JSON file and organizing its material in a human-readable way (es. a HTML page, or pure text).
	Viewers must be able to render the text either with no or with one translation, and in this last case to organize the translation after the whole text, stanza by stanza or line by line.
	
	Args:
		path (str): the path of the JSON file that must be rendered.
	
	Attrs:
		path (str): the path of the JSON file that must be rendered.
		json (JsonParser): the instance of JsonParser that represents the poem.

	Concrete implementations of this class need to override three methods:
	 - build_line_renderer
	 - build_disposer
	 - render
		
	An easy way to build concrete implementations of this class is to override the two class attributes LINE_RENDERER_CLASS with the concrete implementation of	AbstractLineRenderer that need to be 
	employed. If the concrete implementation of AbstractLineRenderer takes the same initialization arguments of AbstractLineRenderer, the override of build_line_renderer can be done just by calling 
	the super method; otherwise, it must be rewritten.
	The same can be said for the class attributes NO_TRANSLATION_DISPOSER, AFTER_TEXT_TRANSLATION_DISPOSER, EACH_STANZA_TRANSLATION_DISPOSER and EACH_LINE_TRANSLATION_DISPOSER.
	If their concrete implementations do nothave different initialization arguments than those of their abstract ancestors, the abstract method build_disposer can be overridden simply calling 
	its super() implementation. If instead it needs to be rewritten, one can use the method _get_disposer to get the disposer correspondent to the translation arrangement passed as parametre, and 
	then handle initialization. 
	If the render method is overridden by just calling its super() implementation, it will directly return the rendering of the lines as made by an instance of DISPOSER_CLASS.
	"""
	
	LINE_RENDERER_CLASS = AbstractLineRenderer

	NO_TRANSLATION_DISPOSER = AbstractNoTranslationDisposer
	AFTER_TEXT_TRANSLATION_DISPOSER = AbstractAfterTextDisposer
	EACH_STANZA_TRANSLATION_DISPOSER = AbstractEachStanzaDisposer
	EACH_LINE_TRANSLATION_DISPOSER = AbstractEachLineDisposer
	SIDE_BY_SIDE = AbstractSideBySideDisposer

	def __init__(self, body: JsonText):
		self._body = body
	
	@property
	def body(self):
		return self._body
	
	@property
	def disposers(self):
		return {
			TranslationArrangement.NO_TRANSLATION: self.__class__.NO_TRANSLATION_DISPOSER,
			TranslationArrangement.AFTER_TEXT: self.__class__.AFTER_TEXT_TRANSLATION_DISPOSER,
			TranslationArrangement.EACH_STANZA: self.__class__.EACH_STANZA_TRANSLATION_DISPOSER,
			TranslationArrangement.EACH_LINE: self.__class__.EACH_LINE_TRANSLATION_DISPOSER,
			TranslationArrangement.SIDE_BY_SIDE: self.__class__.SIDE_BY_SIDE_TRANSLATION_DISPOSER,
		}
	
	def _get_disposer(self, translation_arrangement: TranslationArrangement) -> abc.ABCMeta:
		"""Return the concrete disposer class (not the instance) correspondent to translation_arrangement."""
		disposer = self.disposers[translation_arrangement]
		if disposer == None:
			raise DisposerException(translation_arrangement)
		return disposer		
		
	@abc.abstractmethod
	def build_disposer(self, line_renderers : Tuple[Tuple[AbstractLineRenderer]], translation_arrangement: TranslationArrangement):
		disposer = self._get_disposer(translation_arrangement)
		if disposer == None:
			raise DisposerException(translation_arrangement)
		return disposer(line_renderers)
		
	@abc.abstractmethod
	def build_line_renderer(self, line, translation_id):
		return self.__class__.LINE_RENDERER_CLASS(line, translation_id)

	def _build_line_renderers_for_stanza(self, stanza: JsonStanza, translation_id: str):
		ret_tuple = tuple(self.build_line_renderer(line, translation_id) for line in stanza.iter_lines())
		
		return ret_tuple
		
	def _build_line_renderers(self, translation_id: str):
		ret_tuple = tuple(self._build_line_renderers_for_stanza(stanza, translation_id) for stanza in self.body.iter_stanzas())
		
		#now we assign to each line its number in the poem:
		i = 1
		for stanza in ret_tuple:
			for line_renderer in stanza:
				line_renderer.number = i
				i += 1

		return ret_tuple

	@abc.abstractmethod
	def render(self, translation_id: str, translation_arrangement: TranslationArrangement, line_numbers_after: int) -> str:
		"""Builds the view and returns it as a string (this function doesn't save it on a file).
		
		Args:
			translation_id (str): the id of the translation to insert into the view, or None if no translation is desired.
			translation_arrangement (TranslationArrangement): an member of the :class:`TranslationArrangement` enum class.
			line_numbers_after (int): says after how many lines the line number must be included in the rendering. If it is None, line numbers will be added to no line.
			
		
		Returns
			view (str): the view of the text as string.
		
		Raises
			MissingTranslationError: raised if one tries to render a translation not present in the json file.
		"""
		
		line_renderers = self._build_line_renderers(translation_id)
		disposer = self.build_disposer(line_renderers, translation_arrangement)
		return disposer.get_rendered_lines(line_numbers_after)
