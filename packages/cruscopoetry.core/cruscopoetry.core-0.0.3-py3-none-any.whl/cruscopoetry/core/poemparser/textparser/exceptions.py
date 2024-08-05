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


class TextParsingException(Exception):
	"""Base class for all the exceptions that can be raised in text parsing. These exceptions will be handled so that, while raising it, there will be also a reference to the line they come from."""

	def __init__(self):
		super().__init__()


class SyllabificationSyntaxError(TextParsingException):
	"""Exception class for bad syllabification syntax."""
	
	def __init__(self, bad_string: str):
		super().__init__()
		self.bad_string = bad_string
		
	def __str__(self):
		return "Invalid syllabification syntax: '%s'"%self.bad_string
		

class SpacingSyllabificationSyntaxError(SyllabificationSyntaxError):
	"""Exception class for the occurrence of more syllabification syntaxes next to each other and not separated by spacing."""

	def __init__(self, bad_string):
		super().__init__()
		
	def __str__(self):
		ret_str = super().__str__()
		ret_str += "\nMore syllabification blocks must be separated by spacing! Try enclosing all this in one syllabification block."
		return ret_str


class TranscriptionSyntaxError(TextParsingException):
	"""Exception class for bad transcription syntax."""
	
	def __init__(self, bad_string: str):
		super().__init__()
		self.bad_string = bad_string
		
	def __str__(self):
		return "Invalid transcription syntax: '%s'"%self.bad_string


class ColonMarkerError(TextParsingException):
	"""Exception class for bad colon markers placement."""
	
	def __init__(self, bad_string: str):
		super().__init__()
		self.bad_string = bad_string
		
	def __str__(self):
		return "Invalid transcription syntax: '%s'"%self.bad_string


class UnrecognizedCharacterWarning(TextParsingException):
	"""Exception class raised when a syllabifier finds an unknown character in a word. Normally, this exception does not stop the execution, but prints a warning."""

	def __init__(self, char):
		super().__init__()
		self.phoneme = char


class LabelError(TextParsingException):
	"""Exception class concerning labels."""

	def __init__(self):
		super().__init__()
	
	def __str___(self):
		return "Labels can not have 'all' as value"
		

class LabelMatchError(TextParsingException):
	"""Exception class concerning the parsing of labels."""

	def __init__(self, line_string):
		super().__init__()
		self._line_string = line_string
	
	def __str___(self):
		return "Label parsing has given None as result. Line: '%s'"%self._line_string

