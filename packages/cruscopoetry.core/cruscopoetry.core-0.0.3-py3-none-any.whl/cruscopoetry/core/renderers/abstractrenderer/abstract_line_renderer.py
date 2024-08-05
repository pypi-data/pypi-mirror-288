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
from ...jsonparser import JsonLine, JsonTranslation
from typing import Tuple
from .exceptions import LineNumberingError
	
	
class AbstractLineRenderer(metaclass=abc.ABCMeta):
	"""Abstract class for line renderers.
	
	Args:
		jline (JsonLine): the line that must be rendered
		translation_id (str): the id of the translation that must be represented in the rendering, or None if no translation needs to be included.
	"""

	def __init__(self, jline: JsonLine, translation_id: str):
		self._jline = jline
		self._translation: str = jline.get_translation_by_id(translation_id) if translation_id != None else None
		self._number: int = 0
	
	@property
	def number(self):
		return self._number
	
	@number.setter
	def number(self, integer: int):
		if self._number == 0:
			self._number = integer
		else:
			raise LineNumberingError
	
	@property
	def index(self):
		return self._jline.index
	
	@property
	def jline(self) -> JsonLine:
		return self._jline
	
	@property
	def translation(self) -> JsonTranslation:
		return self._translation
	
	@abc.abstractmethod
	def get_source(self):
		"""Returns a view of the line's source text, built in such a way that an AbstractDisposer instance could arrange it in a rendering style."""
		pass
	
	@abc.abstractmethod
	def get_translation(self):
		"""Returns a view of the line's translation text, built in such a way that an AbstractDisposer instance could arrange it in a rendering style."""
		pass
