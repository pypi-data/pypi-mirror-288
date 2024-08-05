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
from .joiners import Joiners
from .exceptions import InvalidLanguageError, InvalidCountryError, InvalidScriptError, MandatoryFieldError
from .utils import MetadataDict, MetadataValidator


class JsonMetadata:
	"""Class representing the metadata of a JSON-serialized poem. It behaves as a normal Python dictionary, but several validations are carried out while trying to set or delete items.
	
	Args:
		jdict (dict): the dictionary resulting from the JSON parsing and corresponding to the metadata section of the poem.
	
	Attrs:
		jdict (MetadataDict): the MetadataDict instance resulting from the JSON parsing.
	"""
	MANDATORY_FIELDS = ("title", "author", "language", "script", "country")

	def __init__(self, jdict):

		#here we set the requirements. Each tuple containes the name of a field; the second argument sets whether the field is mandatory; the third whether it is editable;
		#the fourth the validations it needs to go through
		requirements = [
			("title", True, False, MetadataValidator.NO_CONTROL),
			("author", True, False, MetadataValidator.NO_CONTROL),
			("language", True, False, MetadataValidator.LANGUAGE),
			("country", True, False, MetadataValidator.COUNTRY),
			("script", True, False, MetadataValidator.SCRIPT),
		]
		validator = MetadataValidator(requirements)
		self.__jdict = MetadataDict(jdict, validator)

	def json_dict(self):
		"""Returns the metadata dictionary with eventual updates."""
		return self.__jdict.dict
		
	def __getitem__(self, key):
		"""As dict.__getitem__(key)"""
		return self.__jdict.__getitem__(key)

	def __len__(self):
		"""As dict.__len__()"""
		return len(self.__jdict)
	
	def __iter__(self):
		"""As dict.__iter__()"""
		return iter(self.__jdict)
		
	def keys(self):
		"""As dict.keys()"""
		return self.__jdict.keys()
		
	def values(self):
		"""As dict.values()"""
		return self.__jdict.values()
		
	def items(self):
		"""As dict.items()"""
		return self.__jdict.items()

	@property
	def title(self):
		"""The poem's title"""
		return self.__jdict["title"]

	@property
	def author(self):
		"""The poem's author"""
		return self.__jdict["author"]

	@property
	def language(self):
		"""The poem's language"""
		return self.__jdict["language"]

	@property
	def script(self):
		"""The poem's script"""
		return self.__jdict["script"]

	@property
	def country(self):
		"""The poem's country"""
		return self.__jdict["country"]
			
	def mandatory_keys(self) -> list:
		"""The keys of the mandatory metadata fields"""
		return self.__jdict.mandatory_keys()
			
	def mandatory_values(self) -> list:
		"""The values of the mandatory metadata fields"""
		return self.__jdict.mandatory_values()
			
	def mandatory_items(self) -> list:
		"""The item pairs of the mandatory metadata fields"""
		return self.__jdict.mandatory_items()
	
	def optional_keys(self) -> list:
		"""The keys of the optional metadata fields"""
		return self.__jdict.optional_keys()
	
	def optional_values(self) -> list:
		"""The values of the optional metadata fields"""
		return self.__jdict.optional_values()
	
	def optional_items(self) -> list:
		"""The item pairs of the optional metadata fields"""
		return self.__jdict.optional_items()

	@property
	def as_text(self):
		"""A plain text representation of the metadata (useful if one wants to build back the txt source file)"""
		ret_string = "METADATA" + Joiners.LINES + self.__jdict.as_text
		return ret_string
