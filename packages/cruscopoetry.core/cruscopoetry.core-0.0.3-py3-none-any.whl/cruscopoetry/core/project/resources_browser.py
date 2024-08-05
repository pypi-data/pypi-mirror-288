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
from ..poemparser import poem_parser
from ..translationparser import translation_parser
from .. import jsonparser
from .exceptions import *
from pathlib import Path


class AbstractResourcesBrowser(metaclass=abc.ABCMeta):

	SOURCE_FILE_NAME = "source.txt"
	TRANSLATIONS_DIR = "translations"
	JSON_FILE_NAME = "poem.json"

	def __init__(self, path: str):
		self._path = path
	
	@property
	def path(self) -> str:
		return self._path

	@abc.abstractmethod
	def get_source(self) -> poem_parser.Poem:
		pass
	
	@abc.abstractmethod
	def get_translations(self) -> Tuple[translation_parser.TranslationParser]:
		pass
		
	@abc.abstractproperty
	def json_path(self) -> str:
		"""Returns the path, or generally the position, where the built json file must be stored"""
		pass
		
	@abc.abstractproperty
	def json_exists(self) -> str:
		"""Returns True if the json file has already been created and stored in the project."""
		pass
		
	@abc.abstractproperty
	def json_parser(self) -> jsonparser.JsonParser:
		"""Returns the already compiled project's poem as a JsonParser instance"""
		pass
	

class DirResourcesBrowser(AbstractResourcesBrowser):
	
	def __init__(self, path: str):
		super().__init__(path)
		
		#if the json file is not yet build, it will remain None. Else, it will contain the JsonParser instance of the poem
		self._json_parser: json_parser.JsonParser = None
		
	@property	
	def path(self) -> Path:
		return Path(super().path)
	
	@property	
	def translations_dir(self) -> Path:
		return self.path.joinpath(self.__class__.TRANSLATIONS_DIR)
	
	def get_source(self) -> poem_parser.Poem:
		path = self.path.joinpath(self.__class__.SOURCE_FILE_NAME)
		return poem_parser.Poem(str(path))
		
	def get_translations(self) -> Tuple[translation_parser.TranslationParser]:
		names = tuple(str(tr_file) for tr_file in self.translations_dir.glob("*.txt"))
		translations = tuple(translation_parser.TranslationParser(tr_file) for tr_file in names)
		return translations

	@property
	def json_path(self) -> str:
		return str(self.path.joinpath(self.__class__.JSON_FILE_NAME))
		
	@property
	def json_exists(self):
		return self.path.joinpath(self.__class__.JSON_FILE_NAME).exists()

	@property
	def json_parser(self):
		if self._json_parser == None:
			if not self.json_exists:
				raise ProjectNotBuiltException(self.path)
			
			self._json_parser = jsonparser.JsonParser(self.json_path)
		return self._json_parser
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
