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
from typing import Tuple, List
from ..metres import Metre
import os


class MetreFormException(Exception):

	def __init__(self):
		super().__init__()


class NahkFormingError(MetreFormException):

	def __init__(self, sequence):
		super().__init__()
		self.sequence = sequence
	
	def __str__(self):
		return "Impossible to apply nahk on the sequence %r: it has %d feet, which is not a multiple of 3."%(self.sequence, len(self.sequence))


class MetreForm:
	"""Represents one of the possible forms the metre can have (tāmm, maǧzūʾ, etc.)
	
	Args:
		index (int): the integer representing the metre form, according to the configuration file
		name (str): the name of the form
		caruuds_number (int): the quantity of ʿarūḍ hemistichs that the form has
		transform (int): an integer representing the transformation the metre must undergo (0 for no transformation, 1 for *ǧazʾ*, 2 for *nahk*)
		"""
	
	def __init__(self, index: int, name: str, arabic_name: str, caruuds_number: int, transform: int):
		self._index = index
		self._name = name
		self._arabic_name = arabic_name
		self._caruuds_number = caruuds_number
		self._transform_integer = transform

		if transform == 0:
			self._transform_function = self._leave_unchanged
		elif transform == 1:
			self._transform_function = self._make_jaz2
		elif transform == 2:
			self._transform_function = self._make_nahk
		else:
			raise RuntimeError("Unrecognized transformation: %d"%transform)
			
	def apply(self, metre: Metre) -> Tuple[int]:
		"""Applies the transformation to a metre.
		
		Args:
			metre (Metre): the abstract metre from which the form is built.)
		
		Returns:
			feet_sequence (Tuple[int]): a tuple of integers, each one representing a foot of the metre that has undergone the transformation.
		"""
		feet_sequence = metre.feet_sequence
		return self._transform_function(feet_sequence)

	def _leave_unchanged(self, feet_sequence: Tuple[int]):
		"""Represents a null transformation: the metre's hemistichs in this metre form must undergo no change"""
		return feet_sequence
	
	def _make_jaz2(self, feet_sequence: Tuple[int]):
		"""Applies a *ǧazʾ* (dropping of the last foot of every hemistich) to the metre represented by feet_sequence"""
		
		#since in the base form each metre is composed of two equal hemistichs, we just need to divide the length of sequence for 2 and we get the position of the caesura:
		half_index = len(feet_sequence) // 2
		
		#now we remove the foot immediatly preceding the caesura and the last one:
		feet_sequence = feet_sequence[:half_index-1] + feet_sequence[half_index:-1]
		return feet_sequence
	
	def _make_nahk(self, feet_sequence: Tuple[int]):
		"""Applies a *nahk* (dropping of the last two thirds of the feet sequence) to the metre represented by feet_sequence"""
		
		#nahk is applicable only if the number of feet is a multiple of three:
		if len(feet_sequence) % 3 != 0:
			raise NahkFormingError(feet_sequence)

		nahk_index = len(feet_sequence) // 3
		feet_sequence = feet_sequence[:nahk_index]
		return feet_sequence
		

	def __index__(self) -> int:
		return self._index
	
	@property
	def index(self) -> int:
		return self._index
	
	@property
	def number(self) -> int:
		return self._index + 1
	
	@property
	def name(self) -> str:
		return self._name
	
	@property
	def arabic_name(self) -> str:
		return self._arabic_name
	
	@property
	def caruuds_number(self) -> int:
		return self._caruuds_number
	
	@property
	def transformation_name(self) -> str:
		if self._transform_integer == 0:
			return "no tranformation"
		elif self._transform_integer == 1:
			return "ǧazʾ"
		elif self._transform_integer == 2:
			return "nahk"

	def __str__(self) -> str:
		ret_str = '\t0x%x - %s: %d ʿarūḍ, %s'%(self.index, self.name, self.caruuds_number, self.transformation_name)
		
		return ret_str
		

class MetreFormPool(SubscriptableSet):
	
	def __str__(self):
		ret_str = "šukūl al-buḥūr:"
		for i in self.indexes:
			ret_str += os.linesep*2
			ret_str += str(self[i])
		return ret_str

