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
from .exceptions import NotMatchingColaNumberError, FailedParsingException
from .hemistich_parser import HemistichParser, HemistichParsing
from .foot_parser import FootParser
from cruscopoetry.core.jsonparser import JsonParser, JsonLine, JsonColon
from typing import List


class LineParsing:
	"""Represents the parsing of a line.
	
	Args:
		cola_parsings (List[HemistichParsing]): a list of HemistichParsing instances, each one representing the parsing of a colon of the verse.
	
	Attrs:
		cola_parsings (List[HemistichParsing]): a list of HemistichParsing instances, each one representing the parsing of a colon of the verse.
	"""
	
	def __init__(self, cola_parsings: List[HemistichParsing], elements: MetricElements):
		self._cola_parsings = cola_parsings
		self._elements = elements if elements != None else MetricElements()
	
	@property
	def cola_parsings(self):
		return self._cola_parsings
	
	def __iter__(self):
		return iter(self._cola_parsings)

	@property
	def json_dict(self):
		
		ret_array = []
		for colon_parsing in self._cola_parsings:
			ret_array.append(colon_parsing.json_array)
		
		return ret_array
		
	
	@property
	def as_tuple(self):
		return tuple(hemistich.as_tuple for hemistich in self)
	
	@property
	def variation_level(self):
		ret_int = 0
		for colon_parsing in self._cola_parsings:
			ret_int += colon_parsing.variation_level
		return ret_int


class LineParser:
	"""Handles the parsing of a line.
	
	Args:
		metre_index (int): the integer representing the abstract metre
		form_index (int): the integer representing the actual metre form.

	Raises:
		MetreFormError: raised if one attempts to apply a form to a metre that doesn't accept it.
	"""

	def __init__(self, metre_index: int, form_index: int, elements: MetricElements = None):
		self._elements = elements if elements != None else MetricElements()

		self._metre = self._elements.metres_pool[metre_index]
		if not self._metre.has_form(form_index):
			raise exceptions.MetreFormError(self._metre, form)

		self._form = self._elements.metre_forms_pool[form_index]
		feet_sequence = self._form.apply(self._metre)
		
		#now we have to individuate the ṣadr and the ʿaǧz splitting the sequence in two equal halves:
		half_index = len(feet_sequence) // 2
		
		self.sadr, self.cajz = HemistichParser(feet_sequence[:half_index], self._elements), HemistichParser(feet_sequence[half_index:], self._elements)

	@property
	def json_dict(self):
		print(int(self.metre))
		print(self._elements.metre_info_base_16_order)
		print(int(self.form))
		metre_and_form = int(self.metre) * self._elements.metre_info_base_16_order + int(self.form)
		return {
			"metre_and_form": metre_and_form
		}

	@property
	def metre(self):
		return self._metre
	
	@property
	def form(self):
		return self._form
	
	@property
	def name(self):
		return self._metre.name + " " + self._form.name
	
	def _morae_to_harfs(self, morae: int) -> str:
		"""Takes the number of morae composing a syllable and returns the corresponding sequence of ḥarf values."""
		if morae == 1:
			return "0"
		else:
			return self._morae_to_harfs(morae-1) + "1"

	def _to_harfs(self, colon: JsonColon) -> str:
		"""Takes a JsonColon instance and returns a string of ḥarf values representing its prosodic structure."""
		morae = tuple(syllable._jdict["morae"] for syllable in colon.iter_syllables())
		morae = tuple(self._morae_to_harfs(morae_int) for morae_int in morae)
		harfs = ''.join(morae) 
		
		#if the sequence ends with a vocalized ḥarf, we need to add a prosodical silent one:
		if harfs[-1] == "0":
			harfs += "1"
		return harfs
		
	def parse(self, line: JsonLine):
		
		if line.count_cola() != (self.caruud_numbers + 1):
			raise NotMatchingColaNumberError(self.form, line)
		
		parsings = []
		for colon in line.iter_cola():
			harfs = self._to_harfs(colon)
			try:
				if colon.number < line.count_cola():
					parsings.append(self.sadr.parse(harfs))
				else:
					parsings.append(self.cajz.parse(harfs))
			except FailedParsingException as e:
				e.colon_number = colon.number
				e.harfs = harfs
				raise e
		return LineParsing(parsings, self._elements)
		
	@property
	def caruud(self) -> FootParser:
		return self.sadr.last_foot

	@property
	def darb(self) -> FootParser:
		return self.cajz.last_foot
		
	@property
	def caruud_numbers(self):
		return self._form._caruuds_number
	
	@property
	def metre(self):
		return self._metre
	
	@property
	def form(self):
		return self._form
		
		
		
