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

from .text_element import *
#from ..translationparser.translation_parser import TranslationParser
#from .translations import JsonTranslations
import re
from .utils import TreeDict


class JsonPhoneme(JsonNumberedElement):
	"""Represents the phoneme of a syllable"""
	
	#since the phoneme dictionary is highly customizable, we just store it in the jdict attribute:
	def __init__(self, index, jdict: dict):
		super().__init__(index, jdict)
		
	def __str__(self):
		if "string" in self._jdict.keys():
			return self._jdict["string"]
		elif "base" in self._jdict.keys():
			return self._jdict["base"]


class JsonSyllable(JsonNumberedElement):
	"""Represents the Syllable section of a Cruscopoetry poem serialized in JSON format."""
	
	PHONEME_CLASS = JsonPhoneme
	
	#since the syllables in cruscopoetry are highly customizable, we just store the dictionary.
	def __init__(self, index, jdict):
		super().__init__(index, jdict)
	
	def __str__(self):
		if "string" in self._jdict.keys():
			return self._jdict["string"]
		else:
			return ''.join((str(phoneme) for phoneme in self.iter_phonemes()))
			


class JsonWord(JsonNumberedElement):
	"""Represents the Word section of a Cruscopoetry poem serialized in JSON format."""

	SYLLABLE_CLASS = JsonSyllable
	PHONEME_CLASS = JsonPhoneme
	
	def __init__(self, index, jdict):
		super().__init__(index, jdict)

	@property
	def string(self):
		return self._jdict["string"]
	
	@string.setter
	def string(self, value):
		self._jdict["string"] = value


class JsonColon(JsonNumberedElement):
	"""Represents the Colon section of a Cruscopoetry poem serialized in JSON format."""

	WORD_CLASS = JsonWord
	SYLLABLE_CLASS = JsonSyllable
	PHONEME_CLASS = JsonPhoneme
	
	def __init__(self, index, jdict):

		if jdict["pwib"] == "true":
			jdict["pwib"] = True
		else:
			jdict["pwib"] = False

		if jdict["fwib"] == "true":
			jdict["fwib"] = True
		else:
			jdict["fwib"] = False

		super().__init__(index, jdict)

	@property
	def pwib(self):
		return self._jdict["pwib"]

	@property
	def fwib(self):
		return self._jdict["fwib"]

	@property
	def transcription(self):
		return self._jdict["transcription"]
	
	@transcription.setter
	def transcription(self, value):
		self._jdict["transcription"] = value
		
	@property
	def phonetics(self):
		return Joiners.WORDS.join(word.string for word in self.iter_words())
		
	@property
	def as_text(self):
		return self._compare(self.transcription, self.phonetics)
			
	def _compare(self, transcription, phonetics):
		ret_str = ""
		word_finder = re.compile("([\\w\\[\\]|]+)|([^\\w\\[\\]|])")
		tr_list = list(result for result in word_finder.findall(transcription))
		ph_tuple = tuple(result for result in word_finder.findall(phonetics) if result[0] != "")

		i = 0
		while i < len(ph_tuple):
			if tr_list[i][0] == "":
				ret_str += tr_list[i][1]
				tr_list.pop(i)
				continue

			if tr_list[i][0].lower() == ph_tuple[i][0]:
				ret_str += tr_list[i][0]

			elif re.sub("[\\[\\]|]", "", ph_tuple[i][0]) == tr_list[i][0]:
				ret_str += ph_tuple[i][0]

			else:
				ret_str += "<%s|%s>"%(tr_list[i][0], ph_tuple[i][0])

			i += 1
		return ret_str


class JsonLine(JsonNumberedElement):
	"""Represents the Line section of a Cruscopoetry poem serialized in JSON format.
	
	Args:
		index (int): the order index of the line within the element that has instantiated it
		jdict (dict): the JSON-serializable dictionary that represents the line
		translations (JsonTranslations): the translations of the poem
		stanza_offset (int): the offset of the stanza the line belongs to (the number of lines before it). Defaults to 0
	"""

	COLON_CLASS = JsonColon
	WORD_CLASS = JsonWord
	SYLLABLE_CLASS = JsonSyllable
	PHONEME_CLASS = JsonPhoneme
	
	def __init__(self, index, jdict, translations, stanza_offset: int = 0):
		super().__init__(index, jdict, translations)
		self._stanza_offset = stanza_offset

	@property
	def index_in_poem(self):
		return self.index + self._stanza_offset

	@property
	def number_in_poem(self):
		return self.index_in_poem + 1

	@property
	def label(self):
		return self._jdict["label"]
	
	@label.setter
	def label(self, value):
		self._jdict["label"] = value
		
	@property
	def transcription(self):
		ret_str = ""
		for colon in self.iter_cola():
			if colon.index != 0:
				if colon.pwib:
					ret_str += Joiners.WORD_INTERNAL_COLA_TRANSCRIPTION
				else:
					ret_str += Joiners.COLA_TRANSCRIPTION
			ret_str += colon.transcription
		return ret_str
		
	@property
	def as_text(self):
		ret_str = ""
		for colon in self.iter_cola():
			if colon.index != 0:
				if colon.pwib:
					ret_str += Joiners.WORD_INTERNAL_COLA
				else:
					ret_str += Joiners.COLA
			ret_str += colon.as_text
		return ret_str
		
	def get_translation_by_id(self, tr_id: str):
		translation = self._translations.get_translation_by_id(tr_id)
		translated_line = translation.get_line_translation(self)
		return translated_line

	def iter_stanzas_dict(self):
		"""For impossible iterations, we just yield from an empty list."""
		yield from []

	def iter_lines_dict(self):
		yield from []

	def iter_cola_dict(self):
		yield from self._jdict["cola"]


class JsonStanza(JsonNumberedElement):
	"""Represents the Stanza section of a Cruscopoetry poem serialized in JSON format.
	
	Args:
		index (int): the index of the stanza in the poem
		jdict (dict): the JSON-serializable dictionary representing the stanza
		translations (JsonTranslations): the JsonTranslations instance representing the translations of the poem
		offset (int): the number of lines that are before the stanza. Defaults to 0.
	"""

	LINE_CLASS = JsonLine
	COLON_CLASS = JsonColon
	WORD_CLASS = JsonWord
	SYLLABLE_CLASS = JsonSyllable
	PHONEME_CLASS = JsonPhoneme
	
	def __init__(self, index, jdict, translations, offset: int = 0):
		super().__init__(index, jdict, translations)
		self._offset = offset

	def iter_stanzas_dict(self):
		"""For impossible iterations, we just yield form an emtpy list."""
		yield from []

	def iter_lines_dict(self):
		yield from self._jdict["lines"]
		
	def iter_words_dict(self):
		for line in self.iter_lines():
			yield from line.iter_words_dict()

	@property
	def offset(self):
		return self._offset

	@property
	def as_text(self):
		return Joiners.LINES.join((line.as_text for line in self.iter_lines()))
		
	@property
	def transcription(self):
		return Joiners.LINES.join((line.transcription for line in self.iter_lines()))		


class JsonText(JsonElement):
	"""Represents the Text section of a Cruscopoetry poem serialized in JSON format."""

	STANZA_CLASS = JsonStanza
	LINE_CLASS = JsonLine
	COLON_CLASS = JsonColon
	WORD_CLASS = JsonWord
	SYLLABLE_CLASS = JsonSyllable
	PHONEME_CLASS = JsonPhoneme
	
	def __init__(self, jdict, translations):
		super().__init__(TreeDict(jdict), translations)

	#we needed to overwrite it since now super().iter_lines() passes self.offset as argument, and JsonText has no self.offset property
	def iter_lines(self):
		for index, line in enumerate(self.iter_lines_dict()):
			yield self.__class__.LINE_CLASS(index, line, self._translations)


	def get_line_by_number(self, number: int):
		"""Gets a line by its number (numbers start from 1). Returns None if no line is found."""
		for line in self.iter_lines():
			if line.number == number:
				return line
		return None

	def get_line_by_label(self, label: str):
		"""Gets a line by its label. Labels here must not include the $ start character. Returns None if no line is found."""
		for line in self.iter_lines():
			if line.label == label:
				return line
		return None
		
	def iter_words_dict(self):
		for stanza in self.iter_stanzas():
			yield from stanza.iter_words_dict()
		
	@property
	def as_text(self):
		return "TEXT\n" + Joiners.STANZAS.join((stanza.as_text for stanza in self.iter_stanzas()))
		
	@property
	def labels_to_indexes_dict(self) -> dict:
		"""Returns a dictionary where each line's label, if exists, is mapped to the line's index(integers starting from 0)."""
		ret_dict = {line.label: line.index for line in self.iter_lines() if line.label != None}
		return ret_dict

	def print_warning(self, message):
		print("\033[1;33;40mWarning\033[m. " + message)
