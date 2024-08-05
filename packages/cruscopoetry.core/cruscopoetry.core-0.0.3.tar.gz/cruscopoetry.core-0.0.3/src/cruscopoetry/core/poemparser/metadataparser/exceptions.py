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


class MetadataException(Exception):
	"""Base class for all the exceptions that can be raised during metadata parsing."""

	def __init__(self):
		super().__init__()	


class InvalidScriptError(MetadataException):

	def __init__(self, scriptcode):
		super().__init__()
		self.scriptcode = scriptcode
		
	def __str__(self):
		return "Invalid script iso15924 code: '%s'"%self.scriptcode


class InvalidCountryError(MetadataException):

	def __init__(self, countrycode):
		super().__init__()
		self.countrycode = countrycode
		
	def __str__(self):
		return "Invalid country iso3166_3 code: '%s'"%self.countrycode


class InvalidLanguageError(MetadataException):

	def __init__(self, langcode):
		super().__init__()
		self.langcode = langcode
		
	def __str__(self):
		return "Invalid language iso639-3 code: '%s'"%self.langcode


class InvalidFieldError(MetadataException):

	def __init__(self, fieldline):
		super().__init__()
		self.fieldline = fieldline
		
	def __str__(self):
		return "Invalid field line: '%s'"%self.fieldline


class MissingFieldError(MetadataException):

	def __init__(self, field):
		super().__init__()
		self.field = field
		
	def __str__(self):
		return "Missing field: '%s'"%self.field

