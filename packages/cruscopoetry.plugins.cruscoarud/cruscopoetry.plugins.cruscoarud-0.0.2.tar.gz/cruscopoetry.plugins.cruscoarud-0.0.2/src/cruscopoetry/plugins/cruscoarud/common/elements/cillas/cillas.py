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
from typing import List, Tuple
import os
from ..abstract.condition import AbstractCondition, InvalidConditionSyntaxError
from ..abstract.transformation import AbstractTransformation, InvalidTransformationSyntaxError, UnapplicableTransformationError
from ..feet.feet import Foot
import re


class CillaCondition(AbstractCondition):
	"""Represents a condition that a sequence of EPU must satisfy in order to be affected by the ʿilla.
	
	Args:
		condition_string (str): the string that represents the condition, as in the configuration file.
	"""
	
	PARSER = re.compile("(?P<index>(\\+|-)?[0-9]+)\\s*(?P<confrontation>(\\!)?\\->)\\s*(?P<epu>[01]+)")
	
	def __init__(self, condition_string: str):
		match = self.__class__.PARSER.fullmatch(condition_string)
		if match == None:
			raise InvalidConditionSyntaxError(condition_string)
		
		self.index = int(match.group("index"))
		self.must_equal = True if match.group("confrontation") == "->" else False
		self.epu = match.group("epu")
		
	@property
	def confrontation_sign(self):
		if self.must_equal:
			return "->"
		else:
			return "!->"
		
	def __str__(self):
		return "%s(%d %s %s)"%(self.__class__.__name__, self.index, self.confrontation_sign, self.epu)
		
	def __repr__(self):
		return str(self)

	def verify(self, sequence: List[str]) -> bool:
		"""Takes a list of strings representing EPUs and verifies if it satisfies the condition"""
		if self.index >= len(sequence):
			return False
			
		epu_to_check = sequence[self.index]
		return (epu_to_check == self.epu) == self.must_equal


class CillaTransformation(AbstractTransformation):
	"""Represents a transformation that a foot affected by a ʿilla must undergo.
	
	Args:
		transformation_string (str): the string that represents the transformation.
	"""
	
	PARSER = re.compile("(?P<old_element>[+-]?[01]+)?\\s*(?P<transformation>(put\\s+|pop\\s+|->))\\s*(?P<element>[+-]?[0-9]+)")
	
	def _put(self, element: str, sequence: Tuple[str]):
		"""Handles the 'put' transformation. If element is a single ḥarf, it appends it to the last EPU of sequence; if it is an EPU, it appends it to sequence as new item.
		
		Args:
			element (str): the element to append
			sequence (Tuple[str]): the sequence of EPUs
		"""

		#first case: element is a ḥarf
		if element in ('0', '1'):
			new_element = sequence[-1] + element
			#if sequence[-1] was a watid mafrūq, then we have now a '0101' sequence, which needs to be split into two sabab ḫafīfs:
			if new_element != '0101':
				sequence_tail = (new_element,)
			else:
				sequence_tail = ("01", "01")
			
			sequence = sequence[:-1] + sequence_tail
		
		#second case: element is epu
		else:
			sequence = sequence + (element,)
		
		return sequence
	
	def _pop(self, element_index: int, sequence: Tuple[str]):
		"""Handles the 'pop' transformation.
		
		Args:
			element_index (int): the index of the element that must be dropped.
			sequence (Tuple[str]): the sequence that the transformation must be applied on
		
		Returns:
			sequence (Tuple[str]): the transformed sequence
		
		Raises:
			UnapplicableTransformationError: raised if there is no element in sequence at index element_index
		"""
###		print(" _pop:(%d, %r)"%(element_index, sequence))
		
		#first, we normalize the negative numbers through the module operation:
		element_index %= len(sequence)
		
		if element_index >= len(sequence):
			raise UnapplicableTransformationError(self.transformation_string, sequence)
###		print(sequence, "->", end=" ")
		sequence = sequence[:element_index] + sequence[element_index+1:]
###		print(sequence)
		
		return sequence
		
	def _replace(self, old_element: str, new_element: str, sequence: Tuple[str]):
		"""Handles replacement (->) transformation.
		
		Args:
			old_element (str): the element whose first occurrence must be replace
			new_element (str): the element with which old_element must be replaced
			sequence (Tuple[str]): the sequence that the transformation must be applied on
		
		Returns:
			sequence (Tuple[str]): the transformed sequence
		
		Raises:
			UnapplicableTransformationError: raised if there is no element in sequence at index element_index
		"""

		if old_element not in sequence:
			raise UnapplicableTransformationError(self._transformation_string, sequence)
		
		index = sequence.index(old_element)
		sequence = sequence[:index] + (new_element,) + sequence[index+1:]
		return sequence
			
	
	def __init__(self, transformation_string: str):
		self._transformation_string = transformation_string

		match = self.__class__.PARSER.fullmatch(transformation_string)
		if match == None:
			raise InvalidTransformationSyntaxError(transformation_string)

		self.old_element = match.group("old_element")
		self.element = match.group("element")
		
		if match.group("transformation")[:3] == 'put':
			self._transform_function = lambda sequence: self._put(self.element, sequence)
		elif match.group("transformation")[:3] == 'pop':
			self._transform_function = lambda sequence: self._pop(int(self.element), sequence)
		elif match.group("transformation")[:2] == '->':
			self._transform_function = lambda sequence: self._replace(self.old_element, self.element, sequence)
		
	def apply(self, sequence: Tuple[str]):
		
		#we create a tuple in order to be able to work on it without modifying the original list object:
		sequence = tuple(sequence)
		return self._transform_function(sequence)
		
	def __str__(self):
		return "%s(%s)"%(self.__class__.__name__, self._transformation_string)
	
	def __repr__(self):
		return str(self)


class Cilla:
	"""Represents a cilla."""
	
	def __init__(self, index: int, name: str, arabic_name: str, in_hashw: bool, conditions: List[str], transform: List[str]):
		self._index = index
		self._name = name
		self._arabic_name = arabic_name
		self._in_hashw = in_hashw


		try:
			self._conditions = tuple(CillaCondition(condition) for condition in conditions)

		except InvalidConditionSyntaxError as e:
			print("\u001b[1;31mCondition syntax error found in Cilla 0x%x - %s:\u001b[0m"%(self.index, self.name))
			raise e


		try:
			self._transformations = tuple(CillaTransformation(transformation) for transformation in transform)

		except InvalidTransformationSyntaxError as e:
			print("\u001b[1;31mTransformation syntax error found in Cilla 0x%x - %s:\u001b[0m"%(self.index, self.name))
			raise e

		except UnapplicableTransformationError as e:
			print("\u001b[1;31mUnapplicable transformation in Cilla 0x%x - %s:\u001b[0m"%(self.index, self.name))
			raise e
	
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
		return self._name
	
	@property
	def in_hashw(self):
		return self._in_hashw
		
	@property
	def conditions(self):
		return self._conditions
		
	@property
	def transformations(self):
		return self._transformations
		
	@property
	def variation_level(self) -> int:
		if len(self.transformations) == 0:
			return 0
		else:
			return 4
	
	def is_possible(self, foot: Foot) -> bool:
		"""Returns True if it is possible to apply the ʿilla on the Foot instance `foot`, else False"""
		sequence = foot.epu_sequence
		for condition in self.conditions:
			if not condition.verify(sequence):
				return False
		return True
		
	def transform(self, foot: Foot) -> Tuple[str]:
		"""Takes a Foot instance and, if the ʿilla is applicable, returns a tuple of ḥarf values representing the mutated foot; otherwise, returns None"""
###		print("Transforming", foot.epu_sequence, "by", self.name)
		if not self.is_possible(foot):
			return None
		sequence = foot.epu_sequence
		for transformation in self.transformations:
###			print(sequence)
			sequence = transformation.apply(sequence)
###		print(sequence)
		return sequence
			
	
	def __str__(self):
		ret_str = '\t0x%x - %s, possible in ḥašw: %s'%(self.index, self.name, self.in_hashw)
		ret_str += os.linesep
		ret_str += "\tconditions: " + str(self.conditions)
		ret_str += os.linesep
		ret_str += "\ttransform: " + str(self.transformations)
		
		return ret_str


class CillaPool(SubscriptableSet):
	
	def __str__(self):
		ret_str = "al-ʿilal:"
		for i in self.indexes:
			ret_str += os.linesep*2
			ret_str += str(self[i])
		return ret_str


