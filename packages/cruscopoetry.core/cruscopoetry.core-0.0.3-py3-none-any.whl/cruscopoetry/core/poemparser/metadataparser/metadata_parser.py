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
import os
import re
import pycountry
from .exceptions import *
from ...markers import Markers


class Metadata:
	"""Represents the metadata section of the poem. All the key-value information is contained in the `field` attribute, which is a built-in dictionary.
	
	Args:
		metadata: the string representing the metadata section of the poem file.
	"""
	
	MANDATORY_FIELDS = ("title", "author", "language", "script", "country")
	ONLY_WHITESPACES = re.compile("^\\s*$")
	FIELDS_REGEX = re.compile("^\\s*(?P<key>\\S+?)\\s*=\\s*(?P<value>.+)$")

	def __init__(self, metadata: str):
		#first, we eliminate comments:
		fields = re.sub("%s.*"%Markers.COMMENT, "", metadata)
		fields = fields.split(os.linesep)
		
		fields = [field for field in fields if self.__class__.ONLY_WHITESPACES.match(field) == None] #deleting empty lines
		self.fields = {}
		for fieldline in fields:
			match = self.__class__.FIELDS_REGEX.match(fieldline)
			if match == None:
				raise InvalidFieldError(fieldline)

			key, value = match.group('key').strip(), match.group('value').strip()
			#we check that what remains after stripping are not empty strings:
			if len(key) == 0 or len(value) == 0:
				raise InvalidFieldError(fieldline)
				
			self.fields[key] = value
		
		for field in self.__class__.MANDATORY_FIELDS:
			if field not in self.fields.keys():
				raise MissingFieldError(field)
		
		#it is better to save the values of the fields language, country and script in any case in lowercase:
		self.fields['language'] = self.fields['language'].lower()
		self.fields['country'] = self.fields['country'].lower()
		self.fields['script'] = self.fields['script'].lower()
				
		#checking if language value is a iso639-3 language code:
		language = pycountry.languages.get(alpha_3=self.fields['language'])
		if language == None:
			raise InvalidLanguageError(self.fields['language'])
			
		#checking if the country code is a valid code
		country = pycountry.countries.get(alpha_3=self.fields['country'])
		if country == None:
			raise InvalidCountryError(self.fields['country'])

		#checking if script code is valid
		script = pycountry.scripts.get(alpha_4=self.fields['script'])
		if script == None:
			raise InvalidScriptError(self.fields['script'])
			
	@property
	def mandatory_fields(self):
		return {key: self.fields[key] for key in self.__class__.MANDATORY_FIELDS}
	
	@property
	def additional_fields(self):
		return {key: self.fields[key] for key in self.fields.keys() if key not in self.__class__.MANDATORY_FIELDS}

	def json_dict(self) -> dict:
		return self.fields

	def __repr__(self):
		ret_str = ""		
		for key, value in self.mandatory_fields.items():
			ret_str += "%s = %s\n"%(key, value)

		for key, value in self.additional_fields.items():
			ret_str += "%s = %s\n"%(key, value)
		return ret_str
