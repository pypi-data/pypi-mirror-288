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
from ..base_parser import BaseParser


class AbstractViewer(BaseParser,metaclass=abc.ABCMeta):
	"""This class provides an interface for all the viewers. A viewer's role is that of parsing the JSON file and organizing its material in a human-readable way (es. a HTML page, or pure text).
	Viewers must be able to render the text either with no or with one translation, and in this last case to organize the translation after the whole text, stanza by stanza or line by line.
	
	Args:
		path (str): the path of the JSON file that must be rendered.
	"""
	
	NO_TRANSLATION = 0
	AFTER_TEXT = 1
	STANZA_BY_STANZA = 2
	LINE_BY_LINE = 3

	def __init__(self, path: str):
		super().__init__(path)

	@abstractmethod
	def render(self, translation_id: str = None, translation_arrangement: int = self.__class__.NO_TRANSLATION) -> str:
		"""Builds the view and returns it as a string (this function doesn't save it on a file.
		
		Args:
			translation_id (str): the id of the translation to insert into the view, or None if no translation is desired.
			translation_arrangement (int): an integer between AbstractViewer.NO_TRANSLATION , AbstractViewer.AFTER_TEXT , AbstractViewer.STANZA_BY_STANZA and AbstractViewer.LINE_BY_LINE.
		
		Returns
			view (str): the view of the text as string.
		"""
		pass
