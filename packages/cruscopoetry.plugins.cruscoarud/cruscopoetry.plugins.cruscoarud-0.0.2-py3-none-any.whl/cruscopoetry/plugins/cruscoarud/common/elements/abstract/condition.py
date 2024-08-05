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


class AbstractCondition(metaclass=abc.ABCMeta):

	@abc.abstractmethod
	def verify(self, sequence: str) -> bool:
		"""Takes a sequence and verifies if it satisfies the condition represented by the instance."""
		pass
		

class ConditionError(Exception):

	def __init__(self, condition_string: str):
		super().__init__()
		self.condition_string = condition_string


class InvalidConditionSyntaxError(ConditionError):

	def __init__(self, condition_string: str):
		super().__init__(condition_string)
	
	def __str__(self):
		return "Invalid condition syntax: '%s'"%self.condition_string

