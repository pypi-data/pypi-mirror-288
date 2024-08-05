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
from .resources_browser import *
from pathlib import Path
from typing import Tuple
from ..poemparser import poem_parser
from ..translationparser import translation_parser
from .. import jsonparser
from ..syllabification.handler import Handler
from .. import renderers
from .exceptions import *


class ProjectManager:

	def __init__(self, project_path: str, output_path: str = None):
		self._path = project_path if isinstance(project_path, Path) else Path(project_path)
		if not self._path.exists():
			raise InexistentPathException(self._path)
		self._output = self._path.parent
		if output_path != None:
			output = output_path if isinstance(output_path, Path) else Path(output_path)
			if output.exists():
				self._output = output
				
		self._res_browser = self.build_resources_browser()
		
	def build_resources_browser(self):
		if self._path.is_dir():
			return DirResourcesBrowser(self._path)
		else:
			raise WrongProjectFormat(self._path)

	@property
	def name(self):
		return self._path.stem

	@property
	def source(self) -> poem_parser.Poem:
		return self._res_browser.get_source()
	
	@property
	def translations(self) -> translation_parser.TranslationParser:
		return self._res_browser.get_translations()
	
	@property
	def json_path(self) -> str:
		return self._res_browser.json_path
	
	@property
	def json_parser(self) -> jsonparser.JsonParser:
		return self._res_browser.json_parser
		
	def compile(self, verbose: bool = False):
		self.source.deploy(self._res_browser.json_path)

		langcode = self.source.metadata.fields["language"]
		handler = Handler(False)
		syllabifier = handler.get(langcode)
		if syllabifier != None:
			syllabifier.Main.syllabify_file(self.json_path)

		if verbose:
			print("\u001b[1;33mAdding translations...\u001b[0m")

		for translation in self.translations:
			self.json_parser.add_translation(translation)

		if verbose:
			print("\u001b[1;33mSaving...\u001b[0m")
		self.json_parser.save()

		if verbose:
			print("\u001b[1;32mSaved\u001b[0m")

	def list_translations(self):
		if self.json_parser != None:
			return self.json_parser.list_translations()
		raise ProjectNotBuiltException(self._path)

	def has_translation(self, tr_id: str):
		if self.json_parser != None:
			return self.json_parser.has_translation(tr_id)
		raise ProjectNotBuiltException(self._path)

	def render_txt(self, translation_id: str, translation_arrangement: renderers.TranslationArrangement, number_after: int = None, indent: str = None):
		if indent == None:
			indent = " "*2
		renderer = renderers.TextRenderer(self.json_parser)
		text = renderer.render(translation_id, translation_arrangement, indent, number_after)
		file_name = self.name + "_rendering_%s_%s.txt"%(translation_id, translation_arrangement.name)
		output_path = str(self._output.joinpath(file_name))
		with open(output_path, 'w') as outfile:
			outfile.write(text)


	def render_html(self, translation_id: str, translation_arrangement: renderers.TranslationArrangement, number_after: int = None, pretty_print: bool = None):
		renderer = renderers.HtmlRenderer(self.json_parser)
		text = renderer.render(translation_id, translation_arrangement, number_after, pretty_print)
		file_name = self.name + "_rendering_%s_%s.html"%(translation_id, translation_arrangement.name)
		output_path = str(self._output.joinpath(file_name))
		with open(output_path, 'w') as outfile:
			outfile.write(text)

	
