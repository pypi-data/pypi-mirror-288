# This file is part of CruscoPoetry.
# 
# CruscoPoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# CruscoPoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CruscoPoetry. If not, see <http://www.gnu.org/licenses/>.
from cruscopoetry.core.jsonparser import JsonParser
from cruscopoetry.plugins.abstract import AbstractPlugin
from .common import metric_elements
from .parser.text_parser import TextParser
from .renderer.text_renderer import CruscoArudHtmlRenderer
import argparse


class CruscoArud(AbstractPlugin):

	PLUGIN_NAME = "CruscoArud"
	PLUGIN_VERSION = "1.0.0"

	ELEMENTS = metric_elements.MetricElements()
	TEXT_PARSER_CLASS = TextParser
	TEXT_RENDERER_CLASS = CruscoArudHtmlRenderer
		
	@classmethod
	def get_meta_key(cls):
		return cls.ELEMENTS.configuration.json_fields["META_FIELD_NAME"]
		
	@classmethod
	def get_lines_key(cls):
		return cls.ELEMENTS.configuration.json_fields["LINES_FIELD_NAME"]

	@classmethod
	def _build_args_parser(cls):
		argparser = argparse.ArgumentParser(prog="CruscoArud")
		subparsers = argparser.add_subparsers(help="the operation to perform", dest="operation")

		parse_json = subparsers.add_parser("parse", help="Parses a json file from a text in cruscopoetry format and stores information about its *ʿarūḍ parsing*.")
		parse_json.add_argument("json_file", type=str, help="The file path of the poem")
		parse_json.add_argument("-v", "--verbose", action="store_true", help="more verbose output.")

		tables = subparsers.add_parser("tables", help="Prints in tabular format the Ḫalīlian metrical elements with their numerical values in decimal and hexadecimal format.")

		find_metre = subparsers.add_parser("find_metres", help="Finds the metre of a poem.")
		find_metre.add_argument("json_file", type=str, help="The file path of the poem")
		find_metre.add_argument("--for_each_line", action="store_true", help="add to view all the possible metric parsings for each line of the poem.")
		find_metre.add_argument("-v", "--verbose", action="store_true", help="more verbose output.")

		reset_json = subparsers.add_parser("reset", help="Deletes all the information previously stored by the CruscoArud plugin on a JSON file")
		reset_json.add_argument("json_file", type=str, help="The file path of the poem")

		render_json = subparsers.add_parser("render", help="Represents the metrical parsing in a human-readable way")
		render_json.add_argument("json_file", type=str, help="The file path of the poem")
		render_json.add_argument("--tr_id", type=str, default=None, help="the id of the translation to include in the text file.")
		render_json.add_argument(
			"--tr_layout", type=int, choices=[0, 1, 2, 3], default=None, 
			help="the translation layout: 0 for no translation, 1 for the whole translation after text, 2 after each stanza, 3 after each line."
		)
		render_json.add_argument("--pretty_print", action="store_true", help="pretty-print output option.")
		render_json.add_argument("--number_after", type=int, default=None, help="the number whose lines have one of its multiples as number will display their number.")
		render_json.add_argument("-o", "--output", help="the file to save the rendering in (if not specified, it will be printed on stdout.")

		return argparser
	
	@classmethod
	def main(cls):
		parser = cls._build_args_parser()
		args = parser.parse_args()
		if args.operation == "tables":
			cls.represent()
		elif args.operation == "parse":
			cls.parse(args.json_file, args.verbose)
		elif args.operation == "find_metres":
			if args.for_each_line:
				cls.find_metres_for_each_lines(args.json_file, args.verbose)
			else:
				cls.find_metres(args.json_file, args.verbose)
		elif args.operation == "reset":
			cls.reset(args.json_file)
		elif args.operation == "render":
			cls.render(args.json_file, args.output, args.tr_id, args.tr_layout, args.number_after, args.pretty_print)
		else:
			raise RuntimeError("Unrecognized operation: '%s'"%args.operation)

	@classmethod
	def build_parser(cls, json_file):
		return cls.TEXT_PARSER_CLASS(json_file, cls.ELEMENTS)

	@classmethod
	def build_renderer(cls, json_file):
		plugin_data = cls.get_data(json_file)
		if cls.get_lines_key() not in plugin_data:
			print("\u001b[1;31mNo metric parsing found. Please use the function parse() before rendering.\u001b[0m")
			return None
		return cls.TEXT_RENDERER_CLASS(json_file, plugin_data, cls.ELEMENTS)

	@classmethod
	def represent(cls):
		print(cls.ELEMENTS.configuration)
	
	@classmethod
	def parse(cls, json_file: str, verbose: bool = False):
	
		metre_parser = cls.build_parser(json_file)
		#first we check if the metre has already been detected; otherwise, we ask the user to do that
		data = cls.get_data(metre_parser.jpoem)
		if cls.get_meta_key() not in data:
			print("\u001b[1;31mNo metric information found. Please use the method find_metres() before parsing.\u001b[0m")
			return None
			
		if verbose:
			print("\u001b[1;32mMetric information found\u001b[0m")
	
		metre_and_form = data[cls.get_meta_key()]
		print("parsing with", metre_and_form)
		line_parsings_array = metre_parser.parse(metre_and_form, verbose)

		#now we save the parsing:
		data = cls.get_data(metre_parser.jpoem)
		data[cls.get_lines_key()] = line_parsings_array
		cls.save_data(metre_parser.jpoem, data)
		print("Parsing successfully completed")
	
	@classmethod
	def find_metres(cls, json_file: str, verbose: bool):
		metre_parser = cls.build_parser(json_file)
		metre = metre_parser.find_metre(verbose)
		data = cls.get_data(metre_parser.jpoem)
		if metre != None:
			data[cls.get_meta_key()] = metre.json_dict
			cls.save_data(metre_parser.jpoem, data)
	
	@classmethod
	def find_metres_for_each_lines(cls, json_file: str, verbose: bool = False):
		parser = cls.build_parser(json_file)
		results = parser.find_metres_for_each_line(verbose)
		if results == None:
			return

		print("Metres for each line:")
		for i, result in enumerate(results):
			print("\tline %d - %d parsing%s:"%(i+1, len(result), "s" if len(result) != 1 else ''))
			for line_parser, line_parsing in result:
				print("\t\t %s %s - variation_level: %d"%(line_parser.metre.name, line_parser.form.name, line_parsing.variation_level))
	
	@classmethod
	def reset(cls, json_file: str):
		"""Deletes all the information previously stored by the CruscoArud plugin on the file `json_file"""
		parser = cls.build_parser(json_file)
		super().reset(parser.jpoem)
		print("File successfully reset.")
	
	@classmethod
	def render(cls, infile, outfile, translation_id, translation_arrangement, number_after, pretty_print):
		jpoem = JsonParser(infile)
		renderer = cls.build_renderer(jpoem)
		if renderer == None:
			return None
		text = renderer.render(translation_id, translation_arrangement, number_after, pretty_print)
		if outfile == None:
			print(text)
		else:
			with open(outfile, 'w') as out:		
				print(text, file=out)
