# This file is part of Cruscopoetry.
# 
# Cruscopoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Cruscopoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Cruscopoetry. If not, see <http://www.gnu.org/licenses/>.
from muc import SubscriptableSet
from typing import List
import os


class Foot:
	
	def __init__(self, index: int, name: str, arabic_name: str, epu_sequence: List[str], cillas: List[int]):
		self._index = index
		self._name = name
		self._arabic_name = arabic_name
		self._epu_sequence = tuple(epu_sequence)
		self.cillas = cillas
	
	def __index__(self):
		return self._index

	def __len__(self):
		return len(self._epu_sequence)
	
	@property
	def index(self):
		return self._index
	
	@property
	def number(self):
		return self._index + 1
	
	@property
	def name(self):
		return self._name
	
	@property
	def arabic_name(self):
		return self._arabic_name
		
	@property
	def watid_index(self) -> int:
		"""Returns the index expressing the position of the *watid* within the foot."""
		for i in range(len(self.epu_sequence)):
			if self.epu_sequence[i] in ("001", "010"):
				return i
	
	@property
	def epu_sequence(self):
		return self._epu_sequence
	
	def __str__(self):
		ret_str = '\t0x%x - %s:'%(self.index, self.name)
		ret_str += os.linesep
		ret_str += "\t" + str(self._epu_sequence)

		return ret_str 


class FeetPool(SubscriptableSet):
	
	def __str__(self):
		ret_str = "al-tafāʿīl:"
		for i in self.indexes:
			ret_str += os.linesep*2
			ret_str += str(self[i])
		return ret_str
	
	def get_index(self, epu_sequence: List[str]):
		"""Returns the index of the foot having `epu_sequence` as its base sequence, else None"""
		for foot in self:
			if foot.epu_sequence == epu_sequence:
				return int(foot)
		return None
	
