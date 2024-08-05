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


class JsonException(Exception):
	"""Base class for JSON parsing exceptions"""
	
	def __init__(self):
		super().__init__()


class FieldControlException(JsonException):
	"""Base class for exceptions raised from Metadata validation processes."""

	def __init__(self):
		super().__init__()


class InvariableFieldError(JsonException):
	"""Base class for exceptions raised from Metadata validation processes."""

	def __init__(self, field):
		super().__init__()
		self.field = field

	def __str__(self):
		return "The field '%s' is unvariable and can not be changed after being inserted in the dictionary."%self.field


class MandatoryFieldError(FieldControlException):
	"""Raised when one tries to delete a mandatory field from a metadata dictionary."""
	
	def __init__(self, field):
		super().__init__()
		self.field = field
	
	def __str__(self):
		return "The field '%s' is mandatory and can not be deleted."%self.field


class InvalidLanguageError(FieldControlException):
	"""Raised when one tries to set 'language' without a valid iso639-3 code."""
	
	def __init__(self, code):
		super().__init__()
		self.code = code
	
	def __str__(self):
		return "The language code '%s' is not an ISO639-3 alpha-3 one."%self.code


class InvalidCountryError(FieldControlException):
	"""Raised when one tries to set 'country' without a valid iso3166 code."""
	
	def __init__(self, code):
		super().__init__()
		self.code = code
	
	def __str__(self):
		return "The country code '%s' is not an ISO3166 alpha-3 one."%self.code


class InvalidScriptError(FieldControlException):
	"""Raised when one tries to set 'script' without a valid iso15924 code."""
	
	def __init__(self, code):
		super().__init__()
		self.code = code
	
	def __str__(self):
		return "The script code '%s' is not an ISO15924 one."%self.code


class NullSourceNoteException(JsonException):

	def __init__(self, translation_note):
		self.translation_note = translation_note
		
	def __str__(self):
		return "Tried to add translation note '%r' to null source note"%self.translation_note

