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
import re


class ZihaafaCondition(AbstractCondition):
	"""Represents a condition that a sequence of EPU must satisfy in order to be affected by the ʿilla.
	
	Args:
		condition_string (str): the string that represents the condition, as in the configuration file.
	"""
	
	PARSER = re.compile("(?P<index>(\\+|-)?[0-9]+)\\s*(?P<confrontation>(\\!)?\\->)\\s*(?P<harf>[01])")
	
	def __init__(self, condition_string: str):
		match = self.__class__.PARSER.fullmatch(condition_string)
		if match == None:
			raise InvalidConditionSyntaxError(condition_string)
		
		self.index = int(match.group("index"))
		self.must_equal = True if match.group("confrontation") == "->" else False
		self.harf = match.group("harf")
		
	@property
	def confrontation_sign(self):
		if self.must_equal:
			return "->"
		else:
			return "!->"
		
	def __str__(self):
		return "%s(%d %s %s)"%(self.__class__.__name__, self.index, self.confrontation_sign, self.harf)
		
	def __repr__(self):
		return str(self)

	def verify(self, sequence: List[str], from_kharm: bool = False) -> bool:
		"""Takes a list of strings representing EPUs and verifies if it satisfies the condition"""
		
		sequence = ''.join(sequence)
		
		index = self.index - 1 if from_kharm else self.index
		if index >= len(sequence):
			return False
			
		harf_to_check = sequence[index]
		return (harf_to_check == self.harf) == self.must_equal


class ZihaafaTransformation(AbstractTransformation):
	"""Represents a transformation that a sequence of *ḥarf*s affected by a certain *ziḥāfa* must undergo.
	
	Args:
		tranformation_string (str): the string representing the transformation
	"""
	
	PARSER = re.compile("(?P<transformation>(drop)|(silence))\\s+(?P<index>[+-]?[0-9]+)")
	
	def _drop(self, index: int, sequence: str):
		"""Handles the drop transformation.

		Args:
			index (int): the index of the ḥarf that must be dropped
			sequence (str): the sequence of ḥarf values that the transformation must be applied on.
		
		Returns:
			sequence (str): the transformed sequence
		
		Raises:
			UnapplicableTransformationError: raised if there is no ḥarf in `sequence` at index `index`
		"""
		if index >= len(sequence):
			raise UnapplicableTransformationError(self._transformation_string, sequence)
		
		sequence = sequence[:index] + sequence[index+1:]
		return sequence
	
	def _silence(self, index: int, sequence: str):
		"""Handles the silence transformation.

		Args:
			index (int): the index of the ḥarf that must be silenced
			sequence (str): the sequence of ḥarf values that the transformation must be applied on.
		
		Returns:
			sequence (str): the transformed sequence
		
		Raises:
			UnapplicableTransformationError: raised if there is no ḥarf in `sequence` at index `index`
		"""
		if index >= len(sequence):
			raise UnapplicableTransformationError(self._transformation_string)
		
		sequence = sequence[:index] + "1" + sequence[index+1:]
		return sequence
	
	def __init__(self, transformation_string: str):
		self._transformation_string = transformation_string
		match = self.__class__.PARSER.fullmatch(transformation_string)
		
		self.index = int(match.group("index"))

		if match.group("transformation") == 'drop':
			self._transform_function = self._drop
		else:
			self._transform_function = self._silence
	
	def __str__(self):
		return "%s(%s)"%(self.__class__.__name__, self._transformation_string)
	
	def __repr__(self):
		return str(self)
		
	def apply(self, sequence: str, from_kharm: bool = False) -> str:
		"""Applies the ziḥāfa to sequence.. The boolean parametre `from_kharm` (default False), indicates if the sequence has already been affected by the ʿilla "ḫarm" or not. If it is True,
		this must be specified, otherwise the result is indefinite."""
		index = self.index - 1 if from_kharm else self.index
		return self._transform_function(index, sequence)
	
	def affects_watid(self, sequence: Tuple[str], watid_index: int, from_kharm: bool = False):
		"""Checks if the application of the transformation to the sequence `sequence`, whose *watid* is at watid_index position, would affect the *watid* itself"""
		harfs_before = 0
		current_epu = -1
		
		index = self.index - 1 if from_kharm else self.index

		while index >= harfs_before:
			current_epu += 1
			harfs_before += len(sequence[current_epu])
		
		return current_epu == watid_index



class Zihaafa:
	"""Represents a ziḥāfa."""
	
	def __init__(self, index: int, name: str, arabic_name: str, conditions: List[str], transform: List[str]):
		self._index = index
		self._name = name
		self._arabic_name = arabic_name

		try:
			self._conditions = tuple(ZihaafaCondition(condition) for condition in conditions)

		except InvalidConditionSyntaxError as e:
			print("\u001b[1;31mSyntax error found in Zihaafa 0x%x - %s:\u001b[0m"%(self.index, self.name))
			raise e


		try:
			self._transformations = tuple(ZihaafaTransformation(transformation) for transformation in transform)

		except InvalidTransformationSyntaxError as e:
			print("\u001b[1;31mTransformation syntax error found in Zihaafa 0x%x - %s:\u001b[0m"%(self.index, self.name))
			raise e

		except UnapplicableTransformationError as e:
			print("\u001b[1;31mUnapplicable transformation in Zihaafa 0x%x - %s:\u001b[0m"%(self.index, self.name))
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
		return self._arabic_name
		
	@property
	def conditions(self):
		return self._conditions
		
	@property
	def transformations(self):
		return self._transformations
	
	@property	
	def variation_level(self):
		return len(self.transformations)
		
	def is_possible(self, sequence: Tuple[str], watid_index: int, from_kharm: bool = False):
###		print("\u001b[1;33mVerifying if %s is possible:\u001b[0m"%self.name)
		for condition in self.conditions:
			if not condition.verify(sequence, from_kharm):
###				print("\u001b[1;31msequence", sequence, "doesn't verify", condition, "\u001b[0m")
				return False
###		print("\u001b[1;32mAll conditions verified!\u001b[0m")

		for transformation in self.transformations:
			if transformation.affects_watid(sequence, watid_index, from_kharm):
###				print("\u001b[1;31mtransformation", transformation, "affects watid of", sequence, "\u001b[0m")
				return False
###		print("\u001b[1;32mAll transformations are watid-safe!\u001b[0m")
		
		##when the sequence contains a sabab ṯaqīl, we need also to check that the application of the ziḥāfa does not create sequences of more than four vocalized letter:
		## - ṭayy on mutafāʿilun would give MUTAFACILUn;
		## - kaff on mufāʿalatun would give mufa_CALATU MUFA_
		
		#however, it is still possible to apply these ziḥāfāt in combination with others (es. ḫazl = iḍmr + ṭayy on mutafāʿilun): muftacilun.
		#in order to avoid this situation, we add another check on the feet with sabab ṯaqīl:
		if "00" in sequence:
			transformed_sequence = self.transform(sequence, from_kharm)
			if (("00000" in transformed_sequence) or (transformed_sequence[-3:] == "000")):
				return False
				
		
		return True
		
	def transform(self, sequence: Tuple[str], from_kharm: bool = False) -> str:
		"""Takes a sequence of EPUs, applies the *ziḥāfa* on it and returns the new sequence as a string of ḥarf values."""
		sequence = ''.join(sequence)
		for transformation in self.transformations:
			sequence = transformation.apply(sequence, from_kharm)
		return sequence
		
	
	def __str__(self):
		ret_str = '\t0x%x - %s:'%(self.index, self.name)
		ret_str += os.linesep
		ret_str += "\tconditions: " + str(self.conditions)
		ret_str += os.linesep
		ret_str += "\ttransformations: " + str(self.transformations)
		
		return ret_str


class ZihaafaPool(SubscriptableSet):
	
	def __str__(self):
		ret_str = "al-ziḥāfāt:"
		for i in self.indexes:
			ret_str += os.linesep*2
			ret_str += str(self[i])
		return ret_str


