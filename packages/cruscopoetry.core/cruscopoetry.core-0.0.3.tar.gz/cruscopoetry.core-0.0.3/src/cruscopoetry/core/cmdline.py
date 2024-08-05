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
from .poemparser import poem_parser as parser
from .jsonparser import json_parser as jparser
from .translationparser import translation_parser as tparser
from .syllabification.handler import Handler
from .renderers import TextRenderer, HtmlRenderer
from . import project
import argparse
import sys


class CommandLine:

	_PARSER_CLASS = parser.Poem
	_JSON_PARSER_CLASS = jparser.JsonParser
	
	@classmethod
	def _build_parser(cls):
		parser = argparse.ArgumentParser(prog="CruscoPoetry")
		subparsers = parser.add_subparsers(help="the operation to perform", dest="operation")
		build_json = subparsers.add_parser("build", help="Parses a text in cruscopoetry format and builds a json file from it.")
		build_json.add_argument("-i", "--input", type=str, help="The file path of the poem")
		build_json.add_argument("-o", "--output", type=str, help="The file path to save the json representation on")
		build_json.add_argument("-v", "--verbose", action="store_true", help="set for more verbose output")
		build_json.set_defaults(feature=False)
		add_translation = subparsers.add_parser("add_translations", help="add one or more translations to a json file representing a poem.")
		add_translation.add_argument("-s", "--source", type=str, help="the JSON file with the poem in source language")
		add_translation.add_argument("-t", "--translations", type=str, nargs="+", help="the txt translation files, written in Cruscopoetry format.")
		delete_translation = subparsers.add_parser("delete_translations", help="deletes one or more translations from a json file representing a poem.")
		delete_translation.add_argument("-s", "--source", type=str, help="the JSON file with the poem in source language")
		delete_translation.add_argument("-t", "--translation_ids", nargs="+", type=str, help="the ids of the translations to delete.")
		list_translations = subparsers.add_parser("list_translations", help="lists the id of all the translations inserted in a CruscoPoetry json file.")
		list_translations.add_argument("json_file", type=str, help="the json file whose translations shall be listed.")

		render = subparsers.add_parser("render", help="prints or saves on file the poem as plain text")
		render_subparsers = render.add_subparsers(help="the rendering format", dest="format")
		txtrender = render_subparsers.add_parser("txt", help="plain-text renderer")
		txtrender.add_argument("--indent", type=str, default="  ", help="the indent string to be used in the txt file.")
		txtrender.add_argument("-i", "--input", help="the JSON file to render as text")
		txtrender.add_argument("--tr_id", type=str, default=None, help="the id of the translation to include in the text file.")
		txtrender.add_argument(
			"--tr_layout", type=int, choices=[0, 1, 2, 3, 4], default=None, 
			help="the translation layout: 0 for no translation, 1 for the whole translation after text, 2 after each stanza, 3 after each line, 4 for source and translation next together in one line."
		)
		txtrender.add_argument("--number_after", type=int, default=None, help="the number whose lines have one of its multiples as number will display their number.")
		txtrender.add_argument("-o", "--output", help="the file to save the rendering in (if not specified, it will be printed on stdout.")
		htmlrender = render_subparsers.add_parser("html", help="html renderer")
		htmlrender.add_argument("-i", "--input", help="the JSON file to render as text")
		htmlrender.add_argument("--tr_id", type=str, default=None, help="the id of the translation to include in the text file.")
		htmlrender.add_argument(
			"--tr_layout", type=int, choices=[0, 1, 2, 3, 4], default=None, 
			help="the translation layout: 0 for no translation, 1 for the whole translation after text, 2 after each stanza, 3 after each line, 4 for source and translation next together in one line."
		)
		htmlrender.add_argument("--pretty_print", action="store_true", help="pretty-print output option.")
		htmlrender.add_argument("--number_after", type=int, default=None, help="the number whose lines have one of its multiples as number will display their number.")
		htmlrender.add_argument("-o", "--output", help="the file to save the rendering in (if not specified, it will be printed on stdout.")
		return parser		
	
	@classmethod
	def main(cls):
		parser = cls._build_parser()
		args = parser.parse_args()
		if args.operation == "build":
			#if the output file is not specified, we take the name of the input file and change its suffix to json:
			if args.output != None:
				outfile = args.output
			else:
				outfile = ''.join(args.input.split('.')[:-1]) + '.json'
			cls.build_poem(args.input, outfile, args.verbose)
		elif args.operation == "add_translations":
			for translation in args.translations:
				cls.add_translation(args.source, translation)
		elif args.operation == "delete_translations":
			for translation in args.translation_ids:
				cls.delete_translation(args.source, translation)
		elif args.operation == "list_translations":
			cls.list_translations(args.json_file)
		elif args.operation == "render":
			indent = args.indent if args.format == "txt" else None
			pretty_print = args.pretty_print if args.format == "html" else None
			cls.render(args.format, args.input, args.output, args.tr_id, args.tr_layout, args.number_after, indent, pretty_print)

	@classmethod
	def build_poem(cls, infile: str, outfile: str, is_verbose: bool):
		poem = cls._PARSER_CLASS(infile)
		langcode = poem.metadata.fields["language"].lower()
		poem.deploy(outfile)
		handler = Handler(is_verbose)
		syllabifier = handler.get(langcode)
		if syllabifier != None:
			syllabifier.Main.syllabify_file(outfile)

	@classmethod
	def render(cls, file_format, infile, outfile, translation_id, translation_arrangement, number_after, indent, pretty_print):
		if file_format == 'txt':
			renderer = TextRenderer(infile)
			text = renderer.render(translation_id, translation_arrangement, indent, number_after)
		elif file_format == 'html':
			renderer = HtmlRenderer(infile)
			text = renderer.render(translation_id, translation_arrangement, number_after, pretty_print)
		else:
			return
		if outfile == None:
			print(text)
		else:
			with open(outfile, 'w') as out:		
				print(text, file=out)
	
	@classmethod
	def add_translation(cls, json_file, translation_file):
		j_object = cls._JSON_PARSER_CLASS(json_file)
		j_object.add_translation(translation_file)
		j_object.save()
		print("Translation successfully added")
		
	
	@classmethod
	def delete_translation(cls, json_file, translation_id):
		print("searching '%s'..."%translation_id)
		j_object = cls._JSON_PARSER_CLASS(json_file)
		success = j_object.delete_translation(translation_id)
		if success:
			j_object.save()
			print("Translation successfully deleted")
		else:
			print("No translation with id '%s' found"%translation_id)

	@classmethod
	def list_translations(cls, json_file: str):
		j_object = cls._JSON_PARSER_CLASS(json_file)
		translations = j_object.list_translations()
		print("Translations in '%s':"%j_object.title)
		print("\tlanguage\tid")
		for id, language in translations:
			print("\t%s\t\t%s"%(language, id))
	
