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


class TranslationException(Exception):
	"""Base class for all the exceptions that can be raised during translation parsing."""

	def __init__(self):
		super().__init__()	


class TranslationMetadataException(TranslationException):
	"""Base class for all the exceptions that can be raised from metadata during translation parsing."""

	def __init__(self):
		super().__init__()	


class InvalidLanguageError(TranslationMetadataException):

	def __init__(self, langcode):
		super().__init__()
		self.langcode = langcode
		
	def __str__(self):
		return "Invalid language iso639-3 code: '%s'"%self.langcode


class InvalidFieldError(TranslationMetadataException):

	def __init__(self, fieldline):
		super().__init__()
		self.fieldline = fieldline
		
	def __str__(self):
		return "Invalid field line: '%s'"%self.fieldline


class MissingFieldError(TranslationMetadataException):

	def __init__(self, field):
		super().__init__()
		self.field = field
		
	def __str__(self):
		return "Missing field: '%s'"%self.field

