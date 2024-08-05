# This file is part of CruscoPoetry.
# 
# CruscoPoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CruscoPoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CruscoPoetry. If not, see <http://www.gnu.org/licenses/>.
import mum
import importlib
import subprocess
import os, sys


class Handler(metaclass=mum.Singleton):
	"""Handles the dynamic importing of the syllabifier modules. This class is a Singleton.
	"""
	
	def __init__(self, verbose = False):
		self.namespace = "cruscopoetry.syllabifiers"
		self.verbose = verbose

	@property
	def log_path(self):
		return os.path.join(os.path.dirname(os.path.abspath(__file__)), "importer.log")

	def package_name(self, langcode: str):
		return '.'.join((self.namespace, langcode))

	def _print_logs(self):
		with open(self.log_path, 'r') as logfile:
			print("\u001b[0;31m" + logfile.read() + "\u001b[0m")

	def _get_from_pypi(self, langcode: str):
		"""Installs a package from PyPi. Returns True/False if it has succeeded or not."""
		
		try:
			with open(self.log_path, 'w') as err_str: 
				subprocess.run([sys.executable, "-m", "pip", "install", "-U", self.package_name(langcode)], stdout=subprocess.DEVNULL, stderr=err_str, check= True)
				return True
		except subprocess.CalledProcessError:
			if self.verbose == True:
				self._print_logs()
			return False
		except Exception as e:
			print("\u001b[1;31mOops! Something got wrong\u001b[0m")
			print("Log file content:")
			self._print_logs()
			raise e
			return False

	def _get_from_local(self, langcode: str):
		"""Tries to import the module from sys.path, and returns it if it has been found, else None"""
		try:
			print("\u001b[1;32mLooking for '%s'\u001b[0m"%self.package_name(langcode))
			return importlib.import_module(self.package_name(langcode))
		except ModuleNotFoundError:
			return None
		
	def get(self, langcode: str):
		"""Imports the syllabifier module corresponding to the ISO639-3 language code and returns the module object
		
		Args:
			langcode (str): the langcode whose syllabifier will be imported.
		"""
		print("'%s'"%langcode)
		syllabifier = self._get_from_local(langcode)
		if syllabifier != None:
			print("\u001b[1;32mSyllabifier found!\u001b[0m")
			return syllabifier
		else:
			print("\u001b[1;33mSyllabifier not found. Searching it on PyPi...\u001b[0m")
			success = self._get_from_pypi(langcode)
			if success:
				syllabifier = self._get_from_local(langcode)
				print("\u001b[1;32mSyllabifier found on PyPi!\u001b[0m")
			else:
				print("\u001b[1;31mNothing found.\u001b[0m\nSorry, we have not yet coded it. If you have customized a syllabifier for your language (%s) please let us know!"%langcode)
		return syllabifier

