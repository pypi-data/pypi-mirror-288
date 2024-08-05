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
from .foot_parser import FootParser, FootParsing
from .cilla_parser import CillaParsing
from .exceptions import MorePossibleParsingsWarning, FailedParsingException
from typing import Tuple


class HemistichParsing:

	def __init__(self, hashw_parsing: Tuple[CillaParsing], final_parsing: CillaParsing):
		self.feet_parsing = hashw_parsing + (final_parsing,)
	
	@property
	def variation_level(self):
		ret_int = 0
		for foot in self.feet_parsing:
			ret_int += foot.variation_level
		return ret_int
		
	@property
	def json_array(self):
		"""The array of integers that will represent this parsing in the json file"""
		return tuple(foot.json_number for foot in self.feet_parsing)
		
	@property
	def as_tuple(self):
		"""The array of integers that will represent this parsing in the json file"""
		return tuple(foot.as_tuple for foot in self.feet_parsing)

	@classmethod
	def from_no_harf(cls, final_parsing):
		return cls(tuple(), final_parsing)
	
	def __repr__(self):
		return "%s(%r)"%(self.__class__.__name__, self.feet_parsing)


class HemistichParser:
	"""Handles the parsing of a hemistich (*miṣrāʿ*).
	
	Args:
		feet_sequence (tuple): a tuple of integers representing the feet of the hemistich
	
	Attrs:
		feet_sequence (tuple): a tuple of FootParser instances representing the feet of the hemistich
		hashw (tuple): a tuple of FootParser instances representing the *ḥašw* of the hemistich
		last_foot (FootParser): the final foot of the hemistich (ʿarūḍ or ḍarb)
	"""

	def __init__(self, feet_sequence: Tuple[int], elements: MetricElements = None):
		self._elements = elements if elements != None else MetricElements()
		self.feet_sequence = tuple(FootParser(foot, self._elements, from_hashw=True) for foot in feet_sequence[:-1])
		self.feet_sequence += (FootParser(feet_sequence[-1], self._elements, from_hashw=False),)

	@property
	def json_dict(self):
		return {
			"feet_sequence": [int(foot_parser.foot) for foot_parser in self.feet_sequence]
		}
	
	@property
	def hashw(self) -> Tuple[FootParser]:
		return self.feet_sequence[:-1]
	
	@property
	def last_foot(self) -> FootParser:
		return self.feet_sequence[-1]
		
	def _get_parsing_length(self, cilla_parsings: tuple):
		"""Takes a sequence of CillaParsing instances and return the number of ḥarfs they occupy in total in a verse."""
		ret_int = 0
		for cilla_parsing in cilla_parsings:
			ret_int += len(cilla_parsing)
		return ret_int
		
	def _parse_hashw(self, harfs: str, foot_index: int = 0, previous_parsings: list = None):
###		print("_parse_hashw(%s, %d, %r)"%(harfs, foot_index, previous_parsings))

		possible_parsings = []

		if previous_parsings == None:
			previous_parsings = [tuple()]
		
		#we calculate the index of the starting letter of the foot, looking at the lengths of the CillaParsing instances in previous_parsing
		for previous_parsing in previous_parsings:
###			print("\u001b[1;33m'", previous_parsing, "'\u001b[0m")
			letters_before = self._get_parsing_length(previous_parsing)
		
###			print("\u001b[1;33mletters before:", letters_before, "\u001b[0m")
			harfs_portion = harfs[letters_before:]
###			print("\u001b[1;33m", harfs_portion, "\u001b[0m")
			current_foot_parsings = self.hashw[foot_index].parse(harfs_portion, expected_cilla = self._elements.configuration.cillas_enum.NOTHING)
###			print("\u001b[1;33m foot", current_foot_parsings.foot.name, "at index", foot_index, "\u001b[0m")
			for cilla_parsings in current_foot_parsings:
				possible_parsings.extend([previous_parsing + (cilla_and_zihaafa_parsing,) for cilla_and_zihaafa_parsing in cilla_parsings])
###		print("\u001b[1;33m", possible_parsings, "\u001b[0m")

		if foot_index == len(self.hashw) - 1:
			#now we check that no more letters are left, and in that case we return the parsing, else an empty list:
			
			for i in range(len(possible_parsings)-1,-1,-1):
				parsed_letters = self._get_parsing_length(possible_parsings[i])
				if len(harfs) > parsed_letters:
###					print("\u001b[1;31mRemaining letters:", "'%s'"%harfs[parsed_letters:], "\u001b[0m")
					possible_parsings.pop(i)
###				else:
###					print("\u001b[1;32mNo more letters!\u001b[0m")
			
###			print("\u001b[1;33m_parse_hashw returns:", possible_parsings, "\u001b[0m")
			return possible_parsings
		else:
			return self._parse_hashw(harfs, foot_index+1, possible_parsings)
			
	
	def parse(self, harfs: str, expected_final_cilla: int = -1):
		"""Parses a sequence of ḥarf values and returns a HemistichParsing instance"""
		possible_parsings = []
###		print("HemistichParser.parse(%s)"%harfs)

		final_parsing = self.last_foot.parse(harfs, expected_cilla=expected_final_cilla)
###		print("final parsing:")
		for cilla_parsings in final_parsing:
			for cilla_parsing in cilla_parsings:
				hashw = harfs[:-len(cilla_parsing)]
###				print("With final parsing as (%s, %s, %s) and hashw as '%s':"%(self.last_foot.foot.name, cilla_parsing.cilla.name, cilla_parsing.zihaafa.name, hashw))
	
				if len(self.hashw) > 0:
					hashw_parsings = self._parse_hashw(hashw)
###					print(hashw_parsings)
					for hashw_parsing in hashw_parsings:
						possible_parsings.append(HemistichParsing(hashw_parsing, cilla_parsing))
				else:
					hashw = harfs[:-len(cilla_parsing)]
					if len(hashw) == 0:
						possible_parsings.append(HemistichParsing.from_no_harf(cilla_parsing))
		

		if len(possible_parsings) > 1:
			raise MorePossibleParsingsWarning(possible_parsings)

		if len(possible_parsings) == 0:
			raise FailedParsingException

		possible_parsings = sorted(possible_parsings, key= lambda item: item.variation_level)
		
		return possible_parsings[0]
		
		
