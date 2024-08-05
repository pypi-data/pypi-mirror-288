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
from .cilla_parser import CillaParser, CillaParsing
from typing import Tuple
from muc import SubscriptableSet


class FootParsing:
	"""Represent the result of the parsing of a FootParser instance on a sequence of ḥarfs. If the parsing has been successful, the instance will contain one or more CillaParsing instances;
	otherwise, it will contain 0 ones."""
	
	def __init__(self, foot, parsings: Tuple[CillaParsing]):
		self._foot = foot
		self._parsings = parsings
		
	@property
	def parsings(self):
		return self._parsings
	
		
	def __iter__(self):
		return iter(self._parsings)
	
	def __getitem__(self, index: int):
		return self._parsings.__getitem__(i)
		
	@property
	def foot(self):
		return self._foot
	
	@property
	def is_successful(self):
		return len(self) > 0


class FootParser:

	def __init__(self, foot_index: int, elements: MetricElements = None, from_hashw: bool = True):
		self._elements = elements if elements != None else MetricElements()
		self._foot = self._elements.feet_pool[foot_index]
		self._from_hashw = from_hashw
		cillas = [self._elements.cillas_pool[cilla] for cilla in self._foot.cillas]
		
		cillas = [(cilla, self._foot, self._from_hashw, self._elements) for cilla in cillas]
		
		#if there are ʿillas whose application has returned None, we remove them from the list. However, we print a warning:
		for i in range(len(cillas)-1, -1, -1):
			if cillas[i][1] == None:
				print("\u001b[1;33mWarning: ʿilla '%s' resulted inapplicable to foot %s\u001b[0m"%(cillas[i][0].name, self.foot.name))
				
		#if the foot is inside a ḥašw, we keep only the ʿilal allowed in it:
		if self._from_hashw:
			cillas = tuple(cilla for cilla in cillas if cilla[0].in_hashw)
			
		self.cilla_parsers = SubscriptableSet(CillaParser(*cilla) for cilla in cillas)
		
	@property
	def from_hashw(self) -> bool:
		return self._from_hashw

	@property
	def foot(self):
		return self._foot
		
	def _parse_by_cilla(self, harfs: str, cilla_parser: CillaParser) -> CillaParsing:
		return cilla_parser.parse(harfs)
	
	def parse(self, harfs: str, expected_cilla: int = -1, full_match: bool = False):
		"""Parses a sequence of harfs value with all the allowed ʿilla forms and returns a FootParsing instance. If expected_cilla is -1, it tryes to parse `harfs` with all the available ʿillas;
		if instead it corresponds to the integer value of a ʿIlla, it first tries to parse it the verse with it; if the parsing is not successful, it tries again with all the ʿillas"""
		
		if expected_cilla in self.cilla_parsers.indexes:
			parsing = self.cilla_parsers[expected_cilla].parse(harfs, full_match)
			if parsing != None:
				return FootParsing(self._foot, tuple((parsing,),))

		parsings = tuple(cilla_parser.parse(harfs, full_match) for cilla_parser in self.cilla_parsers)
		parsings = tuple(parsing for parsing in parsings if not parsing == None)
###		print("FootParser.parse with no expexted:", parsings)
		return FootParsing(self._foot, parsings)
