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
from .exceptions import *


class BaseParser:
	"""Base class for all the parsers of the module. This class controls if the file to parse exists and, if not, raises an Exception. Inheriting classes implement the actual parsing.
	
	Args:
		path (str): the path of the file to be parsed.
		
	Raises:
		InvalidPathError: raised if the file doesn't exist or is a directory.
	"""
	
	def __init__(self, path):
		if (not os.path.exists(path) or os.path.isdir(path)):
			raise InvalidPathError
		self.path: str = path

	
