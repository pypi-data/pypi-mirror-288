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
from ..exceptions import CruscoArudException


class ConfigurationException(Exception):
	"""Base class for all exceptions related to configuration loading"""
	
	def __init__(self):
		super().__init__()
		self.config = Config()


class CillaException(ConfigurationException):
	
	def __init__(self):
		super().__init__()


class UnapplicableCillaException(ConfigurationException):
	"""Raised when one tries to apply a *ʿilla* to a foot which can not be affected by it """
	
	def __init__(self, cilla_num: int):
		super().__init__()
		self.cilla_num = cilla_num


class DaairaException(ConfigurationException):
	"""Raised when one tries to get an impossible sequence of feet from a dāʾira."""
	
	def __init__(self, epu_sequence, start_epu, watid_index):
		super().__init__()
		self.epu_sequence, self.start_epu, self.watid_index = epu_sequence, start_epu, watid_index
	
	def __str__(self):
		return "Impossible to get feet with watids at index %d and start_index as %d from this sequence: %s"%(self.watid_index, self.start_epu, self.epu_sequence)
