# This file is part of Cruscoarud, a plugin of Cruscopoetry.
# 
# Cruscoarud is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Cruscoarud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Cruscoarud. If not, see <http://www.gnu.org/licenses/>.
from ..common.metric_elements import MetricElements
from .line_parser import LineParser
from cruscopoetry.core.jsonparser import JsonParser
from collections import OrderedDict
from typing import Tuple
from .exceptions import FailedParsingException, NotMatchingColaNumberError
from functools import wraps


class TextParser:
	"""Parser of the metric patterns of a text."""

	LINE_PARSER_CLASS = LineParser

	def __init__(self, infile: JsonParser, elements_instance: MetricElements = None):
		if isinstance(infile, JsonParser):
			self.jpoem = infile
		else:
			self.jpoem = JsonParser(infile)
		self._elements = elements_instance if elements_instance != None else MetricElements()

		self.metre, self.form = None, None
		self.line_parser = None
		
	@property
	def line_parser_class(self):
		return self.__class__.LINE_PARSER_CLASS

	def _set_metre_and_form(self, metre_info):
		if type(metre_info) == str:
			if metre_info[:2] == "0x":
				metre_info = int(metre_info, base = 16)
			else:
				metre_info = int(metre_info, base = 10)
		
		metre = metre_info // self._elements.metre_info_base_16_order
		form = metre_info % self._elements.metre_info_base_16_order
		self.metre = metre
		self.form = form
		self.line_parser = self.line_parser_class(self.metre, self.form, self._elements)

	def _get_all_line_parsers(self) -> Tuple[LineParser]:
		line_parsers = []
		for metre in self._elements.metres_pool:
			for form in metre.forms:
				line_parsers.append(self.line_parser_class(metre, form, self._elements))
		return tuple(line_parsers)

	def find_metre(self, verbose: bool = False):
		"""Tries to find the right metre and metre form for parsing a text. If more than one metre is found, the one presenting the minor quantity of variations (ʿilal, ziḥāfāt) is returned."""
		parsers = [[line_parser, 0] for line_parser in self._get_all_line_parsers()]
		for line in self.jpoem.text.iter_lines():
			for i in range(len(parsers)-1,-1,-1):
				try:
					line_parsing = parsers[i][0].parse(line)
					parsers[i][1] += line_parsing.variation_level
				except FailedParsingException:
					parsers.pop(i)
				except NotMatchingColaNumberError:
					parsers.pop(i)
			if len(parsers) == 0:
				if verbose:
					print("Parsing stopped at line number %d"%line.number)
					print(line.transcription)
					syllables = tuple(str(syllable) for syllable in line.iter_syllables())
					print(' '.join(syllables))
				break
		
		if len(parsers) == 0:
			print("\u001b[1;31mNo possible parsing found.\u001b[0m")
			return None
			
		#now we sort all the parsers by their variation level and return the one with the lowest:
		parsers = sorted(parsers, key = lambda item: item[1])
		
		if len(parsers) > 1:
			print("\u001b[1;33mMore than one possible parsing found:")
		else:
			print("\u001b[1;32mOne possible parsing found!")
			
			for parser in parsers:
				print("%s %s (variation level: %d)"%(parser[0].metre.name, parser[0].form.name, parser[1]))
			print("\u001b[0m")
		
		return parsers[0][0]
		
	def find_metres_for_each_line(self, verbose: bool = False) -> tuple:
		"""Tries to parse each line of the poem with any metre and metre form possible combination, and returns a tuple where each item at index i is a tuple of (LineParser, LineParsing) pairs of 
		all the successful parsings of the line whose index is i."""
		results = []
		line_parsers = self._get_all_line_parsers()
		for line in self.jpoem.text.iter_lines():
			line_parsings = []
			if verbose:
				print("\u001b[1;33mFinding metre for line %d, %s:"%(line.number, line.transcription), end=" ")
				for colon in line.iter_cola():
					print(line_parsers[0]._to_harfs(colon), end= " ")
				print("\u001b[0m", end=" ")
			for line_parser in line_parsers:
				try:
					line_parsing = line_parser.parse(line)
					line_parsings.append((line_parser, line_parsing))
				except FailedParsingException as e:
					pass
				except NotMatchingColaNumberError:
					pass
			line_parsings = sorted(line_parsings, key = lambda it: it[1].variation_level)
			if verbose:
				if len(line_parsings) > 1:
					print("\u001b[1;33m%d matches\u001b[0m"%len(line_parsings))
				elif len(line_parsings) == 1:
					print("\u001b[1;32m%d match\u001b[0m"%len(line_parsings))
				else:
					print("\u001b[1;31mNo match\u001b[0m")
			results.append(tuple(line_parsings))
		return tuple(results)

	def parse(self, metre_info, verbose: bool = False):
		self._set_metre_and_form(metre_info["metre_and_form"])
		line_parsings_array = []
		for line in self.jpoem.text.iter_lines():
			try:
				line_parsing = self.line_parser.parse(line)
				if verbose:
					print(line_parsing)

				if line.count_cola() != len(line_parsing._cola_parsings):
					raise NotMatchingColaNumberError(line_parsing, line)
				
				line_parsings_array.append(line_parsing.json_dict)
				
			except FailedParsingException as e:
				e.line_number = line.number
				e.metre = self._elements.metres_pool[self.metre].name
				e.form = self._elements.metre_forms_pool[self.form].name
				e.color = FailedParsingException.WARNING
				print(e)

		return line_parsings_array
