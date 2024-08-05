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
from typing import Tuple, List
from muc import SubscriptableSet
from ...exceptions import DaairaException
import os


class Daaira():
	"""Represents a *dāʾira*. This class is basically a sequence of strings of *ḥārf* values (each one representing an EPU) that can iterate from any starting point making a complete tour, i. e.
	as making a complete path on a circle. It will be used to generate the metres.
	
	Args:
		index (int): the integer representing the dāʾira;
		name (str): the dāʾira's name;
		epu_sequence (List[str]): a list of strings, each one representing an EPU sequence
	
	Attrs:
		index (int): the integer representing the dāʾira;
		name (str): the dāʾira's name;
		epu_sequence (Tuple[str]): a list of strings, each one representing an EPU sequence
	
	Raises:
		TypeError
		DaairaException: if one tries to form an impossible sequence of feet from an instance of this class.
		
	"""

	def __init__(self, index: int, name: str, arabic_name: str, epu_sequence: List[str]):
		self._index = index
		self._name = name
		self._arabic_name = arabic_name
		self._epu_sequence = tuple(epu_sequence)
	
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
	def epu_sequence(self):
		return self._epu_sequence

	def __getitem__(self, index: int):

		if type(index) == int:
			index %= len(self)
			return self._epu_sequence[index]

		elif type(index) == slice:
			start = index.start if index.start != None else 0
			step  = index.step  if index.step != None else 1
			ret_list = []

			#since range is not modular, we have to make sure that stop > start:
			stop = index.stop
			while stop < start:
				stop += len(self)
				
			for i in range(start, stop, step):
				ret_list.append(self.__getitem__(i))
			return ret_list

		else:
			raise TypeError("%s indices must be integers or slices, not %s"%(self.__class__.__name__, type(index)))
	
	def iter(self, start_index):
		"""Iterates along the dāʾira starting from start_index position; when the last element is reached, the iteration continues from item 0; it ends at item = start_index - 1"""
		start_index %= len(self)
		index = start_index
		yield self.__getitem__[index]
		index = (index + 1) % len(self)
		while index != start_index:
			yield self.__getitem__[index]
			index = (index + 1) % len(self)
	
	def __str__(self):
		ret_str = '\t0x%x - %s:'%(self.index, self.name)
		ret_str += os.linesep
		ret_str += "\t" + str(self._epu_sequence)
		
		return ret_str
		
	def _is_watid(self, sequence: str):
		return sequence in ("001", "010")
		
	def get_feet(self, start_epu: int, watid_index: int) -> Tuple[Tuple[str]]:
		"""Traverses base sequence from start_index, groups the EPUs in feet and returns them. Feet are grouped on the base of the position that the watid should have within them, represented 
		by the parametre watid_index. This integer can be both a positive or a negative value (es. -1 represents feet with the watid at last EPU."""

		#first we get the indexes of all the watids:
		watids = [i for i in range(len(self)) if self._is_watid(self._epu_sequence[i])]

		#if we substract to each item of watid the value of watid_index, we get the starting EPU of each foot that must be yielded:
		first_EPUs = [watid - watid_index for watid in watids]
		
		#we module each item of firsts_EPUs for len(self):
		first_EPUs = [item % len(self) for item in first_EPUs]
		
		#At this point, start_epu should be in first_EPUs. If not, we raise an error:
		if start_epu not in first_EPUs:
			raise DaairaException(self.epu_sequence, self.start_epu, self.watid_index)
		
		#if it is, we make it be the first item of the list, removing each item[0] and appending it to the list's end:
		while first_EPUs[0] != start_epu:
			first_item = first_EPUs.pop(0)
			first_EPUs.append(first_item)
		
		#now, for each i from 0 to len(first_EPUs) - 1, we store in feet the slice self[first_EPUs[i]:first_EPUs[i+1]]. Each slice is a foot:
		feet = []
		for i in range(len(first_EPUs)-1):
			feet.append(self[first_EPUs[i]:first_EPUs[i+1]])
		#we store also the sliceself[first_EPUs[-1]:first_EPUs[0]]:
		feet.append(self[first_EPUs[-1]:first_EPUs[0]])

		return tuple(tuple(foot) for foot in feet)
						
	

class DaairaPool(SubscriptableSet):
	"""A subclass of SubscriptablSet specifically intended to contain instances of Daaira"""
	
	def __str__(self):
		ret_str = "al-dawāʾir:"
		for i in self.indexes:
			ret_str += os.linesep*2
			ret_str += str(self[i])
		return ret_str

