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
from ..exceptions import RenderingException
from .translation_arrangement import TranslationArrangement


class DisposerException(RenderingException):

	def __init__(self, arrangement: TranslationArrangement):
		super().__init__()
		self._arrangement = arrangement
	
	def __str__(self):
		return "This rendered doesn't support the translation arrangement '%s'"%self._arrangement.name


class LineNumberingError(RenderingException):

	def __init__(self):
		super().__init__()
	
	def __str__(self):
		return "The `number` property of AbstractLineRenderer instances can be set only once."
