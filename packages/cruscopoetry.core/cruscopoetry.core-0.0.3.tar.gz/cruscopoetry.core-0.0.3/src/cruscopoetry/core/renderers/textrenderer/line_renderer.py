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
from ...jsonparser import JsonText, JsonTranslations, JsonTranslation, JsonStanza, JsonLine, JsonColon
from ..abstractrenderer import AbstractLineRenderer
from .joiners import Joiners
	

class PlainTextColonRenderer:

	def __init__(self, jcolon: JsonColon):
		self.jcolon = jcolon

	def render(self) -> str:
		return self.jcolon.transcription


class PlainTextLineRenderer(AbstractLineRenderer):

	def __init__(self, jline: JsonLine, translation_id: int):
		super().__init__(jline, translation_id)
		

	def get_source(self):
		ret_str = ""
		for colon in self.jline.iter_cola():
			if colon.index != 0:
				if colon.pwib:
					ret_str += Joiners.COLON
				else:
					ret_str += " %s "%Joiners.COLON
			ret_str += colon.transcription
		return ret_str
	
	def get_translation(self):		
		return self.translation
	
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
