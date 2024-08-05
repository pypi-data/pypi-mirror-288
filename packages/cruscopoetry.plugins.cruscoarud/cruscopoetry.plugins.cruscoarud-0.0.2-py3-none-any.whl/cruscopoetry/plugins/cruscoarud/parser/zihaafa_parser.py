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
from ..common.elements.zihaafas import Zihaafa


class ZihaafaParsing:
	"""Represents the result of the confrontation of a portion of a hemistich with a particular ziḥāfa of a particular ʿilla of a particular foot.
	The instances of this class are indexable, and can therefore be collected in a SubscriptableSet.
	
	Args:
		zihaafa: the zihaafa that has been parsed
		length: the number of ḥarfs from the parsed hemistich that have matched the ziḥāfa parsing.
	"""
	
	def __init__(self, zihaafa: Zihaafa, length: int):
		self._zihaafa = zihaafa
		self._length = length
	
	@property
	def zihaafa(self):
		return self._zihaafa
	
	@property
	def length(self):
		return self._length
	
	def __len__(self):
		return self._length
		
	def __str__(self):
		return "%s, %d morae"%(self._zihaafa.name, self._length)


class ZihaafaParser:

	def __init__(self, zihaafa: Zihaafa, sequence, from_hashw, from_kharm: bool = False):
		self._zihaafa = zihaafa
		self._match_sequence = self._zihaafa.transform(sequence, from_kharm)
		self._from_hashw = from_hashw
		self._from_kharm = from_kharm
		
	def __index__(self):
		return int(self._zihaafa)

	@property
	def zihaafa(self):
		return self._zihaafa
		
	@property
	def match_sequence(self):
		return self.match_sequence

	@property
	def length(self):
		return len(self._match_sequence)
		
	def matches(self, harfs: str, full_match: bool = False):
		if full_match:
			return harfs == self._match_sequence
		else:
			if self._from_hashw:
###				print("Matching from _hashw:", harfs[:self.length], "==", self._match_sequence)
				return harfs[:self.length] == self._match_sequence
			else:
###				print("Matching not from _hashw:", harfs[-self.length:], "==", self._match_sequence)
				return harfs[-self.length:] == self._match_sequence
		
	def parse(self, harfs: str, full_match: bool = False) -> ZihaafaParsing:
		"""Takes a string of ḥarf values and checks if the Ziḥāfa matches it.
		
		Args:
			harfs (str): the string of ḥarf values
		
		Returns:
			parsing (ZihaafaParsing): the result of the parsing if it has been successful, else None
		"""
		if not self.matches(harfs, full_match):
			return None
		else:
			return ZihaafaParsing(self._zihaafa, self.length)

