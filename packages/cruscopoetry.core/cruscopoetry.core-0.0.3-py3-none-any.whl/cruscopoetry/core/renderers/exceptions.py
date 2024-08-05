#    This file is part of Cruscopoetry.
#
#    Cruscopoetry is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Cruscopoetry is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Cruscopoetry.  If not, see <http://www.gnu.org/licenses/>.


class RenderingException(Exception):
	"""Base class for the exceptions raised during rendering"""
	
	def __init__(self):
		super().__init__()	

class MissingTranslationError(RenderingException):
	"""Raised when one tries to render a poem with a translation that is not in the Json file"""
	
	def __init__(self, translation_id, poem_title):
		super().__init__()
		self.translation_id = translation_id
		self.poem_title = poem_title
	
	def __str__(self):
		return "The poem '%s' contains no translation with id '%s'"%(self.poem_title, self.translation_id)
