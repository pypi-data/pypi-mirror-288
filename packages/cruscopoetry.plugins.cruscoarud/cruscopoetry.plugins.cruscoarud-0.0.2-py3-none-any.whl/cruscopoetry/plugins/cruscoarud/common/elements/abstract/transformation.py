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
import abc


class AbstractTransformation(metaclass=abc.ABCMeta):

	@abc.abstractmethod
	def apply(self, sequence):
		"""Takes a sequence and applies on it the transformation represented by the instance."""
		pass
		

class TransformationError(Exception):

	def __init__(self, transformation_string: str):
		super().__init__()
		self.transformation_string = transformation_string


class InvalidTransformationSyntaxError(TransformationError):

	def __init__(self, transformation_string: str):
		super().__init__(transformation_string)
	
	def __str__(self):
		return "Invalid transformation syntax: '%s'"%self.transformation_string


class UnapplicableTransformationError(TransformationError):

	def __init__(self, transformation_string: str, sequence: tuple):
		super().__init__(transformation_string)
		self.sequence = sequence
	
	def __str__(self):
		return "The transformation '%s' can not be applied to '%s' (sequence is not long enough)"%(self.transformation_string, self.sequence)

