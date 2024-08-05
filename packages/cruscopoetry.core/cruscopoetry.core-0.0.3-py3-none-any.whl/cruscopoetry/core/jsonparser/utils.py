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
from typing import Tuple, List
from .exceptions import MandatoryFieldError, InvalidLanguageError, InvalidCountryError, InvalidScriptError, InvariableFieldError
import pycountry
from .joiners import Joiners


class Requirement:

	def __init__(self, field, is_mandatory: bool, is_variable: bool, control: int):
		self.field = field
		self.is_mandatory = is_mandatory
		self.is_variable = is_variable
		self.control = control


class MetadataValidator:
	"""Validates the attempts of setting or deleting new values from a MetadataDict. This class is initialized with a list of requirements. Each requirement is on its turn a tuple of four values: 
	
	 - a string containing the field's name;
	 - a boolean value indicating if the value is mandatory in the dictionary (and thus non-deletable) or not;
	 - a boolean value indicating if the value can be changed after after it has been inserted in the dictionary or not;
	 - an integer specifying which kind of control must be done.
	In particular:
	
		- 0 is for no control;
		- 1 is for language control (the value must be a valid ISO639-3 code;
		- 2 is for country control (the value must be a valid ISO3166 alpha-3 code;
		- 3 is for script control (the value must be a valid ISO15924 alpha-4 code.
	
	Args:
		requirements (list): a list with all the requirements.
	
	Attrs:
		requirements (list): a list with all the requirements.

	Methods:
		validate: validates a value that must be set in the dictionary for a given key
	"""

	NO_CONTROL = 0
	LANGUAGE = 1
	COUNTRY = 2
	SCRIPT = 3

	def __init__(self, requirements: List[Tuple[str, bool, bool, int]]):
		self.requirements = [Requirement(*requirement) for requirement in requirements]
		
	def add_requirement(requirement: Tuple[str, bool, bool, int]):
		"""Adds a new requirement. If another requirement with the same field name already existed, deletes it and puts the new one at its place."""
		new_requirement = Requirement(*requirement)
		self.remove_requirement(new_requirement.field)
		self.requirements.append(new_requirement)
		
	def remove_requirement(field_name: str):
		"""Removes the requirement referring to the field ``field_name``, if exists. If it doesn't, nothing happens."""
		requirement = self._find_requirement(field_name)
		if requirement != None:
			self.requirements.remove(requirement)
		
	def is_valid_language(self, langcode):				
		language = pycountry.languages.get(alpha_3=langcode)
		return language != None
			
	def is_valid_country(self, countrycode):				
		country = pycountry.countries.get(alpha_3=countrycode)
		return country != None

	def is_valid_script(self, scriptcode):				
		script = pycountry.scripts.get(alpha_4=scriptcode)
		return script != None

	def _find_requirement(self, key):
		"""Returns a requirement for a given key, if it exists, else returns None"""
		for requirement in self.requirements:
			if requirement.field == key:
				return requirement
		return None
	
	def validate_setting(self, key, value, is_new: bool = False, old_value= None):
		"""Checks if :parameter:`value` can be set as value for :parameter:`key`. If the instance contains no requirement whose field name is `key`, the validation will return None.
		The same happens if a requirement exists and it is respected. If instead it is not, this method will raise an exception.
		
		Args:
			key: the key which the new value must be assigned to
			value: the value that must be validated
			new_element (bool): default is False. True if the item with key `key` did not exist in the dictionary before this setting attempt.
		
		Raises:
			InvalidLanguageError: if one attempts to set a language field with an invalid ISO639-3 code;
			InvalidCountryError: if one attempts to set a country field with an invalid ISO3166 alpha-3 code;
			InvalidScriptError: if one attempts to set a script field with an invalid ISO15924 alpha-4 code;
		"""
		requirement = self._find_requirement(key)
		if requirement != None:
			if not (is_new or requirement.is_variable):
				if value != old_value:
					raise InvariableFieldError(key)
			if requirement.control == self.__class__.LANGUAGE:
				if not self.is_valid_language(value):
					raise InvalidLanguageError(value)
			if requirement.control == self.__class__.COUNTRY:
				if not self.is_valid_country(value):
					raise InvalidCountryError(value)
			if requirement.control == self.__class__.SCRIPT:
				if not self.is_valid_script(value):
					raise InvalidScriptError(value)
		return None
	
	def validate_deleting(self, key):
		"""Checks if :parameter:`key` can be deleted. If the instance contains no requirement whose field name is `key`, the validation will return None.
		The same happens if a requirement exists, but the field is not indicated as mandatory. If instead it is, a MandatoryFieldError will be raised.
		
		Args:
			key: the key of the item that must be deleted
		
		Raises:
			MandatoryFieldError: if one attempts to delete a mandatory field;
		"""
		requirement = self._find_requirement(key)
		if requirement != None:
			if requirement.is_mandatory == True:
				raise MandatoryFieldError(key)
	
	


class MetadataDict:
	"""Handles the metadata section of a CruscoPoetry json file as if it is a dictionary; moreover, it checks that the mandatory fields are never deleted and that each attempt of setting a new value
	on a field that requires a code goes through a proper validation.
	
	Args:
		validator (MetadataValidator): it is the object that controls the setting and deleting instructions on the dictionary.
	
	Attrs:
		validator (MetadataValidator): it is the object that controls the setting and deleting instructions on the dictionary.
	"""
	
	def __init__(self, dictionary, validator):

		#if the values in the dictionary are invalid initialisation will be interrupted:
		for key, value in dictionary.items():
			validator.validate_setting(key, value, True)
		self.dict = dictionary
		self.validator = validator

	def __len__(self):
		return len(self.dict)

	def __getitem__(self, key):
		return self.dict.__getitem__(key)
		
	def __setitem__(self, key, value):
		is_new = key not in self.keys()
		old_value = None
		if not is_new:
			old_value = self.dict.__getitem__(key)
		self.validator.validate_setting(key, value, is_new, old_value)
		#if no exception has been raised, we will just call the super() method
		self.dict.__setitem__(key, value)
		
	def has_key(key) -> bool:
		return self.dict.has_key(key)

	def __delitem__(self, key):
		self.validator.validate_deleting(key)
		#if no exception has been raised, we will just call the super() method
		self.dict.__delitem__(key)
	
	def keys(self):
		return self.dict.keys()
		
	def is_mandatory(self, key) -> bool:
		"""Returns True if a key is mandatory, False otherwise"""
		requirement = self.validator._find_requirement(key)
		if requirement == None:
			return False
		else:
			return requirement.is_mandatory
		
	def is_variable(self, key) -> bool:
		"""Returns True if a key is variable, False otherwise"""
		requirement = self.validator._find_requirement(key)
		if requirement == None:
			return True
		else:
			return requirement.is_variable

	def mandatory_keys(self):
		mand_dict = {key: value for key, value in self.items() if self.is_mandatory(key)}
		return mand_dict.keys()

	def mandatory_values(self):
		mand_dict = {key: value for key, value in self.items() if self.is_mandatory(key)}
		return mand_dict.values()

	def mandatory_items(self):
		mand_dict = {key: value for key, value in self.items() if self.is_mandatory(key)}
		return mand_dict.items()

	def optional_keys(self):
		opt_dict = {key: value for key, value in self.items() if not self.is_mandatory(key)}
		return opt_dict.keys()

	def optional_values(self):
		opt_dict = {key: value for key, value in self.items() if not self.is_mandatory(key)}
		return opt_dict.values()

	def optional_items(self):
		opt_dict = {key: value for key, value in self.items() if not self.is_mandatory(key)}
		return opt_dict.items()

	
	def values(self):
		return self.dict.values()
	
	def items(self):
		return self.dict.items()
	
	def __iter__(self):
		return iter(self.dict)
		
	def update(self, other_dict: dict):
		"""Similar to dict.update(other_dict). The new items will undergo no validation, unless a requirement for them is already in the class. Validations must be added or removed separatedly."""
		for key, value in other_dict.items():
			is_new = key not in self.keys()
			old_value = self[key] if not is_new else None
			self.validator.validate_setting(key, value, is_new, old_value)
		self.dict.update(other_dict)

	@property
	def as_text(self):
		"""A plain text representation of the metadata (useful if one wants to build back the txt source file)"""
		fields = [Joiners.METADATA_FIELDS_INTERNAL.join(pair) for pair in self.items()]
		ret_string = Joiners.METADATA_FIELDS.join(fields)
		return ret_string
		

class TreeDict(dict):
	"""This class inherits from the dict built-in type. It is thought to represent tree-structures, such as JSON encodings. It provides an iter function, that goes through the dictionary yielding 
	from all the items with a given key (from any position in the tree structure)."""
	
	def __new__(self, *args, **kwargs):
		obj = dict.__new__(self, *args, **kwargs)
		return obj
	
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)
		for key, value in self.items():
			if type(value) == dict:
				value = self.__class__(value)
				self.__setitem__(key, value)
			elif self._is_array(value):
				self._init_in_array(value)

	def _init_in_array(self, array):
		"""Traverse the array, transforms any dict item in a TreeDict, and if an item is a nested array, calls itself recursively on it"""
		for i in range(len(array)):
			if type(array[i]) == dict:
				array[i] = self.__class__(array[i])
				
				
	def _is_array(self, obj):
		"""Checks if an object is an iterable, but not a dictionary or a string"""
		try:
			iterator = iter(obj)
			return ((isinstance(obj, dict) == False) and (isinstance(obj, str) == False))
		except TypeError:
			return False
				
	def _yield_from_array(self, array, key_name):
		"""Iterates through an array (an iterable which is not a dict) yielding all the items which equal value. If one of the items are arrays on their turn, it iterates over them as well"""
		for item in array:
			if self._is_array(item):
				yield from self._yield_from_array(item, key_name)
			elif isinstance(item, self.__class__):
				yield from item.iter(key_name)
	
	def iter(self, key_name: str):
		"""Iterates across the dictionary finding any field whose key is :parameter:`key_name`. If the corresponding value is not a number, a string, a boolean or a null value, it just yields it. If it 
		is an array, it yields from the array. If it is another TreeDict, it iterates from items() and then goes on iterating recursively
		from it"""
		for key, value in self.items():
			#if key equals key_name, we yield value:
			if key == key_name:
				yield value

			#if it isn't, but value is an array, we yield from it and from nested arrays the items with key = key_name
			if self._is_array(value):
				yield from self._yield_from_array(value, key_name)
			#if value is another TreeDict, we call iter(key_name) on it:

			if isinstance(value, self.__class__):
				yield from value.iter(key_name)

	def _count_from_array(self, value, key_name):
		ret_int = 0
		for item in value:
			if self._is_array(item):
				ret_int += self._count_from_array(item, key_name)
			if isinstance(item, self.__class__):
				ret_int += item.count(key_name)
		return ret_int
	
	def count(self, key_name: str):
		"""Returns the number of all the dictionary keys corresponding to key_name that are found among the element's children and descendant. The element itselfis not counted, even if its key is
		`key_name`."""
		ret_int = 0
		for key, value in self.items():
			if key == key_name:
				ret_int += 1

			if isinstance(value, self.__class__):
				ret_int += value.count(key_name)
			
			if self.is_array(value):
				ret_int += self._count_from_array(value, key_name)

		return ret_int

	def get_first(self, key_name:str):
		"""Iterates across the dictionary and returns the first field whose key is :parameter:`key_name`. If this field is not found, it returns None"""
		for value in self.iter(key_name):
			return value
		return None

	def __str__(self):
		return "TreeDict(%s)"%super().__str__()				
