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
from ...base_parser import BaseParser
from ...jsonparser import JsonParser
from ..exceptions import MissingTranslationError
from typing import Tuple
from .abstract_metadata_renderer import AbstractMetadataRenderer
from .abstract_text_body_renderer import AbstractTextBodyRenderer
from .abstract_notes_renderer import AbstractNotesRenderer
from .translation_arrangement import TranslationArrangement


class AbstractRenderer(BaseParser,metaclass=abc.ABCMeta):
	"""This class provides an interface for all the renderers. A renderer's role is that of parsing the JSON file and organizing its material in a human-readable way (es. a HTML page, or pure text).
	Viewers must be able to render the text either with no or with one translation, and in this last case to organize the translation after the whole text, stanza by stanza or line by line.
	
	Args:
		poem (str | JsonParser): the poem that must be rendered. It can be either a JsonParser instance or the path of the json file (as string).
	
	Attrs:
		path (str): the path of the JSON file that must be rendered.
		json (JsonParser): the instance of JsonParser that represents the poem.
		metadata (AbstractMetadataRenderer): the object that provides the rendering of the metadata.
		body (AbstractMetadataRenderer): the object that provides the rendering of the text's body.
		notes (AbstractMetadataRenderer): the object that provides the rendering of the notes.
		
	Class Attrs:
		METADATA_RENDERER (abc.abcMETA): the concrete implementation of AbstractMetadataRenderer that creates the instance in self.metadata.
		TEXT_BODY_RENDERER (abc.abcMETA): the concrete implementation of AbstractTextBodyRenderer that creates the instance in self.body.
		NOTES_RENDERER (abc.abcMETA): the concrete implementation of AbstractNotesRenderer that creates the instance in self.notes.

	Concrete implementations of this class need to implement four methods:
	 - build_metadata_renderer
	 - build_text_body_renderer
	 - build_notes_renderer
	 - render
	 
	Coding inheriting classes its made easier by the possibility of overriding the three class attributes METADATA_RENDERER, TEXT_BODY_RENDERER and NOTES_RENDERER with the concrete children classes
	of AbstractMetadataRenderer, AbstractTextBodyRenderer and AbstractNotesRenderer that one needs to employ. If the concrete implementations of these classes take the same initialization parametres 
	of they abstract base classes, you can override the correspondend build method simply calling the super() one.
	
	"""
	METADATA_RENDERER = AbstractMetadataRenderer
	TEXT_BODY_RENDERER = AbstractTextBodyRenderer
	NOTES_RENDERER = AbstractNotesRenderer

	def __init__(self, poem: str):
		if type(poem) == str:
			super().__init__(poem)
			self.json = JsonParser(self.path)
		elif type(poem) == JsonParser:
			self.json = poem
			self.path = poem.path
		self._metadata_renderer = self.build_metadata_renderer(self.json)
		self._text_body_renderer = self.build_text_body_renderer(self.json)
		self._notes_renderer = self.build_notes_renderer(self.json)

	@property
	def metadata(self):
		return self._metadata_renderer

	@property
	def body(self):
		return self._text_body_renderer

	@property
	def notes(self):
		return self._notes_renderer

	def adjust_translation_data(self, translation_id: str, translation_arrangement: int):
		"""Checks the translation data given as input and adjust them for the rendering.
		
		Args:
			translation_id: the id of the translation
			translation_arrangement: the member of the :class:`TranslationArrangement` enum class indicating how to adjust the translation.
		
		Returns:
			translation_id
			translation_arrangement as the parametre passed if translation_id is not null, else :attribute:`TranslationArrangement.NO_TRANSLATION`
		
		Raises:
			MissingTranslationError: raised if no translation with it `translation_id` is found in the text.
		"""
		if (translation_id != None) and (translation_id not in self.json.translations):
			raise MissingTranslationError(translation_id, self.json.title)

		if translation_id == None:
			translation_arrangement = TranslationArrangement.NO_TRANSLATION
		
		#conversely, we set translation_id to None if translastion_arrangement is NO_TRANSLATION:
		if translation_arrangement == TranslationArrangement.NO_TRANSLATION:
			translation_id = None

		return translation_id, translation_arrangement

	@abc.abstractmethod
	def build_metadata_renderer(self, json: JsonParser):
		return self.__class__.METADATA_RENDERER(self.json.metadata, self.json.translations)

	@abc.abstractmethod
	def build_text_body_renderer(self, json: JsonParser):
		return self.__class__.TEXT_BODY_RENDERER(self.json.text)

	@abc.abstractmethod
	def build_notes_renderer(self, json: JsonParser):
		lines_map = self.json.text.labels_to_indexes_dict
		#we pass to NOTES_RENDERER constructor also a reference to json.translation, so that it can access the translation note<s:
		return self.__class__.NOTES_RENDERER(self.json.notes, lines_map, self.json.translations)

	@abc.abstractmethod
	def render(self, translation_id: str, translation_arrangement: int) -> str:
		"""Builds the view and returns it as a string (this function doesn't save it on a file.
		
		Args:
			translation_id (str): the id of the translation to insert into the view, or None if no translation is desired.
			translation_arrangement (int): an integer between AbstractViewer.NO_TRANSLATION , AbstractViewer.AFTER_TEXT , AbstractViewer.STANZA_BY_STANZA and AbstractViewer.LINE_BY_LINE.
		
		Returns
			view (str): the view of the text as string.
		
		Raises
			MissingTranslationError: raised if one tries to render a translation not present in the json file.
		"""
		pass
		
		
		
