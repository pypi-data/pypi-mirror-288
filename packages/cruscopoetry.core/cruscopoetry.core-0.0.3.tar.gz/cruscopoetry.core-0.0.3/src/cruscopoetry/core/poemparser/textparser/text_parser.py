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
from . import syntax_handlers
from ...markers import Markers
from .exceptions import *


class Word:

	NON_SYLLABIFIED_REGEX = re.compile("[^|\\[\\]]+")
	SYLLABIFIED_REGEX = re.compile("\\[(\\w+\\|)*\\w+\\]")
	
	def __init__(self, word_string: str):
		self.string = word_string

		#we check if the string is manually syllabified and, in that case, that the syntax is correct:
		if self.__class__.NON_SYLLABIFIED_REGEX.fullmatch(self.string) != None:
			self.is_manually_syllabified = False
		else:
			if self.__class__.SYLLABIFIED_REGEX.fullmatch(self.string) != None:
				self.is_manually_syllabified = True
			else:
				#if the error is due to the fact that two or more syllabification blocks are not separated  by spacing, we raise a more specific exception:
				if len(tuple(self.__class__.SYLLABIFIED_REGEX.findall(self.string))) > 1:
					raise syntax_handlers.SpacingSyllabificationSyntaxError(self.string)
				#else we raise a general one:
				else:
					raise syntax_handlers.SyllabificationSyntaxError(self.string)
		
		#now we set self.syllables as None, this value will be changed by syllabifier plugins	
		self.syllables = None
		
	def split(self, char: str):
		"""Splits the word string on the occurrences of ``char`` and builds a tuple of Word objects from the result. Useful in syllabification."""
		sections = self.string.split(char)
		return tuple(self.__class__(section) for section in sections)
		
	def raise_unrecognized_char_warning(self, char):
		raise UnrecognizedCharacterWarning(char)
		
	def json_dict(self) -> dict:
		ret_dict = {
			"string": self.string,
			"syllables": self.syllables,
		}
		return ret_dict
		
	def __repr__(self):
		return "%s(%s)"%(self.__class__.__name__, self.string)


class InvalidColonError(Exception):

	def __init__(self, match):
		super().__init__()
		self.match = match
		
	def __str__(self):
		ret_str = "Invalid misplacement of character %s or %s:\n"%(Markers.CRASIS, Markers.ELISION)
		ret_str += "\n" + self.show()
		return ret_str
	
	def show(self):
		ret_str = ""
		ret_str += self.match.string + "\n"
		ret_str += " "*(self.match.span()[0]-1) + "!" + "-"*(self.match.span()[1]-self.match.span()[0]-1)
		return ret_str
	
	
class Colon:
	"""Represents the parsing of the line of a poem. This class splits the line in (phonetic) words and builds :class:`Word` instances from them; moreover, it also stores the transcription of the 
	colon as read from the source
	
	Args:
		colon_string (str): the string representing the line in Cruscopoetry format
		previous_WIB (bool): True if the colon is preceded by a word-internal boundary
		following_WIB (bool): True if the colon is followed by a word-internal boundary
	
	Attributes:
		transcription (str): a string representing the colon as written in the source
		words (tuple): a tuple of :class:`Word` instances, representing the (phonetic) words of the poem.
		previous_WIB (bool): True if the colon is preceded by a word-internal boundary
		following_WIB (bool): True if the colon is followed by a word-internal boundary
	"""

	def __init__(self, colon_string: str, previous_WIB: bool = False, following_WIB: bool = False):
		transcription, phonetics = syntax_handlers.Transcription.parse_colon(colon_string)
		self.previous_WIB = previous_WIB
		self.following_WIB = following_WIB
		
		#syllabification syntax has not yet been handled. Since it has no use in the transcription (which will not be used for further parsing), we can cancel it from the string.
		#The crasis marker remains; the user can eventually decide itself to remove it or replace it with another character (es. a space):
		self.transcription = re.sub("\\[|\\||\\]", "", transcription)
		
		#instead, in phonetics we have to remove the punctuation and lower all letters:
		self.phonetics = re.sub("[\\.,:;\\?!«»‘’“”\"]", "", phonetics).lower()

		#we substitute the elision markers that are at the beginning or end of the colon or next to whitespaces with a space character:
		self.phonetics = re.sub("((^|\\s+)')|('(\\s+|$))", " ", self.phonetics)

		#we control also that the crasis marker is not put next to spaces, or at the beginning or at the end of the verse:		
		control_re = re.compile("((^|\\s+)%s)|(%s(\\s+|$))"%(Markers.CRASIS, Markers.CRASIS))
		if match := control_re.search(self.phonetics) != None:
			raise InvalidColonError(match)
			
		#now we replace all the sequences of whitespace remained in phonetics with single spaces:
		self.phonetics = re.sub("\\s+", " ", self.phonetics)

		#and we get the words:
		self.words = tuple(Word(word) for word in self.phonetics.split())

	def iter_words(self):
		yield from self.words

	def __repr__(self):
		ret_str = "..." if self.previous_WIB else ""
		ret_str += self.transcription
		if self.following_WIB:
			ret_str += "..."
		return ret_str
		
	def json_dict(self) -> dict:
		ret_dict = {
			"transcription": self.transcription,
			"words": tuple(word.json_dict() for word in self.words),
			"pwib": self.previous_WIB,
			"fwib": self.following_WIB
		}
		return ret_dict


class Line:
	"""Represents the parsing of the line of a poem. This class splits the line in cola and builds :class:`Cola` instances from them.
	
	Args:
		line_string (str): the string representing the line in Cruscopoetry format
	
	Attributes:
		cola (tuple): a tuple of :class:`Cola` instances, representing the cola of the poem.
		label (str): the label attributed to the verse, or None if no label has been specified.
	"""
	
	LABEL_REGEX = re.compile("^\\s*(\\$(?P<label>\\w+))?\\s*(?P<line>.+)$")
	
	def __init__(self, line_string: str):
		match = self.__class__.LABEL_REGEX.match(line_string)
		if match == None:
			print("'%s'"%line_string)
			raise LabelMatchError(line_string)
		self.label = match.group("label")
		if self.label == "all":
			raise LabelError
		line = match.group("line")
		line = line.strip()
		if (line[0] in (Markers.COLON_SEP, Markers.WORD_INTERNAL_COLON_SEP) or line[-1] in (Markers.COLON_SEP, Markers.WORD_INTERNAL_COLON_SEP)):
			raise ColonMarkerError(line)
		cola = re.split("(%s|%s)"%(Markers.COLON_SEP, Markers.WORD_INTERNAL_COLON_SEP), line)
		while '' in cola:
			cola.remove('')

		#verse parsing will also handle the exceptions raised by further parsing and store them, so that it can be raised with a reference to the verse line:
		self.exceptions = []
		
		for i in range(len(cola)):
			if cola[i] in (Markers.COLON_SEP, Markers.WORD_INTERNAL_COLON_SEP):
				continue

			previous_word_internal_boundary = False
			following_word_internal_boundary = False
			if i > 0: 
				if cola[i-1] == Markers.WORD_INTERNAL_COLON_SEP:
					previous_word_internal_boundary = True
			if i < len(cola)-1:
				if cola[i+1] == Markers.WORD_INTERNAL_COLON_SEP:
					following_word_internal_boundary = True

			#now we can strip the colon strip and build our object:
			cola[i] = cola[i].strip()
			try:
				cola[i] = Colon(cola[i], previous_word_internal_boundary, following_word_internal_boundary)
			except TextParsingException as e:
				self.exceptions.append(e)

		#now we can remove the colon boundary markers and instantiate our Colon objects:
		cola = [colon for colon in cola if colon not in (Markers.COLON_SEP, Markers.WORD_INTERNAL_COLON_SEP)]
		self.cola = tuple(cola)
		
	def __repr__(self):
		ret_str = ""
		for i in range(len(self.cola)-1):
			ret_str += self.cola[i].transcription
			if self.cola[i].following_WIB == True:
				ret_str += Markers.WORD_INTERNAL_COLON_JOIN
			else:
				ret_str += Markers.COLON_JOIN
		ret_str += self.cola[-1].transcription
		return ret_str

	def iter_cola(self):
		yield from self.cola

	def iter_words(self):
		for colon in self.iter_cola():
			yield from colon.iter_words()

	def json_dict(self) -> dict:
		ret_dict = {
			"label": self.label,
			"cola": tuple(colon.json_dict() for colon in self.cola)
		}
		return ret_dict
				

class Stanza:
	"""Represents the parsing of the stanza of a poem. This class split the string representing the stanza in lines and builds :class:`Line` instances from them.
	
	Args:
		stanza_string (str): the string representing the stanza in Cruscopoetry format
	
	Attributes:
		lines (tuple): a tuple of :class:`Line` instances, representing the lines of the poem.
	"""

	def __init__(self, stanza_string: str):
		self.lines = tuple(Line(line) for line in stanza_string.split(Markers.LINE_SEP))
		
	def __repr__(self):
		return Markers.LINE_SEP.join((line.__repr__() for line in self.lines))

	def iter_lines(self):
		yield from self.lines

	def iter_cola(self):
		for line in self.iter_lines():
			yield from line.iter_cola()

	def iter_words(self):
		for colon in self.iter_cola():
			yield from colon.iter_words()

	def json_dict(self) -> dict:
		ret_dict = {
			"lines": tuple(line.json_dict() for line in self.lines)
		}
		return ret_dict


class Text:
	"""Represents the parsing of a *TEXT* section of a poem. This class adjust the whitespace formatting of the text string and parses its stanzas in :class:`Stanza` instances.
	
	Args:
		text_string (str): the string representing the text in Cruscopoetry format
	
	Attributes:
		stanzas (tuple): a tuple of :class:`Stanza` instances, representing the stanzas of the poem.
	"""

	#this regex exception, employed with re.sub,  trims all the lines internal in the string:
	ONLY_WHITESPACES_LINES ="[^\\S\n\r]*" + os.linesep + "[^\\S\n\r]*"

	def __init__(self, text_string: str):
		text_string = re.sub(self.__class__.ONLY_WHITESPACES_LINES, os.linesep, text_string)
		text_string = re.sub("^[^\\S\n\r]*"+os.linesep, "", text_string)
		text_string = re.sub(os.linesep+"[^\\S\n\r]*$", "", text_string)

		#after having trimmed the lines, we find the occurrences of three or more line separator characters and replace them with two occurrences of them (corresponding to stanza boundaries):
		text_string = re.sub("%s{3,}"%Markers.LINE_SEP, Markers.STANZA_SEP, text_string)

		#then, we find comments and delete them and the newline they end with from the text:
		text_string = re.sub("%s.*"%Markers.COMMENT, "", text_string)
		
		#now we can split text_string and obtain a tuple of Stanza Objects.		
		text_stanzas = text_string.split(Markers.STANZA_SEP)
		while '' in text_stanzas:
			text_stanzas.remove('')
		
		#there is still the possibility that the first line of the poem contains \n as starting character.
		#this happens if it is separated by ONLY ONE blank line from the head of the text section. We eliminate
		#this \n char if it is there:
		if text_stanzas[0][0] == '\n':
			text_stanzas[0] = text_stanzas[0][1:]

		self.stanzas: tuple = tuple(Stanza(stanza) for stanza in text_stanzas)
		
		#finally, we iterate over the lines and work on the exceptions that have been stored:
		for index, line in enumerate(self.iter_lines()):
			for exception in line.exceptions:
				try:
					self.print_error(index+1, line.label, exception)
					raise exception
				except UnrecognizedCharacterWarning as e:
					self.print_warning(index+1, line.label, e)

	def print_warning(self, verse_number, verse_label, exception):
		print("\033[1;33;40mWarning\033[m. Unrecognized character at line %d (label '%s'): '%s'"%(verse_number, verse_label, exception.phoneme))

	def print_error(self, verse_number, verse_label, exception):
		print("\033[1;31;40mError\033[m at line %d (label '%s')."%(verse_number, verse_label))
		raise exception
		
	def __repr__(self):
		return Markers.STANZA_SEP.join((stanza.__repr__() for stanza in self.stanzas))

	def iter_stanzas(self):
		yield from self.stanzas

	def iter_lines(self):
		for stanza in self.iter_stanzas():
			yield from stanza.iter_lines()

	def iter_cola(self):
		for line in self.iter_lines():
			yield from line.iter_cola()

	def iter_words(self):
		for colon in self.iter_cola():
			yield from colon.iter_words()

	def json_dict(self) -> dict:
		ret_dict = {
			"stanzas": tuple(stanza.json_dict() for stanza in self.stanzas)
		}
		return ret_dict

