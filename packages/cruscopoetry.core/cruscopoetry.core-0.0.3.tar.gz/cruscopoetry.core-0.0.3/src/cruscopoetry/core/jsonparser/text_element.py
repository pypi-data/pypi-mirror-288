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


class JsonElement:
	"""Base class for all the element classes used in JSON parsing. This class provides the iterator methods, the initialization of the jdict attribute and the json_dict method."""
	
	def __init__(self, jdict, translations = None):
		self._jdict = jdict
		self._translations = translations

	#differently from the case of the txt parser, in this case we don't initialize all the sections, but we go lazy: we provide the class with iterator functions, that instantiate any element of the 
	#poem (stanza, line, cola, word, syllable, phoneme) with its corresponding class.
	
	#we code two series of iterator; the first yields only the dicts corresponding to the various elements of the poem;
	#the second yields objects built on the dicts of the first series, which contain also an progressive integer corresponding to their position in the text (es. stanza_number, verse_number...)

	STANZA_CLASS = None
	LINE_CLASS = None
	COLON_CLASS = None
	WORD_CLASS = None
	SYLLABLE_CLASS = None
	PHONEME_CLASS = None

	def iter_stanzas_dict(self):
		for array in self._jdict.iter("stanzas"):
			yield from array

	def count_stanzas(self):
		counter = 0
		for stanza in self.iter_stanzas_dict():
			counter += 1
		return counter
		
	def iter_lines_dict(self):
		for array in self._jdict.iter("lines"):
			yield from array

	def count_lines(self):
		counter = 0
		for line in self.iter_lines_dict():
			counter += 1
		return counter
		
	def iter_cola_dict(self):
		for array in self._jdict.iter("cola"):
			yield from array

	def count_cola(self):
		counter = 0
		for colon in self.iter_cola_dict():
			counter += 1
		return counter

	def _words_iterator_split_on_boundaries(self):
		for array in self._jdict.iter("words"):
			yield from array
			
	def _merge(self, sections: list):
		"""Takes a list containing the sections of a word split by word-internal colon boundaries, empties it returns the word resulting from the merging of all the sections:"""
		new_word = {"string": "", "syllables": []}
		while len(sections) > 0:
			section = sections.pop(0)
			new_word["string"] += section["string"]
			new_word["syllables"].append(section["syllables"])
		return new_word
	
	def _words_iterator_merge_on_boundaries(self):
		word_sections = []
		for colon in self.iter_cola_dict():
		
			cola_count = len(colon["words"])

			#first we deal with the particular case of cola_count == 1:
			if cola_count == 1:
				if (colon["pwib"] and colon["fwib"]):
					word_sections.append(colon["words"][0])

				elif colon["pwib"] and (not colon["fwib"]):
					word_sections.append(colon["words"][0])
					yield self._merge(word_sections)

				elif colon["fwib"] and (not colon["pwib"]):
					word_sections.append(colon["words"][0])
				else:
					yield colon["words"][0]
	
			
			#else we iterate over all the words in colon, paying particular attention to colon["words"][0] and colon["words"][-1]:
			else:
				for i in range(cola_count):

					#if i == 0, if colon["pwib"] == False, we yield the word, else we append it to word_sections and then yield its merging: 
					if i == 0:
						if not colon["pwib"]:
							yield colon["words"][i]
						else:
							word_sections.append(colon["words"][i])
							yield self._merge(word_sections)

					#elif i == cola_count-1, if colon["fwib"] == False, we yield the word, else we append it to word_sections:
					elif i == (cola_count-1):
						if not colon["fwib"]:
							yield colon["words"][i]
						else:
							word_sections.append(colon["words"][i])

					#in the other cases we simply yield:
					else:
						yield colon["words"][i]
				
	def iter_words_dict(self):
		#if self.__class__.COLON_CLASS == None, then the class represents a colon or something lower in the hierarchy and so we just yield the words as they are:
		if self.__class__.COLON_CLASS == None:
			yield from self._words_iterator_split_on_boundaries()
		
		#else, we have to compound the sections of a word split by word-internal caesurae as one only word and yield it:
		else:
			yield from self._words_iterator_merge_on_boundaries()

	def count_words(self):
		counter = 0
		for word in self.iter_words_dict():
			counter += 1
		return counter
							
	def iter_syllables_dict(self):
		for array in self._jdict.iter("syllables"):
			yield from array

	def count_syllables(self):
		counter = 0
		for syllable in self.iter_syllables_dict():
			counter += 1
		return counter
	
	def iter_phonemes_dict(self):
		for array in self._jdict.iter("phonemes"):
			yield from array

	def count_phonemes(self):
		counter = 0
		for phoneme in self.iter_phonemes_dict():
			counter += 1
		return counter
	
	def iter_stanzas(self):
		offset = 0 #the number of lines before the stanza that will be yielded. This value will be useful to get, in the stanza istance, the number of each line IN the poem
		for index, stanza in enumerate(self.iter_stanzas_dict()):
			new_stanza = self.__class__.STANZA_CLASS(index, stanza, self._translations, offset)
			offset += new_stanza.count_lines()
			yield new_stanza
	
	def iter_lines(self):
		for index, line in enumerate(self.iter_lines_dict()):
			yield self.__class__.LINE_CLASS(index, line, self._translations, self.offset)
	
	def iter_cola(self):
		for index, colon in enumerate(self.iter_cola_dict()):
			yield self.__class__.COLON_CLASS(index, colon)
	
	def iter_words(self):
		for index, word in enumerate(self.iter_words_dict()):
			yield self.__class__.WORD_CLASS(index, word)
	
	def iter_syllables(self):
		for index, syllable in enumerate(self.iter_syllables_dict()):
			yield self.__class__.SYLLABLE_CLASS(index, syllable)
	
	def iter_phonemes(self):
		for index, phoneme in enumerate(self.iter_phonemes_dict()):
			yield self.__class__.PHONEME_CLASS(index, phoneme)

#############################


	def get_first_stanza_dict(self):
		for array in self._jdict.iter("stanzas"):
			return array[0]
		
	def get_first_line_dict(self):
		for array in self._jdict.iter("lines"):
			return array[0]
		
	def get_first_colon_dict(self):
		for array in self._jdict.iter("cola"):
			return array[0]

	def get_first_word_dict(self):
		for array in self._jdict.iter("words"):
			return array[0]
							
	def get_first_syllable_dict(self):
		for array in self._jdict.iter("syllables"):
			return array[0]
	
	def get_first_phoneme_dict(self):
		for array in self._jdict.iter("phonemes"):
			return array[0]
	
	def get_first_stanza(self):
		for index, stanza in enumerate(self.iter_stanzas_dict()):
			return self.__class__.STANZA_CLASS(index, stanza)
	
	def get_first_line(self):
		for index, stanza in enumerate(self.iter_lines_dict()):
			return self.__class__.LINE_CLASS(index, stanza)
	
	def get_first_colon(self):
		for index, stanza in enumerate(self.iter_cola_dict()):
			return self.__class__.COLON_CLASS(index, stanza)
	
	def get_first_word(self):
		for index, stanza in enumerate(self.iter_words_dict()):
			return self.__class__.WORD_CLASS(index, stanza)
	
	def get_first_syllable(self):
		for index, stanza in enumerate(self.iter_syllables_dict()):
			return self.__class__.SYLLABLE_CLASS(index, stanza)
	
	def get_first_phonemes(self):
		for index, phoneme in enumerate(self.iter_phonemes_dict()):
			return self.__class__.PHONEME_CLASS(index, phoneme)


#############################

	def json_dict(self):
		return self._jdict
		
	def __repr__(self):
		return "%s (%r)"%(self.__class__.__name__, self._jdict.keys())


class JsonNumberedElement(JsonElement):
	"""Represents all those elements that occur more than once in a poem and in a definite order, and can therefore be numerated.
	Two attributes of this class represent the position of the element: index (progressive element starting from 0) and number (progressive element starting from 1).
	"""
	
	def __init__(self, index, jdict, translations = None):
		super().__init__(jdict)
		self.index = index
		self._translations = translations
	
	@property
	def number(self):
		return self.index+1
		
	def __repr__(self):
		return "%s-%d(%r)"%(self.__class__.__name__, self.number, list(self._jdict.keys()))
