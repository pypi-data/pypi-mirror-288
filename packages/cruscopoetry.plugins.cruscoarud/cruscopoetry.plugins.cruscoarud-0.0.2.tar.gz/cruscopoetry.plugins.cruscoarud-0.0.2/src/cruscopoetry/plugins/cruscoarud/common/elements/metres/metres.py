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
from typing import Tuple, Union
import os


class Metre:
	"""Represents the base structure of a metre. The actual metre forms (tāmm, maǧzūʾ, etc.) are grouped in the instances of Metre and will be responsible of the actual parsing.
	
	Args:
		metre_num (int): the integer representing the num, as in :class:`constants.MetreNums`.
		feet_sequence (Tuple[int]): a tuple of integer values representing the feet of the metre.
	"""
	
	
	
	def __init__(self, index: int, name: str, arabic_name: str, feet_sequence: Tuple[int], forms: list):
		self._index = index
		self._name = name
		self._arabic_name = arabic_name
		self._feet_sequence = tuple(feet_sequence)
		self.forms = forms
	
	def __index__(self):
		return self._index
	
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
	def feet_sequence(self):
		return self._feet_sequence

	def has_form(self, form: int) -> bool:
		"""Returns True if the metre can accept the form `form`, False otherwise.
		
		Args:
			form (int): the integer representing the metre form whose acceptability for the metre must be checked. Besides an int, it can also be an instance of MetreForm
		"""
		if type(form) != int:
			form = int(form)
			
		return form in self.forms
		
	
	def __str__(self):
		ret_str = '\t0x%x - %s:'%(self.index, self.name)
		ret_str += os.linesep
		ret_str += "\t" + str(self.feet_sequence)
		
		return ret_str
		

class MetrePool(SubscriptableSet):
	
	def __str__(self):
		ret_str = "al-buḥūr:"
		for i in self.indexes:
			ret_str += os.linesep*2
			ret_str += str(self[i])
		return ret_str

