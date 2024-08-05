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
import re
from .exceptions import *

class Transcription:
	"""This class represents the parsing of a transcription syntax inline block in Cruscopoetry format. It raises a :class:`TranscriptionSyntaxError` if the syntax of the parsed block is not correct.
	There is generally no need to initialize directly an instance of this class. Rather, the class method :method:`parse_colon` can be used to obtain directly the parsing of a colon.
	
	Args:
		transcription (tuple): a tuple of the values resulted from the tokenization of a transcription block.
		
	Methods:
		parse_colon: a class method. Takes as argument a string representing a colon and returns a pair of strings, one with its transcription, one with its representation.
	"""

	HEAD_REGEX = re.compile("^(?P<head>[^<]*)(?P<rest>.*)$")

	TRANSCRIPTION_REGEX = re.compile(
			"(?P<start_transcription><)" + 
				"(?P<transcription>([^\\[\\]|<>]+)|(\\[[^\\[\\]<>]+\\]))" +
				"(?P<middle_bar>\\|)?" + 
				"(?P<phonetics>([^\\[\\]|<>]+)|(\\[[^\\[\\]<>]+\\]))" +
			"(?P<end_transcription>>)?" + 
			"(?P<tail>[^<]*)" 
	)

	def __init__(self, transcription: tuple):
		self.start_transcription = transcription[0]
		self.transcription = transcription[1]
		self.middle_bar = transcription[4]
		self.phonetics = transcription[5]
		self.end_transcription = transcription[8]
		self.tail = transcription[9]
		
		if (self.start_transcription != "" and (self.middle_bar == "" or self.end_transcription == "")):
			raise TranscriptionSyntaxError(self.__repr__())
		
	@classmethod
	def parse_colon(cls, colon_string: str) -> tuple:
		"""This method parses the colon string a returns a pair of tuples, the first corresponding to its transcription, the second to its phonetics.
		
		Args:
			colon_string (str): The string of the colon to be parsed.
		
		Returns:
			transcription (str): the transcription of the colon as written in the source.
			phonetics (str): the phonetic transcription of the colon, of use for further parsing.
		
		Raises:
			TranscriptionSyntaxError: raised if the transcription syntax is not correct.
		"""

		transcription, phonetics = "", ""

		#first, we yield the head of the colon using HEAD_REGEX:
		head_match = cls.HEAD_REGEX.match(colon_string)
		head, rest = head_match.group("head"), head_match.group("rest")
		transcription += head
		phonetics += head
		
		#then, we parse the rest of the verse:
		other_portions = tuple(cls.TRANSCRIPTION_REGEX.findall(rest))
		
		#if other_portions has 0 items but rest is different from '', then something is wrong in the transcription and we raise an error:
		if (len(other_portions) == 0 and rest != ""):
			raise TranscriptionSyntaxError(rest)
		for parsed in other_portions:
			result = cls(parsed)
			transcription += result.transcription + result.tail
			phonetics += result.phonetics + result.tail
		return transcription, phonetics
			
	@property
	def verbose(self):
	 	return """transcription = '%s'
transcription = '%s'
middle_bar = '%s'
phonetics = '%s'
end_transcription = '%s'
tail = '%s'"""%(self.start_transcription, self.transcription, self.middle_bar, self.phonetics, self.end_transcription, self.tail)
			
	def __repr__(self):
		return "%s%s%s%s%s%s"%(self.start_transcription, self.transcription, self.middle_bar, self.phonetics, self.end_transcription, self.tail)
