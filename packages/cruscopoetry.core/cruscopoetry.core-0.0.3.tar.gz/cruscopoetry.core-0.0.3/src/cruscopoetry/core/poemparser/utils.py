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
import abc


class Singleton(type):

	_instance = None
	
	def __call__(cls, *args, **kwargs):
		if cls._instance == None:
			cls._instance = super().__call__(*args, **kwargs)
		return cls._instance		


class Validator(metaclass=Singleton):

	def __init__(self):
		self._label_validator = re.compile("\\$\\w+")

	def is_valid_label(self, string: str):
		return self._label_validator.fullmatch(string) != None



class AbstractSingleton(abc.ABCMeta):

	_instance = None
	
	def __call__(cls, *args, **kwargs):
		if cls._instance == None:
			cls._instance = super().__call__(*args, **kwargs)
		return cls._instance

